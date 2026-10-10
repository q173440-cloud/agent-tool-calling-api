# Agent Tool Calling Project

## 项目简介

基于 Python + FastAPI 实现的最小 Tool Calling Agent（工具调用智能体）项目：

- **智能工具调用（LLM Tool Calling）**：LLM 根据用户问题自主决定是否调用工具，支持无需调用工具的直接回答（No Tool 分支）。
- **工具注册与动态分发（Tool Registry + Dynamic Dispatch）**：统一维护本地工具映射，根据模型返回的函数名动态调用对应的 Python 工具。
- **最小智能体循环（Minimal Agent Loop）**：维护对话历史，按标准消息协议回填助手消息与工具结果，持续迭代直至任务完成。
- **单/多工具调用支持（Single & Multi Tool Calling）**：支持单工具调用与同轮多工具调用。Agent supports executing multiple tool calls returned in the same model turn and feeds each result back using the corresponding tool_call_id（支持在同一模型轮次中逐个执行返回的多个工具调用，并使用对应的 `tool_call_id` 将各工具结果独立封装并回填）。
- **结构化工具返回**：商品库存工具 `get_product_stock` 支持返回结构化字典，包含库存数量（`stock`）与库存状态（`stock_status`：`out_of_stock` / `low_stock` / `in_stock`）。
- **Web API 服务与输入校验**：基于 FastAPI 提供 HTTP 接口（包含 `/health` 与 `/ask`）。`/ask` 接口自动去除 `question` 首尾空格；空问题（包括全空格输入）在进入 Agent 前直接拒绝并返回提示；`model` 为可选参数，不传时使用默认模型，原有仅传 `question` 的请求格式保持兼容；正常问题继续保持原有 Agent / Tool Calling 流程。
- **评测与回归（Evaluation / Regression）**：结合自动化用例评测（`eval_agent.py`）与 HTTP Smoke Test（冒烟测试）双重验证。
- **HTTP 超时保护（Timeout Handling）**：在首轮模型请求与后续 Agent Loop 工具调用请求中统一配置超时保护（`timeout=10`）与异常降级，保障服务可用性。

## Quickstart

### 1. 创建虚拟环境

```powershell
py -3.13 -m venv .venv
```

### 2. 激活虚拟环境

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. 安装项目依赖

```powershell
python -m pip install -r requirements.txt
```

### 4. 设置环境变量

项目需要配置以下环境变量：

- `LLM_API_KEY`：API 密钥
- `LLM_API_URL`：OpenAI-compatible LLM API 请求地址

PowerShell 中设置：

```powershell
$env:LLM_API_KEY="你的API密钥"
$env:LLM_API_URL="你的API地址"
```

不要把真实 API Key 写入项目文件或提交到 GitHub。

### 5. 运行单元与回归测试（Mock，无需真实 API Key）

项目内置基于 `unittest` 与 `unittest.mock` 的单测套件，可直接离线运行验证超时与核心行为：

```powershell
python -m unittest discover -s tests
```

测试包含：
- 场景 1：首次 LLM 请求超时捕获与降级
- 场景 2：Tool Calling 后续轮次请求超时捕获与降级
- 场景 3：正常无工具请求回归验证
- 场景 4：正常 Tool Calling 工具执行与回填回归验证

### 6. 运行 Agent Evaluation

```powershell
python .\eval_agent.py
```

当前 Evaluation 包含：

- No Tool
- Single Tool
- Multi Tool
- Conditional Tool

### 7. 启动 FastAPI 服务

```powershell
python -m uvicorn main:app --reload
```

默认服务地址：

```text
http://127.0.0.1:8000
```

保持这个终端运行。

### 8. 运行 HTTP Smoke Test

打开另一个 PowerShell，进入项目目录并激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

然后运行：

```powershell
python .\smoke_api.py
```

Smoke Test 会验证：

- `/health` 正常返回 `200`
- `/ask` 正常请求返回 `200`
- 缺少 `question` 的非法请求返回 `422`