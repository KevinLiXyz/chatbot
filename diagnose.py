"""
模型下载问题诊断和修复工具
Model Download Troubleshooting and Fix Tool
"""

import sys
import os

def test_imports():
    """测试基础导入"""
    print("\n" + "="*70)
    print("📦 测试 1: 检查依赖包导入")
    print("="*70)
    
    packages = {
        "sentence_transformers": "sentence-transformers",
        "torch": "torch",
        "transformers": "transformers",
    }
    
    all_ok = True
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package}: {e}")
            all_ok = False
    
    return all_ok


def test_model_download():
    """测试模型下载"""
    print("\n" + "="*70)
    print("📥 测试 2: 模型下载测试")
    print("="*70)
    
    print("\n尝试方法 1: 使用 sentence-transformers 直接加载")
    try:
        from sentence_transformers import SentenceTransformer
        print("  ⏳ 正在下载模型 all-MiniLM-L6-v2...")
        print("  (首次下载约80MB,需要1-3分钟)")
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        test_text = "This is a test."
        embedding = model.encode(test_text)
        
        print(f"  ✅ 成功! 向量维度: {len(embedding)}")
        return True, "sentence-transformers"
        
    except Exception as e:
        print(f"  ❌ 失败: {str(e)[:200]}")
    
    print("\n尝试方法 2: 使用 HuggingFaceEmbeddings")
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("  ⏳ 正在加载...")
        
        embeddings = HuggingFaceEmbeddings(
            model_name='all-MiniLM-L6-v2',
            model_kwargs={'device': 'cpu'}
        )
        test_embedding = embeddings.embed_query("test")
        
        print(f"  ✅ 成功! 向量维度: {len(test_embedding)}")
        return True, "langchain"
        
    except Exception as e:
        print(f"  ❌ 失败: {str(e)[:200]}")
    
    return False, None


def check_network():
    """检查网络连接"""
    print("\n" + "="*70)
    print("🌐 测试 3: 网络连接检查")
    print("="*70)
    
    try:
        import requests
        
        urls = [
            ("Hugging Face", "https://huggingface.co"),
            ("Hugging Face 镜像", "https://hf-mirror.com"),
        ]
        
        for name, url in urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {name}: 可访问")
                else:
                    print(f"  ⚠️  {name}: 状态码 {response.status_code}")
            except Exception as e:
                print(f"  ❌ {name}: 无法访问 - {str(e)[:50]}")
        
    except ImportError:
        print("  ⚠️  requests 包未安装,跳过网络测试")


def check_disk_space():
    """检查磁盘空间"""
    print("\n" + "="*70)
    print("💾 测试 4: 磁盘空间检查")
    print("="*70)
    
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        
        free_gb = free / (1024**3)
        print(f"  可用空间: {free_gb:.2f} GB")
        
        if free_gb < 1:
            print("  ⚠️  警告: 可用空间不足 1GB")
            return False
        else:
            print("  ✅ 磁盘空间充足")
            return True
            
    except Exception as e:
        print(f"  ⚠️  无法检查磁盘空间: {e}")
        return True


def suggest_solutions(import_ok, model_ok, method):
    """提供解决方案建议"""
    print("\n" + "="*70)
    print("💡 诊断结果和建议")
    print("="*70)
    
    if import_ok and model_ok:
        print("\n✅ 所有测试通过!")
        print(f"   使用方法: {method}")
        print("\n📝 你现在可以:")
        print("   python demo_simple.py    # 测试RAG检索")
        print("   python main.py           # 启动完整应用")
        return 0
    
    if not import_ok:
        print("\n❌ 依赖包导入失败")
        print("\n解决方案:")
        print("  1. 重新安装依赖:")
        print("     pip install --upgrade sentence-transformers torch transformers")
        print("  2. 或使用国内镜像:")
        print("     pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sentence-transformers")
        return 1
    
    if not model_ok:
        print("\n❌ 模型下载失败")
        print("\n可能的原因:")
        print("  • 网络连接问题")
        print("  • 无法访问 huggingface.co")
        print("  • 磁盘空间不足")
        print("  • 防火墙或代理设置")
        
        print("\n解决方案:")
        print("\n方案 1: 使用 Hugging Face 镜像")
        print("  $env:HF_ENDPOINT=\"https://hf-mirror.com\"")
        print("  python download_model.py")
        
        print("\n方案 2: 使用离线模式(无需模型下载)")
        print("  python demo_offline.py")
        
        print("\n方案 3: 手动下载模型")
        print("  1. 访问: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2")
        print("  2. 下载所有文件到本地目录")
        print("  3. 修改 app/config.py 指向本地路径")
        
        print("\n方案 4: 使用更小的模型")
        print("  编辑 app/config.py:")
        print("  EMBEDDING_MODEL = \"all-MiniLM-L6-v2\"")
        
        return 1


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🔍 AI 智能客服 - 模型问题诊断工具")
    print("="*70)
    print("\n这个工具将帮助诊断和解决模型下载问题。")
    print("测试可能需要几分钟,请耐心等待...\n")
    
    # 运行所有测试
    import_ok = test_imports()
    check_network()
    check_disk_space()
    
    model_ok = False
    method = None
    if import_ok:
        model_ok, method = test_model_download()
    
    # 提供建议
    return suggest_solutions(import_ok, model_ok, method)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
