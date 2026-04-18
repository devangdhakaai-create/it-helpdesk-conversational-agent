import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="IT Helpdesk Agent", layout="wide")
st.title("🖥️ IT Helpdesk Conversational Agent")

# --- API key input first, block everything else until provided ---
with st.sidebar:
    st.header("🔑 Groq API Key")
    api_key = st.text_input("Paste key", type="password", placeholder="gsk_...")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key  # inject into env at runtime

if not os.environ.get("GROQ_API_KEY"):
    st.info("👈 Enter your Groq API key to start. Free at console.groq.com")
    st.stop()  # halt until key is present

# safe imports after key is set
from agent import HelpdeskAgent
from tickets import TicketManager

# init once per session
if "agent"    not in st.session_state: st.session_state.agent    = HelpdeskAgent()
if "tickets"  not in st.session_state: st.session_state.tickets  = TicketManager()
if "messages" not in st.session_state: st.session_state.messages = []
if "ticket"   not in st.session_state: st.session_state.ticket   = {}

# --- Sidebar: ticket creation + dashboard ---
with st.sidebar:
    st.divider()
    st.header("🎫 New Ticket")
    user_name = st.text_input("Your Name")
    dept      = st.selectbox("Department", ["IT","HR","Finance","Operations","Other"])
    priority  = st.selectbox("Priority", ["Low","Medium","High","Critical"])
    issue     = st.text_area("Describe Issue", height=80)

    if st.button("Create Ticket"):
        if user_name and issue:
            t = st.session_state.tickets.create(user_name, dept, priority, issue)
            st.session_state.ticket = t          # bind ticket to chat session
            st.success(f"Ticket #{t['id']} created!")
        else:
            st.error("Name and issue required.")

    st.divider()
    st.header("📋 Ticket Dashboard")
    all_tickets = st.session_state.tickets.get_all()
    if all_tickets:
        df = pd.DataFrame(all_tickets)
        st.dataframe(df[["id","name","priority","status"]], use_container_width=True)
        sel_id     = st.selectbox("Ticket ID", df["id"].tolist())
        new_status = st.selectbox("Update Status", ["Open","In Progress","Resolved","Closed"])
        if st.button("Update"):
            st.session_state.tickets.update_status(sel_id, new_status)
            st.rerun()

# --- Active ticket context banner ---
if st.session_state.ticket:
    t = st.session_state.ticket
    st.info(f"🎫 Active: **#{t['id']}** | {t['name']} | {t['priority']} | {t['status']}")

# --- Chat area ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Describe your IT issue...")

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)

    ticket_ctx = f"Ticket: {st.session_state.ticket}" if st.session_state.ticket else ""
    history    = st.session_state.messages[-6:]       # rolling 6-msg memory

    with st.spinner("Diagnosing..."):
        reply = st.session_state.agent.chat(user_input, ticket_ctx, history)

    # auto-update ticket status to In Progress once agent replies
    if st.session_state.ticket and st.session_state.ticket.get("status") == "Open":
        st.session_state.tickets.update_status(st.session_state.ticket["id"], "In Progress")
        st.session_state.ticket["status"] = "In Progress"

    st.session_state.messages.append({"role":"assistant","content":reply})
    with st.chat_message("assistant"):
        st.write(reply)