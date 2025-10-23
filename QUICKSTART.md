# ⚡ 快速开始 - 3分钟上手指南

## 🎯 两条启动路径

### 路径A: 🆓 完全免费 (推荐!)
使用 Ollama 本地模型,无需任何 API Key

### 路径B: 💳 OpenAI API
使用 OpenAI GPT 模型,需要 API Key

---

## 🆓 路径A: 免费Ollama路径 (推荐)

### 1️⃣ 安装依赖 (2分钟)

```powershell
cd c:\Github\AIAgentDemo
pip install -r requirements.txt
```

> 💡 如果速度慢,使用国内镜像:
> ```powershell
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 2️⃣ 安装 Ollama (5分钟)

```powershell
# 1. 下载 Ollama (Windows版)
# 访问: https://ollama.com/download/windows

# 2. 安装后,拉取推荐模型
ollama pull qwen2.5:7b
```

> 📖 详细指南: 查看 [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md)

### 3️⃣ 配置 (30秒)

```powershell
# 复制配置模板
copy .env.example .env

# 用记事本打开
notepad .env
```

在 `.env` 文件中设置:
```
LLM_TYPE=ollama
OLLAMA_MODEL=qwen2.5:7b
```

### 4️⃣ 启动应用 (30秒)

```powershell
# 启动智能客服
python main.py
```

**完全免费,本地运行!** 🎉

---

## 💳 路径B: OpenAI API路径

### 1️⃣ 安装依赖 (2分钟)

```powershell
cd c:\Github\AIAgentDemo
pip install -r requirements.txt
```

### 2️⃣ 配置API密钥 (30秒)

```powershell
# 复制配置模板
copy .env.example .env

# 用记事本打开并填入API Key
notepad .env
```

在 `.env` 文件中填写:
```
LLM_TYPE=openai
OPENAI_API_KEY=sk-your-actual-api-key-here
```

> 🔑 获取API Key: https://platform.openai.com/api-keys

### 3️⃣ 启动应用 (30秒)

```powershell
# 启动智能客服
python main.py
```

**OpenAI强大模型!** 🎉

---

## 💬 开始对话

启动后,直接输入问题:

```
👤 您: 考试时间多长?
🤖 助手: 考试总时长为90分钟...

👤 您: 需要会哪些技术?
🤖 助手: 主要需要掌握...

👤 您: quit
👋 感谢使用!
```

---

## 🆘 没有OpenAI API?

### 方案A: 先体验检索功能

```powershell
# 运行简化演示(无需API)
python demo_simple.py
```

这会展示RAG检索如何工作,但不包含LLM问答。

### 方案B: 免费获取API Key

1. 访问 https://platform.openai.com/signup
2. 注册免费账号(新用户有$5额度)
3. 创建API Key
4. 填入 `.env` 文件

---

## 🧪 验证安装

### 运行验证脚本

```powershell
python verify.py
```

看到以下信息表示成功:
```
✅ 项目结构完整
✅ 所有依赖已安装
🎉 验证通过! 项目已就绪.
```

### 运行完整测试

```powershell
python test.py
```

---

## 🎯 常用命令

### 应用运行
```powershell
python main.py              # 启动客服
python main.py --rebuild    # 重建向量库
python main.py --show-sources  # 显示来源
```

### 测试与验证
```powershell
python verify.py            # 验证环境
python test.py              # 运行测试
python demo_simple.py       # 简化演示
```

### 应用内命令
```
clear / 清空     - 清空对话历史
history / 历史   - 查看对话记录
quit / exit / 退出 - 退出程序
```

---

## ❓ 遇到问题?

### 常见问题快速解决

#### ❌ 依赖安装失败
```powershell
# 升级pip后重试
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### ❌ API调用失败
- 检查 `.env` 文件是否正确配置
- 确认API Key有效且有余额
- 检查网络能否访问OpenAI

#### ❌ 中文显示乱码
```powershell
# 设置PowerShell为UTF-8编码
chcp 65001
```

#### ❌ 向量库构建失败
```powershell
# 强制重建
python main.py --rebuild
```

---

## 📚 想了解更多?

- 📖 **完整文档** → [README.md](README.md)
- 🔧 **详细安装** → [INSTALL.md](INSTALL.md)
- 📊 **技术架构** → [OVERVIEW.md](OVERVIEW.md)
- 🎉 **项目总结** → [SUMMARY.md](SUMMARY.md)

---

## 🎓 示例对话

### 例1: 考试信息
```
👤: 考试包括哪些科目?
🤖: 招聘考试包含两个科目:
    1. 行政能力测验
    2. 专业知识
    总时长为90分钟。
```

### 例2: 技术要求
```
👤: Python和Java都要会吗?
🤖: 不需要。岗位要求是熟练使用Python/Java
    至少一种主流开发语言,掌握其中一种即可。
```

### 例3: 加分项
```
👤: 什么经验是加分项?
🤖: 以下项目经验者优先录用:
    - 大模型语料治理经验
    - 智能体编排经验
    - RAG规划经验
    - AI Agent项目管理经验
    ...
```

---

## ⏱️ 时间表

| 步骤 | 预计时间 | 说明 |
|-----|---------|------|
| 安装依赖 | 2分钟 | 首次需下载模型 |
| 配置API | 30秒 | 复制并填写Key |
| 启动应用 | 30秒 | 自动构建向量库 |
| **总计** | **3分钟** | **即可开始使用** |

---

## 🚀 立即开始

```powershell
# 一键复制执行
cd c:\Github\AIAgentDemo
pip install -r requirements.txt
copy .env.example .env
# [手动编辑.env填入API Key]
python main.py
```

**就是这么简单! 🎊**

---

_快速开始指南 | 上海大数据中心政务智能客服系统_
