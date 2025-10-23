"""
聊天机器人核心模块
Chatbot Core Module with LangChain
"""

from typing import List, Dict
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_openai import ChatOpenAI

from app.config import (
    OPENAI_API_KEY,
    QW_API_BASE_URL,
    QW_API_KEY,
    QW_Model,
    LLM_TYPE,
    LLM_MODEL,
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    TEMPERATURE,
    SYSTEM_PROMPT
)
from app.rag import RAGRetriever


class GovernmentChatbot:
    """政务智能客服机器人"""
    
    def __init__(self, rag_retriever: RAGRetriever):
        """
        初始化聊天机器人
        
        Args:
            rag_retriever: RAG检索器实例
        """
        self.rag_retriever = rag_retriever
        self.llm = None
        self.memory = None
        self.qa_chain = None
        
        self._initialize_llm()
        self._initialize_memory()
        self._initialize_chain()
    
    def _initialize_llm(self):
        """初始化大语言模型"""
        
        # 自动选择可用的LLM
        llm_type = LLM_TYPE
        if llm_type == "auto":
            if OPENAI_API_KEY:
                llm_type = "openai"
            elif QW_API_KEY:
                llm_type = "qw"
            else:
                # 尝试使用Ollama
                llm_type = "ollama"
        
        print(f"🤖 正在初始化LLM模型...")
        print(f"   类型: {llm_type}")
        
        try:
            llm_type = "qw"
            if llm_type == "openai":
                # 使用 OpenAI
                from openai import OpenAI
                
                if not OPENAI_API_KEY:
                    raise ValueError("OpenAI API Key未设置")
                
                print(f"   模型: {LLM_MODEL}")
                self.llm = ChatOpenAI(
                    model="deepseek-chat",  # 或者 "deepseek-reasoner" 用于思考模式:cite[1]
                    temperature=TEMPERATURE,
                    openai_api_key=OPENAI_API_KEY,
                    openai_api_base="https://api.deepseek.com/v1",  # DeepSeek API 端点:cite[1]:cite[5]
                    max_tokens=1024,  # 可选参数
                    timeout=None,
                    max_retries=2
                )
                # self.llm = ChatOpenAI(
                #     model=OLLAMA_MODEL,  # 或者 "deepseek-reasoner" 用于思考模式:cite[1]
                #     temperature=TEMPERATURE,
                #     openai_api_key=OLLAMA_API_KEY,
                #     openai_api_base="https://api.deepseek.com/v1",  # DeepSeek API 端点:cite[1]:cite[5]
                #     max_tokens=1024,  # 可选参数
                #     timeout=None,
                #     max_retries=2
                # )
                print("✅ OpenAI模型初始化完成")
            elif llm_type == "qw":
                # 使用 QW 大模型
                if not QW_API_KEY:
                    raise ValueError("QW API Key未设置")
                
                print(f"   模型: {QW_Model}")
                print(f"   服务: {QW_API_BASE_URL}")
                self.llm = ChatOpenAI(
                    model=QW_Model,
                    openai_api_key=QW_API_KEY,
                    openai_api_base=QW_API_BASE_URL,
                    temperature=TEMPERATURE,
                    timeout=30
                )
                print("✅ QW大模型初始化完成")    
            elif llm_type == "ollama":
                # 使用 Ollama 本地模型
                try:
                    from langchain_community.llms import Ollama
                    
                    print(f"   模型: {OLLAMA_MODEL}")
                    print(f"   服务: {OLLAMA_BASE_URL}")
                    self.llm = Ollama(
                        model=OLLAMA_MODEL,
                        base_url=OLLAMA_BASE_URL,
                        temperature=TEMPERATURE,
                        timeout=300
                    )
                    print("✅ Ollama本地模型初始化完成")
                    print("💡 提示: 使用免费的本地大语言模型")
                    
                except Exception as e:
                    print(f"⚠️  Ollama初始化失败: {e}")
                    print("💡 请确保Ollama服务已启动")
                    print("   安装: https://ollama.ai")
                    print("   启动: ollama serve")
                    print(f"   拉取模型: ollama pull {OLLAMA_MODEL}")
                    raise
                    
            elif llm_type == "fake":
                # 使用假的LLM用于测试
                from langchain_community.llms.fake import FakeListLLM
                
                responses = [
                    "这是一个测试回答。实际使用时，请配置OpenAI API Key或安装Ollama。",
                    "我是一个演示用的假模型。请安装真实的LLM来获得智能回答。",
                    "当前使用测试模式。要获得真实回答，请配置LLM。"
                ]
                self.llm = FakeListLLM(responses=responses)
                print("⚠️  使用测试模式(FakeLLM)")
                print("💡 要获得真实回答,请配置OpenAI或Ollama")
                
            else:
                raise ValueError(f"不支持的LLM类型: {llm_type}")
                
        except Exception as e:
            print(f"\n❌ LLM初始化失败: {e}")
            print("\n💡 可用选项:")
            print("   1. 配置OpenAI API Key (推荐):")
            print("      在.env文件中设置: OPENAI_API_KEY=sk-xxx")
            print("   2. 使用Ollama本地模型(免费):")
            print("      安装: https://ollama.ai")
            print("      运行: ollama pull qwen2.5:7b")
            print("   3. 使用测试模式:")
            print("      在.env文件中设置: LLM_TYPE=fake")
            raise
    
    def _initialize_memory(self):
        """初始化对话记忆"""
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        
        print("💭 对话记忆已初始化")
    
    def _initialize_chain(self):
        """初始化对话检索链"""
        print("🔗 正在构建对话检索链...")
        
        # 自定义问答提示词模板
        qa_template = f"""{SYSTEM_PROMPT}

基于以下检索到的上下文信息回答用户的问题:

{{context}}

用户问题: {{question}}

请给出准确、有帮助的回答:"""
        
        QA_PROMPT = PromptTemplate(
            template=qa_template,
            input_variables=["context", "question"]
        )
        
        # 创建对话检索链
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.rag_retriever.retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT},
            verbose=False
        )
        
        print("✅ 对话检索链构建完成\n")
    
    def chat(self, user_input: str, show_sources: bool = False) -> Dict:
        """
        处理用户输入并返回回答
        
        Args:
            user_input: 用户输入的问题
            show_sources: 是否显示来源文档
            
        Returns:
            包含回答和来源的字典
        """
        if not user_input.strip():
            return {
                "answer": "请输入您的问题。",
                "sources": []
            }
        
        # 调用对话链
        result = self.qa_chain.invoke({"question": user_input})
        
        answer = result.get("answer", "抱歉,我无法回答这个问题。")
        source_docs = result.get("source_documents", [])
        
        response = {
            "answer": answer,
            "sources": []
        }
        
        # 如果需要显示来源
        if show_sources and source_docs:
            for i, doc in enumerate(source_docs[:3], 1):
                response["sources"].append({
                    "index": i,
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
        
        return response
    
    def reset_conversation(self):
        """重置对话历史"""
        self.memory.clear()
        print("🔄 对话历史已清空")
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        获取对话历史
        
        Returns:
            对话历史列表
        """
        messages = self.memory.chat_memory.messages
        history = []
        
        for msg in messages:
            if hasattr(msg, 'type'):
                role = "用户" if msg.type == "human" else "助手"
                history.append({
                    "role": role,
                    "content": msg.content
                })
        
        return history
