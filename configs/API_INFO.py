"""
----------------
API_INFO.py
----------------
This module defines API endpoint URLs, keys, and model information classes for accessing various AI model platforms (OpenAI, Aliyun/Qwen).
----------------
"""

from camel.types import ModelPlatformType, ModelType

OPENAI_API_BASE_URL = 'https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
OPENAI_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

ALIYUN_API_BASE_URL = 'https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ALIYUN_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


class Base_Model_Info:
    PLATFORM = None
    TYPE = None
    API_KEY = None
    API_BASE_URL = None
    
class GPT_4O_MINI_Model_Info(Base_Model_Info):
    PLATFORM = ModelPlatformType.OPENAI
    TYPE = ModelType.GPT_4O_MINI
    API_KEY = OPENAI_API_KEY
    API_BASE_URL = OPENAI_API_BASE_URL
    
class GPT_4O_Model_Info(Base_Model_Info):
    PLATFORM = ModelPlatformType.OPENAI
    TYPE = ModelType.GPT_4O
    API_KEY = OPENAI_API_KEY
    API_BASE_URL = OPENAI_API_BASE_URL
    
class QWEN_TURBO_Model_Info(Base_Model_Info):
    PLATFORM = ModelPlatformType.QWEN
    TYPE = ModelType.QWEN_TURBO
    API_KEY = ALIYUN_API_KEY
    API_BASE_URL = ALIYUN_API_BASE_URL