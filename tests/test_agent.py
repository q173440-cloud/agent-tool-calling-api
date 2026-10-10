import unittest
from unittest.mock import Mock, patch
from requests.exceptions import Timeout
from agent import run_agent


class TestAgentTimeoutAndRegression(unittest.TestCase):
    """
    Agent HTTP 超时处理与核心功能回归测试套件 (Mock 驱动，不依赖真实网络与线上 API)
    """

    def test_timeout_first_request(self):
        """
        场景 1: 首次 LLM 请求 Timeout
        - 模拟首次 HTTP 请求直接超时
        - 验证返回超时友好提示
        - 验证 HTTP 请求次数为 1
        """
        with patch(
            "agent.requests.post",
            side_effect=Timeout("模拟首次请求超时")
        ) as mock_post:
            result = run_agent("你好")

            self.assertEqual(result, "模型服务响应超时，请稍后重试")
            self.assertEqual(mock_post.call_count, 1)

    def test_timeout_after_tool_call(self):
        """
        场景 2: Tool Calling 后续请求 Timeout
        - 首次请求返回 Tool Call (get_order_status A1002)
        - 本地成功执行工具并生成 tool 消息
        - 第二次 HTTP 请求模拟超时
        - 验证返回超时友好提示
        - 验证 HTTP 请求次数为 2
        - 验证第二次请求带上了工具执行结果
        """
        first_response = Mock()
        first_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_test_001",
                                "type": "function",
                                "function": {
                                    "name": "get_order_status",
                                    "arguments": '{"order_id": "A1002"}'
                                }
                            }
                        ]
                    }
                }
            ]
        }

        with patch(
            "agent.requests.post",
            side_effect=[
                first_response,
                Timeout("模拟第二次请求超时")
            ]
        ) as mock_post:
            result = run_agent("查询订单 A1002 的状态")

            self.assertEqual(result, "模型服务响应超时，请稍后重试")
            self.assertEqual(mock_post.call_count, 2)

            second_request = mock_post.call_args_list[1]
            messages = second_request.kwargs["json"]["messages"]

            tool_messages = [
                msg for msg in messages
                if msg.get("role") == "tool"
                and msg.get("tool_call_id") == "call_test_001"
            ]
            self.assertEqual(len(tool_messages), 1)
            self.assertEqual(tool_messages[0].get("content"), "处理中")

    def test_regression_no_tool(self):
        """
        场景 3: 正常无工具请求回归测试
        - 模拟模型直接返回文本回答，无 tool_calls
        - 验证正确返回模型回答
        - 验证 HTTP 请求次数为 1
        """
        fake_response = Mock()
        fake_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "你好，我可以帮助你查询订单。",
                        "tool_calls": None
                    }
                }
            ]
        }

        with patch(
            "agent.requests.post",
            return_value=fake_response
        ) as mock_post:
            result = run_agent("你好")

            self.assertEqual(result, "你好，我可以帮助你查询订单。")
            self.assertEqual(mock_post.call_count, 1)

    def test_regression_tool_calling(self):
        """
        场景 4: 正常 Tool Calling 回归测试
        - 首次请求返回 Tool Call (get_order_status A1002)
        - 本地成功执行工具
        - 第二次请求模型返回最终回答
        - 验证最终文本回答正确
        - 验证 HTTP 请求次数为 2
        - 验证工具消息正确传递给模型
        """
        first_response = Mock()
        first_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_test_001",
                                "type": "function",
                                "function": {
                                    "name": "get_order_status",
                                    "arguments": '{"order_id": "A1002"}'
                                }
                            }
                        ]
                    }
                }
            ]
        }

        final_response = Mock()
        final_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "订单 A1002 当前状态是处理中。",
                        "tool_calls": None
                    }
                }
            ]
        }

        with patch(
            "agent.requests.post",
            side_effect=[first_response, final_response]
        ) as mock_post:
            result = run_agent("查询订单 A1002 的状态")

            self.assertEqual(result, "订单 A1002 当前状态是处理中。")
            self.assertEqual(mock_post.call_count, 2)

            calls = mock_post.call_args_list
            messages = calls[1].kwargs["json"]["messages"]

            tool_messages = [
                msg for msg in messages
                if msg.get("role") == "tool"
                and msg.get("tool_call_id") == "call_test_001"
            ]
            self.assertEqual(len(tool_messages), 1)
            self.assertEqual(tool_messages[0]["content"], "处理中")


if __name__ == "__main__":
    unittest.main()
