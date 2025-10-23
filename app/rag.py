"""
RAG检索增强生成模块
RAG (Retrieval-Augmented Generation) Module
"""

import os
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import chromadb

from app.config import (
    KNOWLEDGE_BASE_PATH,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    VECTOR_STORE_PATH,
    TOP_K_RESULTS
)


class RAGRetriever:
    """RAG检索器类"""
    
    def __init__(self):
        """初始化RAG检索器"""
        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        
    def initialize_chromadb(self):
        """初始化ChromaDB客户端和集合"""
        self.chroma_client = chromadb.PersistentClient('./data/vector_store/chroma_db')
        self.chromadb_collection = self.chroma_client.get_or_create_collection(name="rag_collection")
    def list_files(self, directory: str) -> List[str]:
        """列出目录下的所有文件"""
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    
    def load_documents(self) -> List[Document]:
        """加载知识库文档"""
        print(f"📄 正在加载知识库: {KNOWLEDGE_BASE_PATH}")
        documents = []
        for file_path in self.list_files(KNOWLEDGE_BASE_PATH):
            print(f"   - {file_path}")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"知识库文件不存在: {file_path}")
            
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
            
        print(f"✅ 成功加载 {len(documents)} 个文档")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """将文档分割成小块"""
        print(f"✂️  正在分割文档 (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "!", "?", ";", "；", "!", "?", "，", ",", " ", ""],
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"✅ 文档已分割成 {len(chunks)} 个文本块")
        print(chunks)
        return chunks
    
    def initialize_embeddings(self):
        """初始化嵌入模型"""
        print(f"🔧 正在加载嵌入模型: {EMBEDDING_MODEL}")
        
        try:
            # 尝试加载模型,设置缓存目录
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True},
                cache_folder="./.cache"  # 使用本地缓存目录
            )
            print("✅ 嵌入模型加载完成")
        except Exception as e:
            print(f"⚠️  模型加载遇到问题: {str(e)[:100]}")
            print("💡 尝试使用备用方法...")
            
            # 备用方案: 直接使用SentenceTransformer
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer(EMBEDDING_MODEL)
            
            # 包装为LangChain兼容的嵌入类
            class CustomEmbeddings:
                def __init__(self, model):
                    self.model = model
                
                def embed_documents(self, texts):
                    return self.model.encode(texts, convert_to_numpy=True).tolist()
                
                def embed_query(self, text):
                    return self.model.encode([text], convert_to_numpy=True)[0].tolist()
            
            self.embeddings = CustomEmbeddings(model)
            print("✅ 使用备用方法加载模型成功")
    
    def build_vector_store(self, chunks: List[Document]):
        """构建向量数据库"""
        print("🏗️  正在构建向量数据库...")
        
        self.vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        print("✅ 向量数据库构建完成")
    
    def save_vector_store(self):
        """保存向量数据库到磁盘"""
        if self.vector_store is None:
            raise ValueError("向量数据库未初始化")
        
        os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        print(f"💾 向量数据库已保存到: {VECTOR_STORE_PATH}")
    def build_vector_store_chroma(self, chunks: List[Document]):
        """保存向量数据库到磁盘"""
        if self.vector_store is None:
            raise ValueError("向量数据库未初始化")
        
        for i, (chunk, embedding) in enumerate(zip(chunks, self.embeddings)):
            chromadb_collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[str(i)]
            )
        print(f"💾 向量数据库已保存到: data/vector_store/chroma_db")
    def load_vector_store(self):
        """从磁盘加载向量数据库"""
        if not os.path.exists(VECTOR_STORE_PATH):
            raise FileNotFoundError(f"向量数据库不存在: {VECTOR_STORE_PATH}")
        
        print(f"📂 正在加载向量数据库: {VECTOR_STORE_PATH}")
        self.initialize_embeddings()
        
        self.vector_store = FAISS.load_local(
            VECTOR_STORE_PATH,
            self.embeddings,
            # allow_dangerous_deserialization=True
        )
        
        print("✅ 向量数据库加载完成")
        def load_vector_store_from_chromas(self):
            """从磁盘加载向量数据库"""
            if not os.path.exists(VECTOR_STORE_PATH):
                raise FileNotFoundError(f"向量数据库不存在: {VECTOR_STORE_PATH}")
            
            print(f"📂 正在加载向量数据库: {VECTOR_STORE_PATH}")
            self.initialize_embeddings()
            
            self.vector_store = FAISS.load_local(
                VECTOR_STORE_PATH,
                self.embeddings,
                # allow_dangerous_deserialization=True
            )
            
            print("✅ 向量数据库加载完成")
        
    def setup_retriever(self):
        """设置检索器"""
        if self.vector_store is None:
            raise ValueError("向量数据库未初始化")
        
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": TOP_K_RESULTS}
        )
        
        print(f"🔍 检索器已配置 (top_k={TOP_K_RESULTS})")
    
    def initialize(self, force_rebuild: bool = False):
        """
        初始化RAG系统
        
        Args:
            force_rebuild: 是否强制重建向量数据库
        """
        print("🚀 初始化RAG检索系统...")
        
        # 检查是否需要重建向量数据库
        if force_rebuild or not os.path.exists(VECTOR_STORE_PATH):
            print("📚 开始构建新的向量数据库...")
            
            # 加载和处理文档
            documents = self.load_documents()
            chunks = self.split_documents(documents)
            
            # 初始化嵌入模型
            self.initialize_embeddings()
            
            # 构建并保存向量数据库
            self.build_vector_store(chunks)
            self.save_vector_store()
        else:
            # 加载现有向量数据库
            self.load_vector_store()
        
        # 设置检索器
        self.setup_retriever()
        
        print("✅ RAG检索系统初始化完成!\n")
    
    def retrieve(self, query: str) -> List[Document]:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            
        Returns:
            相关文档列表
        """
        if self.retriever is None:
            raise ValueError("检索器未初始化")
        
        results = self.retriever.get_relevant_documents(query)
        return results
    
    def retrieve_with_scores(self, query: str) -> List[Tuple[Document, float]]:
        """
        检索相关文档及其相似度分数
        
        Args:
            query: 查询文本
            
        Returns:
            (文档, 分数)元组列表
        """
        if self.vector_store is None:
            raise ValueError("向量数据库未初始化")
        
        results = self.vector_store.similarity_search_with_score(
            query,
            k=TOP_K_RESULTS
        )
        
        return results
