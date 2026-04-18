import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# IT knowledge base — replace with your own docs/PDFs
DOCS = [
    # Network
    "WiFi not connecting: Forget network, restart router, reconnect. Check IP conflict.",
    "VPN issues: Reinstall VPN client, flush DNS with 'ipconfig /flushdns', try alternate server.",
    "Slow internet: Run speedtest, check background downloads, restart NIC via Device Manager.",
    "No network access: Check cable, ping 8.8.8.8, disable/enable adapter, check DHCP lease.",
    # Windows
    "Windows won't boot: Boot into Safe Mode (F8), run 'sfc /scannow', check startup repair.",
    "Blue screen (BSOD): Note error code, update drivers, run memory diagnostic, check Event Viewer.",
    "Windows update stuck: Restart Windows Update service, run troubleshooter, clear SoftwareDistribution folder.",
    "Slow PC: Disable startup programs via Task Manager, run disk cleanup, check for malware.",
    # Email / Office
    "Outlook not opening: Run in safe mode (outlook /safe), disable add-ins, repair Office install.",
    "Cannot send email: Check SMTP settings, verify account credentials, check outbox for stuck mail.",
    "Password reset: Go to account.microsoft.com or contact IT admin for AD password reset.",
    "Excel crashing: Disable COM add-ins, repair Office, delete .xlb toolbar file.",
    # Hardware
    "Printer offline: Set as default printer, restart spooler service, reinstall driver.",
    "Monitor no signal: Check cable connections, try different port, test monitor on another PC.",
    "Keyboard/mouse not working: Try different USB port, check Device Manager, update HID drivers.",
    "Laptop battery not charging: Check charger connection, update battery driver, calibrate battery.",
    # Access / Security
    "Account locked: Wait 15 mins or contact IT admin to unlock in Active Directory.",
    "Ransomware suspected: Disconnect from network immediately, do not pay, contact IT security.",
    "Software installation blocked: Request admin rights via IT portal or submit software request ticket.",
    "MFA not working: Resync authenticator app time, re-register device, contact IT for bypass code.",
]

INDEX_FILE = "faiss_it.bin"   # cached FAISS index

class RAGRetriever:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # lightweight embedder
        self.docs  = DOCS
        self.index = self._load_or_build()

    def _load_or_build(self):
        if os.path.exists(INDEX_FILE):                         # reuse cached index
            return faiss.read_index(INDEX_FILE)
        embs = self.model.encode(self.docs, normalize_embeddings=True)
        idx  = faiss.IndexFlatIP(embs.shape[1])               # cosine similarity
        idx.add(np.array(embs, dtype="float32"))
        faiss.write_index(idx, INDEX_FILE)                     # cache to disk
        return idx

    def search(self, query: str, k: int = 3) -> list:
        q = self.model.encode([query], normalize_embeddings=True)
        _, I = self.index.search(np.array(q, dtype="float32"), k)
        return [self.docs[i] for i in I[0] if i < len(self.docs)]  # top-k docs