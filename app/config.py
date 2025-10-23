"""
配置文件
Configuration settings for the Government AI Assistant
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI配置
OPENAI_API_KEY = ''
QW_API_KEY = os.getenv("QW_API_KEY", "")

QW_Model = os.getenv("QW_Model", "qwen2.5-14b-instruct-1m")
QW_API_BASE_URL = os.getenv("QW_API_BASE_URL", "")
# 模型配置
# 支持的模型类型: "openai", "ollama", "fake"
LLM_TYPE = os.getenv("LLM_TYPE", "auto")  # auto 自动选择
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")  # OpenAI模型
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")  # Ollama本地模型
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")  # Ollama服务地址
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY','') #Ollama 云模型

# 向量数据库配置
# 使用更简单的模型名称(自动从Hugging Face下载)
# 备选模型: "all-MiniLM-L6-v2" (英文), "paraphrase-multilingual-MiniLM-L12-v2" (多语言)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 轻量级英文模型,下载更快
# 如果需要中文支持,改为: "paraphrase-multilingual-MiniLM-L12-v2"
VECTOR_STORE_PATH = "data/vector_store"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# RAG配置
TOP_K_RESULTS = 3
SCORE_THRESHOLD = 0.5

# 知识库文件路径
KNOWLEDGE_BASE_PATH = "data"

# 系统提示词
SYSTEM_PROMPT = """你是一个个人智能助手信息。你的职责是帮助应提问者提供最准确的信息。

请注意:
1. 回答问题时要准确、专业、友好
2. 基于提供的知识库内容回答问题
3. 如果问题超出知识库范围,请礼貌地告知用户
4. 使用清晰的中文表达

你的回答应该:
- 简洁明了,避免冗长
- 突出重点信息
- 必要时提供结构化的列表或步骤
- 保持专业和礼貌的语气
"""
