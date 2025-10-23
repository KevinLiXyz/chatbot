# 上海事业单位 - 政务智能客服系统

基于 **Python + LangChain + RAG** 技术栈构建的政务招聘智能客服应用。

## 🎯 项目简介

本项目是一个智能客服应用,专门用于回答上海事业单位招聘相关的问题。系统采用 **检索增强生成(RAG)** 技术,结合大语言模型(LLM),为应聘者提供准确、专业的咨询服务。

### 核心技术栈

- **Python 3.8+** - 主要开发语言
- **LangChain** - LLM应用开发框架
- **多种LLM支持** - OpenAI GPT / Ollama本地模型 / 测试模式
- **FAISS** - 向量数据库(用于相似度检索)
- **Sentence-Transformers** - 多语言文本嵌入模型
- **RAG架构** - 检索增强生成

### 主要功能

✅ 基于招聘知识库的智能问答  
✅ 支持多轮对话和上下文理解  
✅ 精准的语义检索和答案生成  
✅ 友好的命令行交互界面  
✅ 对话历史管理功能  
🆓 **支持完全免费的本地大语言模型 (Ollama)**  

## 📁 项目结构

```
AIAgentDemo/
├── app/                          # 应用核心代码
│   ├── __init__.py              # 包初始化
│   ├── config.py                # 配置文件
│   ├── rag.py                   # RAG检索模块
│   └── chatbot.py               # 聊天机器人核心
├── data/                         # 数据目录
│   ├── recruitment_knowledge.md # 招聘知识库
│   └── vector_store/            # 向量数据库(自动生成)
├── main.py                       # CLI主程序入口
├── test.py                       # 测试脚本
├── requirements.txt              # Python依赖
├── .env.example                  # 环境变量示例
└── README.md                     # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

**系统要求:**
- Python 3.8 或更高版本
- 至少 2GB 可用内存
- 稳定的网络连接(用于下载模型和调用API)

### 2. 安装依赖

```powershell
# 克隆或进入项目目录
cd c:\Github\AIAgentDemo

# 安装Python依赖包
pip install -r requirements.txt
```

### 3. 配置大语言模型 (选择一种方式)

#### 🆓 方式A: 使用免费本地模型 Ollama (推荐)

**无需API Key,完全免费!**

```powershell
# 1. 安装 Ollama
# 访问 https://ollama.ai/download 下载安装

# 2. 下载中文模型 (约4.7GB)
ollama pull qwen2.5:7b

# 3. 配置 .env
copy .env.example .env
# 编辑 .env,设置: LLM_TYPE=ollama
```

**详细指南**: 查看 [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md)

#### 💰 方式B: 使用 OpenAI GPT (需要API Key)

```powershell
# 复制环境变量示例文件
copy .env.example .env

# 编辑.env文件,填入你的OpenAI API Key
# OPENAI_API_KEY=sk-your-api-key-here
```

**获取OpenAI API Key:**
1. 访问 https://platform.openai.com/api-keys
2. 注册/登录OpenAI账号
3. 创建新的API密钥
4. 将密钥粘贴到`.env`文件中

#### 🔄 方式C: 自动模式 (智能切换)

```bash
# .env 文件
LLM_TYPE=auto  # 有OpenAI Key用OpenAI,否则用Ollama
OPENAI_API_KEY=sk-xxx  # 可选
OLLAMA_MODEL=qwen2.5:7b
```

### 4. 运行应用

```powershell
# 首次运行(会自动构建向量数据库)
python main.py

# 显示来源文档(调试模式)
python main.py --show-sources

# 强制重建向量数据库
python main.py --rebuild
```

## 💬 使用示例

启动程序后,您可以直接输入问题:

```
👤 您: 考试时间是多久?
🤖 助手: 考试总时长为90分钟,包含行政能力测验和专业知识两个科目...

👤 您: 需要掌握哪些技术?
🤖 助手: 主要技术要求包括:
1. 掌握各种主流LLM模型技术...
2. 熟练使用Python/Java至少一种语言...
...

👤 您: Python和Java都要会吗?
🤖 助手: 不需要。岗位要求是熟练使用Python/Java至少一种主流开发语言...
```

### 特殊命令

- `clear` / `清空` - 清空对话历史
- `history` / `历史` - 查看对话记录
- `quit` / `exit` / `退出` - 退出程序

## 🧪 运行测试

```powershell
# 运行完整测试套件
python test.py
```

测试将验证:
1. ✅ RAG系统初始化
2. ✅ 文档检索功能
3. ✅ 聊天机器人对话

## ⚙️ 配置说明

在 `app/config.py` 中可以调整以下参数:

```python
# LLM模型选择
LLM_MODEL = "gpt-3.5-turbo"  # 或 "gpt-4"

# 温度参数(创造性)
TEMPERATURE = 0.7  # 0.0-1.0,越高越随机

# 检索参数
TOP_K_RESULTS = 3  # 检索Top-K个文档
CHUNK_SIZE = 500   # 文本块大小
```

## 🏗️ 技术架构

### RAG工作流程

```
用户问题 → 文本嵌入 → 向量检索 → 相关文档
                              ↓
                     拼接上下文 + 问题
                              ↓
                        LLM生成答案
                              ↓
                         返回用户
```

### 核心模块说明

#### 1. RAG检索器 (`app/rag.py`)
- 加载和分割知识库文档
- 使用多语言嵌入模型生成向量
- FAISS向量数据库构建和检索
- 支持相似度搜索和Top-K检索

#### 2. 聊天机器人 (`app/chatbot.py`)
- 集成LangChain对话链
- 对话历史管理(Memory)
- 自定义系统提示词
- 上下文感知的回答生成

#### 3. CLI界面 (`main.py`)
- 友好的命令行交互
- 实时流式输出
- 特殊命令处理
- 异常处理和错误提示

## 📚 知识库说明

知识库文件位于 `data/recruitment_knowledge.md`,包含:

- 考试信息(科目、时间)
- 岗位技术要求(LLM、编程、AI工程)
- 综合能力要求(学习、沟通、协作)
- 优先条件(RAG、Agent、项目经验)
- 常见问题解答(Q&A)

**自定义知识库:**
您可以直接编辑此文件来更新知识内容,然后使用 `--rebuild` 参数重建向量数据库:

```powershell
python main.py --rebuild
```

## 🔧 常见问题

### Q1: 安装依赖时报错?

**A:** 确保使用Python 3.8+,并升级pip:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Q2: 向量数据库构建失败?

**A:** 可能是网络问题导致模型下载失败。解决方案:
1. 检查网络连接
2. 使用代理或更换网络
3. 手动下载模型到缓存目录

### Q3: OpenAI API调用失败?

**A:** 检查以下事项:
- API Key是否正确配置在`.env`文件
- API Key是否有效且有额度
- 网络是否能访问OpenAI服务
- 是否需要配置代理

### Q4: 回答不准确或偏离主题?

**A:** 尝试以下优化:
- 调整 `TEMPERATURE` 参数(降低更稳定)
- 增加 `TOP_K_RESULTS` 获取更多上下文
- 优化知识库内容的组织结构
- 改进系统提示词 `SYSTEM_PROMPT`

## 🎓 扩展开发

### 添加新的知识内容

1. 编辑 `data/recruitment_knowledge.md`
2. 添加新的章节或Q&A
3. 运行 `python main.py --rebuild` 重建索引

### 更换嵌入模型

在 `app/config.py` 中修改:
```python
EMBEDDING_MODEL = "your-preferred-model"
```

推荐中文模型:
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- `shibing624/text2vec-base-chinese`

### 集成其他LLM

修改 `app/chatbot.py` 中的 `_initialize_llm` 方法,支持:
- Azure OpenAI
- 文心一言
- 通义千问
- 本地部署的开源模型

## 📝 许可证

本项目仅用于学习和技术展示目的。

## 👥 贡献

欢迎提交Issue和Pull Request!

## 📞 联系方式

如有问题,请通过GitHub Issues联系。

---

**祝您应聘顺利! 🎉**
