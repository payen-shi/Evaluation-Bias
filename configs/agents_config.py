"""
----------------
agents_config.py
----------------
This module provides a centralized configuration for agent classes and their supported AI model platforms.
It imports model information and agent class definitions, then maps each agent type to its corresponding class and available platforms.
Each platform entry includes a usage count and model-specific information, enabling flexible agent instantiation and management.

Configuration structure:
- AGENTS_SETUP: Dictionary mapping agent roles to their class and supported platforms.

Agents included:
- Junior physician
- Mid-career physician
- Senior physician

Platforms supported:
- GPT_4O_MINI
- GPT_4O
- QWEN_TURBO
----------------
"""

from configs.API_INFO import *
from src.agent import *

# Centralized configuration for agents
# Change the number of agents for each platform by modifying the 'count' value in the AGENTS_SETUP dictionary.
AGENTS_SETUP = {
    'Junior': {
        'class': Junior,
        'platforms': {
            'GPT_4O_MINI': {'count': 0, 'model_info': GPT_4O_MINI_Model_Info},
            'GPT_4O': {'count': 0, 'model_info': GPT_4O_Model_Info},
            'QWEN_TURBO': {'count': 0, 'model_info': QWEN_TURBO_Model_Info},
        }
    },
    'Mid': {
        'class': Mid,
        'platforms': {
            'GPT_4O_MINI': {'count': 0, 'model_info': GPT_4O_MINI_Model_Info},
            'GPT_4O': {'count': 0, 'model_info': GPT_4O_Model_Info},
            'QWEN_TURBO': {'count': 0, 'model_info': QWEN_TURBO_Model_Info},
        }
    },
    'Senior': {
        'class': Senior,
        'platforms': {
            'GPT_4O_MINI': {'count': 0, 'model_info': GPT_4O_MINI_Model_Info},
            'GPT_4O': {'count': 0, 'model_info': GPT_4O_Model_Info},
            'QWEN_TURBO': {'count': 0, 'model_info': QWEN_TURBO_Model_Info},
        }
    }
}