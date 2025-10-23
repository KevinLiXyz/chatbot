# 🔧 模型下载问题解决方案

## ❌ 问题描述

错误信息:
```
Can't load the model for 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
```

这是因为嵌入模型需要从 Hugging Face 下载,首次使用时会自动下载。

---

## ✅ 解决方案

### 方案 1: 使用自动下载助手(推荐)

运行模型下载助手:

```powershell
python download_model.py
```

选择模型:
- **选项 1**: `all-MiniLM-L6-v2` (英文,80MB,快速) ✅ **推荐先试这个**
- **选项 2**: `paraphrase-multilingual-MiniLM-L12-v2` (多语言,420MB)
- **选项 3**: `distiluse-base-multilingual-cased-v2` (多语言,500MB)

### 方案 2: 手动修改配置使用英文模型

英文模型更小更快,虽然知识库是中文,但仍然可以工作:

1. 打开 `app/config.py`
2. 找到 `EMBEDDING_MODEL` 这一行
3. 确认已设置为: `EMBEDDING_MODEL = "all-MiniLM-L6-v2"`

这个模型已经在配置中设置好了!

### 方案 3: 使用中文多语言模型(需要更多时间下载)

如果需要更好的中文支持:

1. 编辑 `app/config.py`
2. 修改为:
   ```python
   EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
   ```

3. 运行下载助手:
   ```powershell
   python download_model.py
   # 选择选项 2
   ```

---

## 🚀 快速启动步骤

### 步骤 1: 下载模型

```powershell
# 使用英文模型(快速,推荐)
python download_model.py
# 输入: 1
```

### 步骤 2: 配置API Key

```powershell
copy .env.example .env
notepad .env
# 填入: OPENAI_API_KEY=sk-your-key
```

### 步骤 3: 启动应用

```powershell
python main.py
```

---

## 🌐 网络问题解决

### 问题: 无法访问 huggingface.co

#### 解决方案 A: 使用镜像站点

设置环境变量使用镜像:

```powershell
# 使用Hugging Face镜像
$env:HF_ENDPOINT="https://hf-mirror.com"
python download_model.py
```

#### 解决方案 B: 配置代理

如果有代理:

```powershell
$env:HTTP_PROXY="http://your-proxy:port"
$env:HTTPS_PROXY="http://your-proxy:port"
python download_model.py
```

#### 解决方案 C: 手动下载模型

1. 访问模型页面(可能需要科学上网):
   - 英文模型: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
   - 多语言: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

2. 下载所有文件到本地目录:
   ```
   models/
   └── all-MiniLM-L6-v2/
       ├── config.json
       ├── pytorch_model.bin
       ├── tokenizer_config.json
       ├── vocab.txt
       └── ...
   ```

3. 修改 `app/config.py`:
   ```python
   EMBEDDING_MODEL = "./models/all-MiniLM-L6-v2"
   ```

---

## 📊 模型对比

| 模型 | 大小 | 语言 | 下载时间 | 推荐场景 |
|------|------|------|---------|---------|
| all-MiniLM-L6-v2 | 80MB | 英文 | 1-2分钟 | ✅ 快速测试 |
| paraphrase-multilingual-MiniLM-L12-v2 | 420MB | 多语言 | 5-10分钟 | 中文支持 |
| distiluse-base-multilingual-cased-v2 | 500MB | 多语言 | 10-15分钟 | 高质量 |

**建议**: 先用英文模型快速测试,确认系统运行正常后,如需要再切换到多语言模型。

---

## 🧪 测试模型是否下载成功

运行测试脚本:

```powershell
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); print('✅ 模型加载成功!')"
```

---

## ⚡ 快速解决方案(针对当前错误)

**当前配置已更新为使用英文模型 `all-MiniLM-L6-v2`**

直接运行:

```powershell
# 方式1: 使用下载助手
python download_model.py

# 方式2: 直接启动(会自动下载)
python main.py
```

首次运行会自动下载模型(约1-2分钟),之后就不需要了。

---

## 💡 常见问题

### Q1: 为什么要下载模型?

A: Sentence Transformers 需要预训练的神经网络模型来将文本转换为向量。这些模型存储在 Hugging Face 上。

### Q2: 模型存储在哪里?

A: Windows默认路径:
```
C:\Users\你的用户名\.cache\torch\sentence_transformers\
```

### Q3: 可以离线使用吗?

A: 可以! 模型下载后会缓存在本地,之后无需网络。

### Q4: 英文模型能处理中文吗?

A: 可以部分工作,但效果不如多语言模型。对于招聘知识库,英文模型也能产生可用的检索结果。

### Q5: 下载失败怎么办?

A: 
1. 检查网络连接
2. 尝试使用镜像站点
3. 使用更小的模型
4. 手动下载后指定本地路径

---

## 🎯 推荐操作流程

```powershell
# 1. 确保依赖已安装
python verify.py

# 2. 下载嵌入模型(选择1)
python download_model.py

# 3. 配置API Key
copy .env.example .env
notepad .env

# 4. 启动应用
python main.py
```

---

**如果仍有问题,请查看终端的详细错误信息,或尝试上述不同的解决方案。**

_更新时间: 2025-10-16_
