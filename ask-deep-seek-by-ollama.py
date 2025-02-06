import requests

local_ollama_api_url = 'http://localhost:11434/api/chat'

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'messages': [
        {
            'content': 'You are a helpful assistant',
            'role': 'system',
        },
        {
            'content': '9.11 and 9.8, which is greater?',
            'role': 'user',
        },
    ],
    # using deepseek-r1:7b on local ollama server
    # ref https://ollama.com/library/deepseek-r1:7b
    'model': 'deepseek-r1:latest',
    'frequency_penalty': 0,
    'max_tokens': 2048,
    'presence_penalty': 0,
    'response_format': {
        'type': 'text',
    },
    'stop': None,
    'stream': False,
    'stream_options': None,
    'temperature': 1,
    'top_p': 1,
    'tools': None,
    'tool_choice': 'none',
    'logprobs': False,
    'top_logprobs': None,
}
response = requests.post(local_ollama_api_url, headers=headers, json=json_data)

json = response.json()
'''
<think>
think 标签之间的内容代表推理内容，注意该部分内容有可能为空。
</think>
'''
print(json['message']['content'])
