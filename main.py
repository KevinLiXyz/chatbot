"""
命令行界面 (CLI) 主程序
Main CLI Application Entry Point
"""

import sys
import argparse
from app.rag import RAGRetriever
from app.chatbot import GovernmentChatbot


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      上海事业单位 - 政务智能客服系统                           ║
║      Government Intelligent Customer Service System          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

💡 使用说明:
  - 输入您的问题,系统将基于招聘知识库回答
  - 输入 'clear' 清空对话历史
  - 输入 'history' 查看对话记录
  - 输入 'quit' 或 'exit' 退出程序

"""
    print(banner)


def print_separator():
    """打印分隔线"""
    print("─" * 70)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="上海事业单位政务智能客服系统"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="强制重建向量数据库"
    )
    parser.add_argument(
        "--show-sources",
        action="store_true",
        help="显示回答的来源文档"
    )
    
    args = parser.parse_args()
    
    try:
        # 打印欢迎信息
        print_banner()
        
        # 初始化RAG检索器
        print("🔧 正在初始化系统...\n")
        rag_retriever = RAGRetriever()
        rag_retriever.initialize(force_rebuild=args.rebuild)
        
        # 初始化聊天机器人
        chatbot = GovernmentChatbot(rag_retriever)
        
        print("✅ 系统已就绪! 请开始提问...\n")
        print_separator()
        
        # 主对话循环
        while True:
            try:
                # 获取用户输入
                user_input = input("\n👤 您: ").strip()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("\n👋 感谢使用! 祝您应聘顺利!")
                    break
                
                elif user_input.lower() in ['clear', '清空']:
                    chatbot.reset_conversation()
                    print("\n✅ 对话历史已清空")
                    continue
                
                elif user_input.lower() in ['history', '历史']:
                    history = chatbot.get_chat_history()
                    if not history:
                        print("\n📝 暂无对话历史")
                    else:
                        print("\n📝 对话历史:")
                        for msg in history:
                            print(f"  {msg['role']}: {msg['content'][:100]}...")
                    continue
                
                # 获取回答
                print("\n🤖 助手: ", end="", flush=True)
                response = chatbot.chat(user_input, show_sources=args.show_sources)
                
                print(response['answer'])
                
                # 显示来源文档(如果启用)
                if args.show_sources and response.get('sources'):
                    print("\n📚 参考来源:")
                    for source in response['sources']:
                        print(f"  [{source['index']}] {source['content']}")
                
                print_separator()
                
            except KeyboardInterrupt:
                print("\n\n👋 检测到中断信号,正在退出...")
                break
            except Exception as e:
                print(f"\n❌ 处理请求时出错: {str(e)}")
                continue
    
    except KeyboardInterrupt:
        print("\n\n👋 程序已中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 系统初始化失败: {str(e)}")
        print("\n💡 提示:")
        print("  1. 请确保已安装所有依赖: pip install -r requirements.txt")
        print("  2. 请确保已配置.env文件中的OPENAI_API_KEY")
        print("  3. 检查网络连接是否正常")
        sys.exit(1)


if __name__ == "__main__":
    main()
