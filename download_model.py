"""
模型下载助手
帮助下载和验证 Sentence Transformers 嵌入模型
"""

import sys
from sentence_transformers import SentenceTransformer

def download_model(model_name: str):
    """下载并验证模型"""
    print(f"\n📥 正在下载模型: {model_name}")
    print("=" * 70)
    
    # 模型信息
    models_info = {
        "all-MiniLM-L6-v2": {
            "size": "~80MB",
            "languages": "英文",
            "speed": "快",
            "quality": "中等"
        },
        "paraphrase-multilingual-MiniLM-L12-v2": {
            "size": "~420MB",
            "languages": "50+语言(包含中文)",
            "speed": "中等",
            "quality": "高"
        },
        "distiluse-base-multilingual-cased-v2": {
            "size": "~500MB",
            "languages": "50+语言(包含中文)",
            "speed": "中等",
            "quality": "高"
        }
    }
    
    if model_name in models_info:
        info = models_info[model_name]
        print(f"模型大小: {info['size']}")
        print(f"支持语言: {info['languages']}")
        print(f"速度: {info['speed']}")
        print(f"质量: {info['quality']}")
    
    print("\n⏳ 开始下载,首次下载需要几分钟,请耐心等待...")
    print("-" * 70)
    
    try:
        # 下载模型
        model = SentenceTransformer(model_name)
        print("\n✅ 模型下载成功!")
        
        # 测试模型
        print("\n🧪 测试模型功能...")
        test_texts = [
            "This is a test sentence.",
            "这是一个测试句子。"
        ]
        
        for text in test_texts:
            try:
                embedding = model.encode(text)
                print(f"  ✅ 文本: '{text[:30]}...'")
                print(f"     向量维度: {len(embedding)}")
            except Exception as e:
                print(f"  ⚠️  文本: '{text}' - {e}")
        
        print("\n🎉 模型已就绪,可以正常使用!")
        return True
        
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        print("\n💡 可能的原因:")
        print("  1. 网络连接问题 - 请检查网络")
        print("  2. 无法访问 huggingface.co - 可能需要代理")
        print("  3. 磁盘空间不足")
        print("\n🔧 解决方案:")
        print("  1. 检查网络连接")
        print("  2. 使用更小的模型: all-MiniLM-L6-v2")
        print("  3. 配置代理(如需要)")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("📦 Sentence Transformers 模型下载助手")
    print("=" * 70)
    
    # 可选模型列表
    models = [
        ("all-MiniLM-L6-v2", "英文模型 (推荐,快速下载)"),
        ("paraphrase-multilingual-MiniLM-L12-v2", "多语言模型 (包含中文)"),
        ("distiluse-base-multilingual-cased-v2", "多语言模型 (替代选择)")
    ]
    
    print("\n可用模型:")
    for i, (name, desc) in enumerate(models, 1):
        print(f"  {i}. {name}")
        print(f"     {desc}")
    
    print("\n" + "-" * 70)
    
    # 获取用户选择
    try:
        choice = input("\n请选择要下载的模型 (1-3) [默认:1]: ").strip()
        if not choice:
            choice = "1"
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(models):
            print("❌ 无效选择,使用默认模型")
            idx = 0
        
        model_name = models[idx][0]
        
    except (ValueError, KeyboardInterrupt):
        print("\n使用默认模型...")
        model_name = models[0][0]
    
    # 下载模型
    success = download_model(model_name)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ 完成! 现在可以运行:")
        print("   python main.py")
        print("=" * 70)
        return 0
    else:
        print("\n" + "=" * 70)
        print("⚠️  模型下载失败,请检查网络后重试")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  已取消")
        sys.exit(1)
