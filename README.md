# Agent Tool Calling Project

## 项目简介

基于 Python + FastAPI 实现的最小 Tool Calling Agent 项目：

- **智能工具调用**：LLM 根据用户问题决定是否调用工具。
- **Tool Registry（工具注册表）**：根据工具名动态调用 Python 工具。
- **多轮决策循环**：把 Tool Result（工具结果）回填给模型继续决策，直到返回最终答案。
- **场景覆盖**：已覆盖 No Tool、Single Tool、Multi Tool、Conditional Tool 场景。
- **双重验证**：使用 Evaluation（评测）和 HTTP Smoke Test（冒烟测试）验证。

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

### 5. 运行 Agent Evaluation

```powershell
python .\eval_agent.py
```

当前 Evaluation 包含：

- No Tool
- Single Tool
- Multi Tool
- Conditional Tool

### 6. 启动 FastAPI 服务

```powershell
python -m uvicorn main:app --reload
```

默认服务地址：

```text
http://127.0.0.1:8000
```

保持这个终端运行。

### 7. 运行 HTTP Smoke Test

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