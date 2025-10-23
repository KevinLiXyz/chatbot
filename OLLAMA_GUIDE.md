# 🆓 使用免费本地大语言模型 - Ollama 指南

## 🎯 概述

本项目现在支持**完全免费的本地大语言模型**! 无需OpenAI API Key,可以在本地运行。

### 支持的LLM方式

| 方式 | 费用 | 优点 | 缺点 |
|------|------|------|------|
| **OpenAI GPT** | 💰 付费 | 质量最高,响应快 | 需要API Key和网络 |
| **Ollama本地** | 🆓 免费 | 完全免费,隐私保护 | 需要下载模型(几GB) |
| **测试模式** | 🆓 免费 | 无需配置 | 仅固定回答,无智能 |

---

## 🚀 快速开始 - Ollama本地模型

### 步骤 1: 安装 Ollama

#### Windows 系统

1. 访问 https://ollama.ai/download
2. 下载 Windows 安装包
3. 双击安装

或使用命令行:
```powershell
# 使用 winget 安装
winget install Ollama.Ollama
```

#### 验证安装

```powershell
ollama --version
```

应该看到版本号,如: `ollama version is 0.x.x`

---

### 步骤 2: 下载中文大语言模型

推荐使用 **通义千问 Qwen 2.5** (中文友好):

```powershell
# 下载 7B 模型 (约 4.7GB)
ollama pull qwen2.5:7b

# 或使用更小的 3B 模型 (约 2GB)
ollama pull qwen2.5:3b

# 或使用更大的 14B 模型 (约 9GB,效果更好)
ollama pull qwen2.5:14b
```

其他推荐模型:
```powershell
# Llama 3.2 (英文)
ollama pull llama3.2

# Gemma 2 (Google)
ollama pull gemma2:9b

# 查看所有可用模型
ollama list
```

---

### 步骤 3: 启动 Ollama 服务

```powershell
# 启动服务 (通常安装后自动启动)
ollama serve
```

**提示**: Ollama 安装后通常会作为后台服务自动运行,无需手动启动。

---

### 步骤 4: 配置项目使用 Ollama

#### 方式 A: 使用自动模式 (推荐)

创建 `.env` 文件:
```bash
# 自动选择: 有OpenAI Key用OpenAI,没有则用Ollama
LLM_TYPE=auto
OLLAMA_MODEL=qwen2.5:7b
```

#### 方式 B: 明确指定使用 Ollama

```bash
# 强制使用 Ollama
LLM_TYPE=ollama
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_BASE_URL=http://localhost:11434
```

---

### 步骤 5: 运行应用

```powershell
# 直接运行,无需OpenAI API Key!
python main.py
```

首次运行会看到:
```
🤖 正在初始化LLM模型...
   类型: ollama
   模型: qwen2.5:7b
   服务: http://localhost:11434
✅ Ollama本地模型初始化完成
💡 提示: 使用免费的本地大语言模型
```

---

## 🧪 测试 Ollama

### 快速测试

```powershell
# 在命令行直接测试
ollama run qwen2.5:7b

# 输入问题
>>> 你好,请介绍一下自己
>>> exit  # 退出
```

### 测试项目集成

```powershell
python -c "from langchain_community.llms import Ollama; llm = Ollama(model='qwen2.5:7b'); print(llm.invoke('你好'))"
```

---

## 📊 模型选择建议

### 按计算机配置选择

| 配置 | 推荐模型 | 大小 | 内存需求 |
|------|---------|------|---------|
| 高配 (16GB+) | qwen2.5:14b | 9GB | 16GB+ |
| 中配 (8-16GB) | qwen2.5:7b | 4.7GB | 8GB+ |
| 低配 (8GB以下) | qwen2.5:3b | 2GB | 6GB+ |

### 按语言需求选择

| 需求 | 推荐模型 |
|------|---------|
| 中文为主 | qwen2.5:7b (通义千问) |
| 英文为主 | llama3.2, gemma2 |
| 多语言 | qwen2.5:7b, llama3.2 |

---

## 🔧 常见问题

### Q1: Ollama 服务无法启动?

**检查服务状态:**
```powershell
# 检查 Ollama 是否运行
Get-Process ollama -ErrorAction SilentlyContinue

# 或访问
http://localhost:11434
```

**解决方案:**
```powershell
# 手动启动
ollama serve

# 或重启服务
Stop-Process -Name ollama -Force -ErrorAction SilentlyContinue
ollama serve
```

### Q2: 下载模型速度慢?

**使用镜像站点:**
```powershell
# 设置环境变量使用国内镜像
$env:OLLAMA_MODELS="https://ollama.ai"  # 或其他镜像
ollama pull qwen2.5:7b
```

### Q3: 模型存储在哪里?

**Windows 默认路径:**
```
C:\Users\你的用户名\.ollama\models\
```

**查看磁盘占用:**
```powershell
ollama list
```

### Q4: 如何切换模型?

**编辑 `.env` 文件:**
```bash
OLLAMA_MODEL=qwen2.5:3b  # 改为其他模型
```

**或在运行时:**
```powershell
$env:OLLAMA_MODEL="llama3.2"
python main.py
```

### Q5: Ollama vs OpenAI 哪个更好?

| 维度 | OpenAI | Ollama |
|------|--------|--------|
| 费用 | 💰 按使用付费 | 🆓 完全免费 |
| 质量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 速度 | 快 (云端) | 中等 (本地) |
| 隐私 | 数据上传云端 | 完全本地 |
| 网络 | 需要联网 | 无需联网 |

**建议:**
- 生产环境/高质量需求 → OpenAI
- 个人使用/隐私重要 → Ollama
- 学习测试/无预算 → Ollama

---

## 🎨 使用示例

### 示例 1: 完全离线使用

```powershell
# 1. 不配置任何API Key
# 2. 确保 Ollama 已安装并运行
# 3. 启动应用
python main.py
```

### 示例 2: 切换不同模型

```bash
# .env 文件
LLM_TYPE=ollama

# 使用小模型 (更快)
OLLAMA_MODEL=qwen2.5:3b

# 使用大模型 (更智能)
# OLLAMA_MODEL=qwen2.5:14b
```

### 示例 3: OpenAI 和 Ollama 混合

```bash
# .env 文件
LLM_TYPE=auto

# 有网络时用 OpenAI
OPENAI_API_KEY=sk-xxx

# 无网络时降级到 Ollama
OLLAMA_MODEL=qwen2.5:7b
```

---

## 📈 性能对比

### 响应速度测试 (单次问答)

| 模型 | 响应时间 | 质量 |
|------|---------|------|
| GPT-3.5-turbo | 2-3秒 | ⭐⭐⭐⭐⭐ |
| qwen2.5:7b (CPU) | 10-20秒 | ⭐⭐⭐⭐ |
| qwen2.5:7b (GPU) | 3-5秒 | ⭐⭐⭐⭐ |
| qwen2.5:3b (CPU) | 5-10秒 | ⭐⭐⭐ |

**提示**: 有独立显卡(GPU)时,Ollama 速度接近 OpenAI!

---

## 🔄 更新和维护

### 更新 Ollama

```powershell
# Windows: 重新下载安装包覆盖安装
# 或使用 winget
winget upgrade Ollama.Ollama
```

### 更新模型

```powershell
# 拉取最新版本
ollama pull qwen2.5:7b
```

### 删除不用的模型

```powershell
# 查看已下载的模型
ollama list

# 删除模型
ollama rm qwen2.5:3b
```

---

## 💡 推荐配置

### 最佳实践配置

**.env 文件:**
```bash
# 智能切换模式
LLM_TYPE=auto

# OpenAI (有Key时使用)
OPENAI_API_KEY=sk-xxx

# Ollama 备用 (无Key时使用)
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_BASE_URL=http://localhost:11434

# 温度参数
TEMPERATURE=0.7
```

这样配置后:
- ✅ 有 OpenAI Key → 使用 OpenAI (高质量)
- ✅ 无 OpenAI Key → 自动使用 Ollama (免费)
- ✅ 网络问题 → 降级到 Ollama (本地)

---

## 🎓 进阶配置

### 使用 GPU 加速

Ollama 自动检测并使用 GPU,无需额外配置。

**查看是否使用 GPU:**
```powershell
# 运行模型时观察 GPU 使用率
nvidia-smi  # NVIDIA GPU
# 或任务管理器 → 性能 → GPU
```

### 调整上下文窗口

```bash
# .env 文件
OLLAMA_NUM_CTX=4096  # 上下文长度
```

### 使用量化模型

```powershell
# 下载 4-bit 量化版本 (更小更快)
ollama pull qwen2.5:7b-q4
```

---

## 📚 相关资源

- **Ollama 官网**: https://ollama.ai
- **模型库**: https://ollama.ai/library
- **Qwen 官网**: https://qwenlm.github.io
- **GitHub**: https://github.com/ollama/ollama

---

## ✅ 快速检查清单

使用前确认:

- [ ] Ollama 已安装: `ollama --version`
- [ ] 模型已下载: `ollama list`
- [ ] 服务已启动: `http://localhost:11434`
- [ ] `.env` 已配置: `LLM_TYPE=auto 或 ollama`
- [ ] 运行应用: `python main.py`

---

**现在您可以完全免费使用本地大语言模型了! 🎉**

_更新时间: 2025-10-16_
