# 🚀 快速安装指南

本文档帮助您快速设置和运行政务智能客服系统。

---

## 📋 安装步骤

### 步骤 1: 检查Python版本

确保已安装 Python 3.8 或更高版本:

```powershell
python --version
```

如果未安装,请访问 https://www.python.org/downloads/ 下载安装。

---

### 步骤 2: 安装依赖包

在项目根目录运行:

```powershell
pip install -r requirements.txt
```

**注意:** 首次安装会下载模型文件(约200MB),需要等待几分钟。

如果安装速度慢,可以使用国内镜像:

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 步骤 3: 配置API密钥

#### 3.1 创建 .env 文件

```powershell
copy .env.example .env
```

#### 3.2 获取OpenAI API Key

1. 访问 https://platform.openai.com/api-keys
2. 登录或注册账号
3. 点击 "Create new secret key"
4. 复制生成的密钥

#### 3.3 编辑 .env 文件

用文本编辑器打开 `.env` 文件,填入你的API Key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

---

### 步骤 4: 验证安装

运行验证脚本检查是否一切就绪:

```powershell
python verify.py
```

如果看到 "✅ 验证通过! 项目已就绪." 表示安装成功。

---

## 🎯 运行应用

### 方式 1: 完整版智能客服 (需要OpenAI API)

```powershell
python main.py
```

启动后,您可以:
- 输入任何关于招聘的问题
- 系统会基于知识库给出智能回答
- 支持多轮对话

**示例对话:**
```
👤 您: 考试需要多长时间?
🤖 助手: 考试总时长为90分钟,包含行政能力测验和专业知识两个科目...
```

### 方式 2: 简化演示版 (无需OpenAI API)

如果您还没有OpenAI API Key,可以先运行简化版:

```powershell
python demo_simple.py
```

这个版本只展示RAG检索功能,不需要API Key。

### 方式 3: 运行测试

验证所有功能是否正常:

```powershell
python test.py
```

---

## 🔧 常见问题

### ❌ 问题 1: pip install 报错

**解决方案:**
```powershell
# 升级pip
python -m pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

---

### ❌ 问题 2: 模型下载失败

**错误信息:** "ConnectionError" 或 "Timeout"

**解决方案:**
- 检查网络连接
- 使用科学上网工具
- 或手动下载模型(见下方说明)

**手动下载模型:**
```powershell
# 下载中文嵌入模型
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"
```

---

### ❌ 问题 3: OpenAI API调用失败

**错误信息:** "AuthenticationError" 或 "RateLimitError"

**可能原因:**
1. API Key未正确配置
2. API Key已失效
3. 账户余额不足
4. 网络无法访问OpenAI服务

**解决方案:**
- 检查 `.env` 文件中的API Key
- 登录OpenAI官网检查账户状态
- 配置网络代理

---

### ❌ 问题 4: 向量数据库构建失败

**解决方案:**
```powershell
# 强制重建向量数据库
python main.py --rebuild
```

---

### ❌ 问题 5: 中文显示乱码

**Windows PowerShell解决方案:**
```powershell
# 设置编码为UTF-8
chcp 65001
```

---

## 📞 获取帮助

### 命令行帮助

```powershell
# 查看所有可用选项
python main.py --help
```

### 检查项目结构

```powershell
python verify.py
```

### 运行调试模式

```powershell
# 显示检索到的来源文档
python main.py --show-sources
```

---

## 🎓 下一步

安装完成后,建议:

1. **阅读 README.md** - 了解项目详细介绍
2. **运行 demo_simple.py** - 快速体验RAG检索
3. **运行 test.py** - 验证所有功能
4. **运行 main.py** - 开始使用完整客服系统
5. **自定义知识库** - 编辑 `data/recruitment_knowledge.md`

---

## 📊 系统要求

| 项目 | 要求 |
|------|------|
| Python版本 | 3.8+ |
| 内存 | 建议 4GB+ |
| 硬盘空间 | 500MB+ (用于模型) |
| 网络 | 需要访问OpenAI API |

---

**祝您使用愉快! 🎉**

如有问题,请查看 [README.md](README.md) 或提交 Issue。
