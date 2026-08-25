import os
from dotenv import load_dotenv
import openai
import requests

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("MODELSCOPE_ACCESS_TOKEN"),
    base_url="https://api-inference.modelscope.cn/v1/"
)

# 目标 arXiv HTML 页面
url = "http://arxiv.org/html/2509.21243v1"

# 抓取 HTML 原文
resp = requests.get(url, timeout=30)
resp.raise_for_status()
html_content = resp.text

# 可选：为了避免超长输入导致超出上下文长度，这里做一个简单截断（按需调整）
max_chars = 180000
if len(html_content) > max_chars:
    html_content = html_content[:max_chars]

response = client.chat.completions.create(
    model='Qwen/Qwen3-Next-80B-A3B-Instruct',
    messages=[
        {
            'role': 'system',
            'content': '你是一名论文阅读专家。根据提供的Arxiv论文HTML原文，总结论文的要点，不需要输出其他内容。'
        },
        {
            'role': 'user',
            'content': f"以下为论文的HTML原文（可能已截断）：\n\n{html_content}"
        }
    ],
    stream=True
)

for chunk in response:
    delta = chunk.choices[0].delta
    if delta and delta.content:
        print(delta.content, end='', flush=True)