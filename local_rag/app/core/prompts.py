SYSTEM_PROMPT = """You are an intelligent, helpful AI assistant. 
Your task is to answer user questions based ONLY on the provided context.
If the context does not contain the answer, you must respond with "I don't know based on the provided context."
Do not hallucinate or use outside knowledge.
Cite your sources by mentioning the source file or document if helpful.
"""

QA_PROMPT_TEMPLATE = """Context information is below.
---------------------
{context}
---------------------
Given the context information and no prior knowledge, answer the following query.

Query: {query}
Answer:"""
