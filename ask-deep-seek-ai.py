from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

'''
DeepSeek 官方最近遭受攻击，API 请求可能存在缓慢无响应等异常。
建议使用硅基流动托管的 DeepSeek 服务，走下面链接注册，本人能收到硅基流动赠金。
https://cloud.siliconflow.cn/i/c43wkWpu
感谢支持！
'''
api_config = {
    'official_provider': {
        # ak 请到各自平台申请，根据实际填写
        'api_key': os.getenv('DEEPSEEK_API_KEY', ''),
        'base_url': 'https://api.deepseek.com',
        'model': 'deepseek-reasoner',
    },
    'silicon_flow_provider': {
        # ak 请到各自平台申请，根据实际填写
        'api_key': os.getenv('SILICON_FLOW_API_KEY', ''),
        'base_url': 'https://api.siliconflow.cn/v1',
        # 70B (收费 ￥4.13/M Tokens) deepseek-ai/DeepSeek-R1-Distill-Llama-70B
        # 14B (收费 ￥0.7/M Tokens) deepseek-ai/DeepSeek-R1-Distill-Qwen-14B
        # 8B 免费 deepseek-ai/DeepSeek-R1-Distill-Llama-8B
        'model': 'deepseek-ai/DeepSeek-R1-Distill-Llama-8B',
        # 'model': 'deepseek-ai/DeepSeek-R1-Distill-Llama-70B',
    }
}
using_official = False
if using_official:
    client = OpenAI(api_key=api_config['official_provider']['api_key'],
                    base_url=api_config['official_provider']['base_url'])
    model = api_config['official_provider']['model']
else:
    client = OpenAI(api_key=api_config['silicon_flow_provider']['api_key'],
                    base_url=api_config['silicon_flow_provider']['base_url'])
    model = api_config['silicon_flow_provider']['model']

# Round 1
messages = [
    {
        'content': 'You are a helpful assistant',
        'role': 'system'
    },
    {
        # 'content': '9.11 and 9.8, which is greater?',
        # 8B 免费版一本正经的胡说八道，切换为 14B 则准确多了
        'content': '鲁迅为啥暴打周树人？',
        'role': 'user'
    }
]
# temperature 与 top_p 修改其一即可，不要都修改
response = client.chat.completions.create(
    model=model,
    messages=messages,
    # temperature=0.7,
    top_p=0.8,
    stream=False,
    timeout=1200
)

reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

print('<think>')
print(reasoning_content)
print('</think>')
print('-----')
print(content)

"""
# Round 2
messages.append({'role': 'assistant', 'content': content})
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model=model,
    messages=messages,
    # temperature=0.7,
    top_p=0.8,
    stream=False,
    timeout=120
)
# ...
"""
