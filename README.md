# it-helpdesk-conversational-agent
AI support assistant with RAG, memory, troubleshooting workflow, and ticket-style issue handling built with Streamlit and OpenAI.

# 🖥️ IT Helpdesk Conversational Agent MVP

AI-powered IT helpdesk with RAG, memory, troubleshooting flow, and ticket workflow.
> 💡 The entire Streamlit UI was designed and built with the help of AI.

## Stack
| Layer    | Tech                          |
|----------|-------------------------------|
| LLM      | Groq (LLaMA 3.3 70B Versatile)|
| RAG      | FAISS + SentenceTransformers  |
| UI       | Streamlit (AI-assisted design)|
| Tickets  | SQLite                        |
| Memory   | Rolling 6-message history     |

## Setup

```bash
# Step 1 — Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# Step 2 — Install dependencies
pip install -r requirements.txt

# Step 3 — Run
streamlit run app.py
# Paste your free Groq API key in the sidebar → console.groq.com
```

## Features
- **RAG** — FAISS vector search over IT knowledge base (WiFi, BSOD, printers, MFA, VPN...)
- **Memory** — 6-message rolling context so agent remembers prior steps
- **Ticket Workflow** — Create ticket → auto moves to "In Progress" on first agent reply
- **Dashboard** — View all tickets, update status (Open → In Progress → Resolved → Closed)
- **Escalation** — Agent instructs user to escalate if unresolved after 3 steps

## Model
`llama-3.3-70b-versatile` — Groq's current recommended model (2025).
Check [console.groq.com/docs/deprecations](https://console.groq.com/docs/deprecations) if you hit a model error.

## Sample Run Commands (ask the agent these)

```
"My WiFi is connected but there's no internet access."
"Outlook is not opening, I keep getting an error on startup."
"My laptop screen goes blue and restarts randomly."
"I forgot my Windows password and got locked out."
"The printer shows offline even though it's turned on."
"VPN connects but I can't access internal resources."
"My PC is very slow after the latest Windows update."
"I think my account has been compromised, what do I do?"
```

## Extend
- Replace `DOCS` in `rag.py` with your internal IT wiki / Confluence / PDF exports
- Add email alerts on Critical tickets via `smtplib`
- Deploy to Streamlit Cloud — paste key in Streamlit Secrets
- Export ticket CSV with `st.download_button`

---

> 🤝 **Want a custom AI agent for your business?**
> This project was built with AI-assisted development. If you need help building
> agentic AI models or automation tools, connect with me on LinkedIn —
> I'm happy to help for free in exchange for a professional connection.
> **[Connect on LinkedIn →](https://www.linkedin.com/in/devang-dhaka-512859388/)**