# 专线产品意图识别服务


本服务支持并发调用
底层驱动大模型为vllm框架启动的 qwen1.5-32b-int4大语言模型


## 服务启动命令
```python
python pipeline_asyn.py
```


## 服务调用命令


要使用 `curl` 命令并确保发送的请求包含 UTF-8 编码，可以指定 `Content-Type` 头中包含字符集信息。以下是带有 UTF-8 编码的 `curl` 命令：

```bash
curl -X POST "http://localhost:8000/process_request/" -H "Content-Type: application/json; charset=utf-8" -d '{"content": "互联网专线资费信息"}'
```

### Breakdown:
1. `curl`: 命令行工具，用于在命令行或脚本中进行网络请求。
2. `-X POST`: 指定 HTTP 请求方法为 `POST`。
3. `"http://localhost:8000/process_request/"`: 目标 URL。
4. `-H "Content-Type: application/json; charset=utf-8"`: 设置请求头，指定请求体的内容类型为 `application/json`，并包含字符集信息 `charset=utf-8`，确保使用 UTF-8 编码。
5. `-d '{"content": "互联网专线资费信息"}'`: 指定请求的正文数据，包含 JSON 格式的数据 `{"content": "互联网专线资费信息"}`。

这个命令将向本地服务器的 `/process_request/` 端点发送一个 `POST` 请求，内容类型为 `application/json` 并使用 UTF-8 编码，请求体包含一个 JSON 对象 `{"content": "互联网专线资费信息"}`。



```powershell
$jsonPayload = '{"content": "互联网专线资费信息"}'
$bytes = [System.Text.Encoding]::UTF8.GetBytes($jsonPayload)
$encodedJsonPayload = [System.Text.Encoding]::UTF8.GetString($bytes)

Invoke-WebRequest -Uri "http://localhost:8000/process_request/" -Method POST -ContentType "application/json; charset=utf-8" -Body $encodedJsonPayload
```

### Breakdown:
- `$jsonPayload`：定义 JSON 负载。
- `$bytes`：将 JSON 负载转换为 UTF-8 字节数组。
- `$encodedJsonPayload`：将字节数组转换回字符串，确保使用 UTF-8 编码。
- `Invoke-WebRequest`：调用 API，指定 `Content-Type` 为 `application/json; charset=utf-8`。

