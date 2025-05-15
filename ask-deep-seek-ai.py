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
    },
    'ctyun_provider': {
        'api_key': os.getenv('CTYUN_API_KEY', ''),
        'base_url': 'https://wishub-x1.ctyun.cn/v1',
        'model': '4bd107bff85941239e27b1509eccfe98'
    },
    "tencent_provider": {
        'api_key': os.getenv('TENCENT_API_KEY', ''),
        'base_url': 'https://api.lkeap.cloud.tencent.com/v1',
        # deepseek-v3|deepseek-r1
        'model': 'deepseek-r1'
    }
}

ctyun_model_maps = {
    '4bd107bff85941239e27b1509eccfe98': 'DeepSeek-R1-昇腾版',
    '7ba7726dad4c4ea4ab7f39c7741aea68': 'DeepSeek-R1-英伟达版',
    '9dc913a037774fc0b248376905c85da5': 'DeepSeek-V3-昇腾版',
    '515fdba33cc84aa799bbd44b6e00660d': 'DeepSeek-R1-Distill-Llama-70B',
    'b383c1eecf2c4b30b4bcca7f019cf90d': 'DeepSeek-R1-Distill-Qwen-32B',
    '0855b510473e4ec3a029569853f64974': 'DeepSeek-V2-Lite-Chat',
    'f23651e4a8904ea589a6372e0e860b10': 'DeepSeek-Coder-V2-Lite-Instruct'
}
provider_maps = {
    1: 'official_provider',
    2: 'silicon_flow_provider',
    3: 'ctyun_provider',
    4: 'tencent_provider',
}
# 根据序号切换不同 DeepSeek 供应商
using_provider = 4
provider_config = api_config[provider_maps[using_provider]]

client = OpenAI(api_key=provider_config['api_key'],
                base_url=provider_config['base_url'])
model = provider_config['model']


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

reasoning_content = None
if hasattr(response.choices[0].message, 'reasoning_content'):
    reasoning_content = response.choices[0].message.reasoning_content


content = response.choices[0].message.content

if reasoning_content:
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
