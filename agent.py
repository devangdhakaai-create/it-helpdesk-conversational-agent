import os
from groq import Groq
from rag import RAGRetriever

class HelpdeskAgent:
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])  # groq client
        self.rag    = RAGRetriever()                             # FAISS retriever
        self.model  = "llama-3.3-70b-versatile"                 # current groq model

    def chat(self, query: str, ticket_ctx: str, history: list) -> str:
        docs    = self.rag.search(query, k=3)                   # top-3 relevant KB docs
        context = "\n".join(docs)

        system = f"""You are an expert IT helpdesk agent. Your job is to:
1. Diagnose the user's IT issue step by step
2. Provide clear, numbered troubleshooting steps
3. Ask clarifying questions if the issue is unclear
4. Escalate to human if unresolved after 3 steps
5. Always be concise and professional

KNOWLEDGE BASE CONTEXT:
{context}

{ticket_ctx}"""

        # build message history for groq
        messages = [{"role":"system","content":system}]
        for m in history[:-1]:                                  # exclude current msg
            messages.append({"role":m["role"],"content":m["content"]})
        messages.append({"role":"user","content":query})

        resp = self.client.chat.completions.create(
            model       = self.model,
            messages    = messages,
            max_tokens  = 600,
            temperature = 0.4                                   # lower = more precise
        )
        return resp.choices[0].message.content