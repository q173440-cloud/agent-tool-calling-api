import os
import requests
import json


api_key = os.getenv("LLM_API_KEY")
url = os.getenv("LLM_API_URL")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


orders = [
    ["A1001", "已发货"],
    ["A1002", "处理中"],
    ["A1003", "已完成"]
]

product_stocks = [
    ["P001", 12],
    ["P002", 0],
    ["P003", 5]
]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product_stock",
            "description": "根据商品编号查询商品库存数量，如果商品不存在，返回没有找到。",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "商品的编号，例如 P001"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "根据订单编号查询订单状态。",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "订单编号，例如 A1001"
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]


def chuan(question):
    messages = [
        {
            "role": "user",
            "content": question
        }
    ]
    return messages


def get_order_status(order_id):
    for order in orders:
        if order[0] == order_id:
            return order[1]

    return "不存在编号"


def get_product_stock(product_id):
    for product in product_stocks:
        if product[0] == product_id:
            return product[1]

    return "没有找到"


tool_registry = {
    "get_product_stock": get_product_stock,
    "get_order_status": get_order_status
}


max_steps = 5


def run_agent(question):

    messages = chuan(question)

    step_count = 0

    data = {
        "model": "gemini-3.8-flash-high",
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )


    result = response.json()


    tool_calls = result["choices"][0]["message"].get("tool_calls")

    while True:


        if not tool_calls:
            final_answer = result["choices"][0]["message"]["content"]
            return final_answer

        if step_count >= max_steps:
            return "任务轮数已达上限，停止执行"


        step_count += 1

        print("step_count:", step_count)

        tool_call = tool_calls[0]


        tool_call_id = tool_call["id"]


        tool_name = tool_call["function"]["name"]


        arguments = json.loads(
            tool_call["function"]["arguments"]
        )

        tool_function = tool_registry[tool_name]


        tool_result = tool_function(**arguments)

        print("tool_name:", tool_name)
        print("tool_function:", tool_function)
        print("tool_result:", tool_result)

        assistant_message = {
            "role": "assistant",
            "content": None,
            "tool_calls": tool_calls
        }

        messages.append(assistant_message)

        tool_message = {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": str(tool_result)
        }

        messages.append(tool_message)

        data = {
            "model": "gemini-3.8-flash-high",
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto"
        }

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        result = response.json()

        tool_calls = result["choices"][0]["message"].get("tool_calls")
