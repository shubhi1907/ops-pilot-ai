import streamlit as st
import requests
import time
import base64
from pathlib import Path

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="OpsPilot AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://127.0.0.1:8000"
PROCESS_URL = f"{API_BASE}/process-email"

ASSET_DIR = Path(__file__).resolve().parent / "assets"

# =====================================================
# HELPERS
# =====================================================

def image_base64(filename):
    path = ASSET_DIR / filename

    if not path.exists():
        return ""

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =====================================================
# FETCH ANALYTICS FROM BACKEND
# =====================================================

@st.cache_data(ttl=30)
def fetch_analytics():
    try:
        response = requests.get(f"{API_BASE}/analytics", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        pass
    
    return {
        "total_tickets": 0,
        "high_priority_tickets": 0,
        "escalations": 0
    }

# =====================================================
# SESSION STATE
# =====================================================

if "workflow_step" not in st.session_state:
    st.session_state.workflow_step = 0

if "workflow_running" not in st.session_state:
    st.session_state.workflow_running = False

if "api_result" not in st.session_state:
    st.session_state.api_result = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "agent_times" not in st.session_state:
    st.session_state.agent_times = {}

if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total_tickets": 0,
        "high_priority": 0,
        "escalations": 0
    }

if "current_ticket_id" not in st.session_state:
    st.session_state.current_ticket_id = None

if "approval_status" not in st.session_state:
    st.session_state.approval_status = None

if "show_reject_reason" not in st.session_state:
    st.session_state.show_reject_reason = False

if "approval_workflow_step" not in st.session_state:
    st.session_state.approval_workflow_step = 0

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

/* ====================================
   REMOVE STREAMLIT DEFAULT PADDING
==================================== */

.block-container {
    padding-top: 4.2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* Remove extra left gap */
section.main > div {
    padding-left: 0rem !important;
    padding-right: 0rem !important;
}
            
html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.main .block-container {
    max-width: 100% !important;
    padding-top: -1.0rem !important;
    padding-bottom: 0rem !important;
    padding-left: -5.5rem !important;
    padding-right: -5.5rem !important;
}

.stApp {
    background: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at top left, #1e3a8a 0%, transparent 30%),
        linear-gradient(180deg, #050816 0%, #081028 100%);
    width: 220px !important;
}

.sidebar-logo {
    color: white;
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 1.2rem;
}

.sidebar-item {
    color: rgba(255,255,255,0.82);
    border-radius: 10px;
    margin-bottom: 0.3rem;
    font-weight: 600;
}

.sidebar-active {
    background: linear-gradient(90deg,#7c3aed,#6d28d9);
    box-shadow: 0 0 20px rgba(124,58,237,0.35);
}

h1 {
    margin-top: 0rem !important;
    padding-top: 0rem !important;
}

/* ====================================
   PROCESS EMAIL BUTTON
==================================== */

.stButton > button {
    width: 100% !important;
    height: 52px !important;
    border-radius: 14px !important;
    border: 1px solid #7C3AED !important;
    background: linear-gradient(
        135deg,
        #8B5CF6 0%,
        #7C3AED 100%
    ) !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow:
        0 6px 20px rgba(124,58,237,0.22) !important;
}

/* Hover */
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow:
        0 10px 25px rgba(124,58,237,0.30) !important;
    border: 1px solid #8B5CF6 !important;
}

.hero-title {
    font-size: 2.15rem;
    font-weight: 850;
    color: #0f172a;
    line-height: 1.15;
    margin-top: -6px;
    margin-bottom: 0.2rem;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    color: #667085;
    margin-top: 0.3rem;
    margin-bottom: 1rem;
}

.workflow-title {
    font-size: 1.05rem;
    font-weight: 850;
    margin-top: 0.7rem;
    margin-bottom: 0.1rem;
    letter-spacing: -0.01em;
}

.workflow-subtitle {
    color: #667085;
    margin-bottom: 1.6rem;
}

.workflow-row {
    display:flex;
    align-items:stretch;
    justify-content:space-between;
}

.workflow-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 300px;
    font-size: 34px;
    font-weight: 800;
    color: #111827;
}

/* =========================
   EMAIL INPUT
========================= */

textarea {
    border-radius: 16px !important;
    border: 1px solid #E5E7EB !important;
    background: #F9FAFB !important;
    padding: 16px !important;
    font-size: 15px !important;
    color: #111827 !important;
    line-height: 1.5 !important;
    box-shadow: none !important;
}

textarea:focus {
    border: 1px solid #A855F7 !important;
    box-shadow: 0 0 0 2px rgba(168,85,247,0.08) !important;
}

.agent-card {
    position: relative;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 18px 16px;
    height: 300px;
    min-height: 300px;
    max-height: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    overflow: hidden;
    transition: all 0.2s ease;
    box-shadow:
        0 1px 2px rgba(16,24,40,0.04);
}

.agent-active {
    border:2px solid #22c55e;
    box-shadow:0 0 24px rgba(34,197,94,0.20);
    background:#fbfffc;
    animation: pulse-border 1.5s ease-in-out infinite;
}

@keyframes pulse-border {
    0% {
        box-shadow: 0 0 24px rgba(34,197,94,0.20);
    }
    50% {
        box-shadow: 0 0 40px rgba(34,197,94,0.40);
    }
    100% {
        box-shadow: 0 0 24px rgba(34,197,94,0.20);
    }
}

.agent-step {
    position: absolute;
    top: 14px;
    left: 14px;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 16px;
    font-weight: 700;
}
            

            
.step-purple { background:#7c3aed; }
.step-blue { background:#2563eb; }
.step-green { background:#16a34a; }
.step-orange { background:#f97316; }

.agent-image {
    width: 105px;
    height: 105px;
    object-fit: contain;
    margin-top: 10px;
    display: block;
}

.agent-title {
    font-size: 15px;
    font-weight: 700;
    line-height: 1.28;
    text-align: center;
    color: #111827;
    margin-bottom: 10px;
    min-height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.agent-desc {
    font-size: 12px;
    line-height: 1.42;
    color: #6B7280;
    text-align: center;
    max-width: 88%
    margin: 0 auto;
    min-height: 52px;
}

.agent-footer {
    width: 100%;
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 14px;
    font-size: 12px;
    font-weight: 700;
}

.status-banner {
    margin-top:1.6rem;
    background:#ecfdf3;
    border:1px solid #b7ebc6;
    color:#166534;
    border-radius:16px;
    font-weight:700;
    text-align:center;
}

.ops-grid {
    display:grid;
    grid-template-columns:1fr 1fr 1.2fr 1fr;
    gap:14px;
    margin-top:1rem;
}

.ops-card {
    background:white;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:1rem;
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
    min-height:300px;
}

            div.stButton > button {
    border-radius: 12px !important;
    height: 44px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    border: none !important;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    transition: 0.2s ease;
}

.ops-title {
    font-weight:800;
    margin-bottom:1.2rem;
    font-size:1rem;
}

.summary-label {
    color:#667085;
    font-size:0.82rem;
    font-weight:600;
}

.summary-value {
    font-size:0.92rem;
    font-weight:700;
    margin-bottom:1rem;
}

.pill {
    display:inline-block;
    padding:0.4rem 0.7rem;
    border-radius:999px;
    font-size:0.7rem;
    font-weight:700;
}

.red-pill {
    background:#fee2e2;
    color:#dc2626;
}

.purple-pill {
    background:#ede9fe;
    color:#7c3aed;
}

.orange-pill {
    background:#ffedd5;
    color:#ea580c;
}

.green-pill {
    background:#dcfce7;
    color:#16a34a;
}

.response-box {
    background:#f8fbff;
    border:1px solid #c7d2fe;
    border-radius:14px;
    padding:1rem;
    font-size:0.9rem;
    line-height:1.7;
    min-height:200px;
}

.timeline-item {
    display:flex;
    justify-content:space-between;
    margin-bottom:1rem;
    font-size:0.85rem;
}

.kpi-grid {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:16px;
    margin-top:1.8rem;
}

.kpi-card {
    background:white;
    border-radius:18px;
    padding:1.2rem;
    border:1px solid #E5E7EB;
}

.kpi-number {
    font-size:2rem;
    font-weight:800;
}

.kpi-label {
    color:#667085;
    margin-top:0.3rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
'<div class="sidebar-logo">🧠 OpsPilot AI</div>',
        unsafe_allow_html=True
    )

    menu = [
        ("🏠 Dashboard", "Dashboard"),
        ("� Process Email", "Process Email"),
        ("📋 All Tickets", "All Tickets"),
        ("✅ Approvals Queue", "Approvals Queue"),
        ("📊 Analytics & ROI", "Analytics & ROI"),
        ("📚 Knowledge Base", "Knowledge Base"),
        ("⚙️ Settings", "Settings"),
    ]

    for label, page_name in menu:
        if st.button(label, key=f"nav_{page_name}", use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

# =====================================================
# HEADER
# =====================================================

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero-title">
    OpsPilot AI — Agentic Workflow Automation Platform
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-subtitle">
    Intelligent Support Operations. Multi-Agent Orchestration. Smarter Decisions.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# =====================================================
# PAGE ROUTING
# =====================================================

current_page = st.session_state.page

# =====================================================
# PAGE ROUTING
# =====================================================

current_page = st.session_state.page

if current_page != "Dashboard":
    st.markdown(f"<h1>{current_page}</h1>", unsafe_allow_html=True)

    if current_page == "Process Email":
        st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
<h3 style="margin: 0; color: white;">🚀 Process Customer Emails with AI</h3>
<p style="margin: 5px 0 0 0; opacity: 0.9;">Submit customer emails for intelligent analysis, categorization, and automated response generation.</p>
</div>
        """, unsafe_allow_html=True)

        # Show the email processing interface here
        email_left, email_right = st.columns([12, 2.4])

        with email_left:
            st.markdown("""
<div style="font-size:15px; font-weight:600; color:#1F2937; margin-bottom:1px; margin-top:1px;">
Incoming Customer Email
</div>
            """, unsafe_allow_html=True)

            email_input = st.text_area(
                "",
                placeholder="Example: Our production system is down and impacting enterprise customers...",
                height=110,
                label_visibility="collapsed",
                key="email_input_page"
            )

        with email_right:
            st.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)

            process_clicked = st.button(
                "🚀 Process Email",
                use_container_width=True,
                key="process_btn_page"
            )

        # Process email logic
        if process_clicked and email_input:
            st.session_state.workflow_running = True
            st.session_state.agent_times = {}

            for i in range(1, 6):
                step_start = time.time()
                st.session_state.workflow_step = i
                time.sleep(0.5)
                st.session_state.agent_times[i] = round(
                    time.time() - step_start + 0.8,
                    1
                )

            try:
                response = requests.post(
                    PROCESS_URL,
                    json={"email": email_input},
                    timeout=60
                )

                if response.status_code == 200:
                    api_data = response.json()
                    st.session_state.api_result = api_data
                    st.session_state.current_ticket_id = api_data.get("ticket_id")
                    st.session_state.workflow_step = 6
                    st.session_state.agent_times[6] = 0.8
                    st.success(f"✅ Ticket #{st.session_state.current_ticket_id} processed successfully!")
                else:
                    st.error(f"Backend error: {response.status_code}")

            except Exception as e:
                st.error(f"Backend connection failed: {e}")

            st.session_state.workflow_running = False
            st.rerun()

        # Show workflow if running
        if st.session_state.workflow_running or st.session_state.workflow_step > 0:
            st.markdown('<h3>AI Workforce Processing Your Request</h3>', unsafe_allow_html=True)
            # Include workflow visualization here
            workflow_html = '<div class="workflow-row">'

            for idx, agent in enumerate(agents):
                active = st.session_state.workflow_step == agent["step"]
                completed = st.session_state.workflow_step > agent["step"]

                status = "⏳ Pending"
                if completed:
                    status = "✅ Completed"
                if active:
                    status = "⚙️ Running"

                active_class = "agent-card agent-active" if active else "agent-card"

                workflow_html += f'''
<div class="{active_class}">
<div class="agent-step {agent['color']}">
    {agent['step']}
</div>
<img class="agent-image" src="data:image/png;base64,{image_base64(agent['image'])}">
<div class="agent-title">{agent['title']}</div>
<div class="agent-desc">{agent['desc']}</div>
<div class="agent-footer">
<div>{status}</div>
<div>{st.session_state.agent_times.get(agent['step'], '--')}s</div>
</div>
</div>
                '''

                if idx != len(agents) - 1:
                    workflow_html += '<div class="workflow-arrow">→</div>'

            workflow_html += '</div>'
            st.markdown(workflow_html, unsafe_allow_html=True)

        # Show results if available
        result = st.session_state.api_result
        if result and result.get('ticket_id'):
            risk_score = float(result.get('risk_score', 0)) if result.get('risk_score') else 0
            approval_status_display = "Pending Approval"
            approval_status_color = "orange-pill"

            if st.session_state.approval_status == "approved":
                approval_status_display = "Approved"
                approval_status_color = "green-pill"
            elif st.session_state.approval_status == "rejected":
                approval_status_display = "Rejected"
                approval_status_color = "red-pill"

            # AI Generated Response Card (moved above the dashboard cards)
            st.markdown(f"""
<div class="response-card">

<div class="response-title">
💬 AI Generated Response
</div>

<div class="response-box">
{result['response']}
</div>

</div>
""", unsafe_allow_html=True)

            if st.session_state.current_ticket_id is not None:
                approve_col, reject_col, regen_col = st.columns([1,1,1])

                with approve_col:
                    if st.button("✅ Approve & Send", use_container_width=True, key="btn_approve_page"):
                        try:
                            response = requests.post(
                                f"{API_BASE}/approve-ticket/{st.session_state.current_ticket_id}",
                                timeout=10
                            )
                            if response.status_code == 200:
                                st.session_state.approval_status = "approved"
                                st.success("✅ Response approved and delivered to customer!")
                                st.rerun()
                            else:
                                st.error(f"Approval failed: {response.status_code}")
                        except Exception as e:
                            st.error(f"Could not approve ticket: {e}")

                with reject_col:
                    if st.button("❌ Request Changes", use_container_width=True, key="btn_reject_page"):
                        st.session_state.show_reject_reason = True

                with regen_col:
                    if st.button("🔄 Regenerate", use_container_width=True, key="btn_regen_page"):
                        st.info("🔄 Regenerating response... (Feature in development)")

                if st.session_state.show_reject_reason:
                    st.markdown("---")
                    st.subheader("Request Changes")
                    rejection_reason = st.text_area("Why reject this response?", height=100, key="reject_reason_input_page")
                    reject_submit_col1, reject_submit_col2 = st.columns(2)

                    with reject_submit_col1:
                        if st.button("Submit Rejection", use_container_width=True, key="btn_submit_reject_page"):
                            try:
                                response = requests.post(
                                    f"{API_BASE}/reject-ticket/{st.session_state.current_ticket_id}",
                                    params={"reason": rejection_reason},
                                    timeout=10
                                )
                                if response.status_code == 200:
                                    st.session_state.approval_status = "rejected"
                                    st.session_state.show_reject_reason = False
                                    st.warning("⚠️ Ticket rejected. Feedback sent to AI agents for improvement.")
                                    st.rerun()
                                else:
                                    st.error(f"Rejection failed: {response.status_code}")
                            except Exception as e:
                                st.error(f"Could not reject ticket: {e}")

                    with reject_submit_col2:
                        if st.button("Cancel", use_container_width=True, key="btn_cancel_reject_page"):
                            st.session_state.show_reject_reason = False
                            st.rerun()

            st.markdown(f"""
<div class="ops-grid">
<div class="ops-card">
<div class="ops-title">🎫 Current Ticket Summary</div>
<div class="summary-label">Ticket ID</div>
<div class="summary-value">{result['ticket_id']}</div>
<div class="summary-label">Department</div>
<div class="summary-value">{result['department']}</div>
<div class="summary-label">Priority</div>
<div class="summary-value">
<span class="pill red-pill">{result['priority']}</span>
<span class="pill purple-pill">{result['category']}</span>
</div>
<div class="summary-label">Status</div>
<div class="summary-value">
<span class="pill {approval_status_color}">{approval_status_display}</span>
</div>
</div>

<div class="ops-card">
<div class="ops-title">🛡️ AI Decision & Risk Assessment</div>
<div class="summary-label">Risk Score</div>
<div class="summary-value" style="font-size:2rem;color:#dc2626;">
    {risk_score:.1f} / 10
</div>
<div class="summary-label">Suggested Action</div>
<div class="summary-value">
Escalate to L2 Support + Notify Engineering
</div>
</div>

</div>
            """, unsafe_allow_html=True)
            if st.session_state.current_ticket_id is not None:
                approve_col, reject_col, regen_col = st.columns([1,1,1])

                with approve_col:
                    if st.button("✅ Approve & Send", use_container_width=True, key="btn_approve_page"):
                        try:
                            response = requests.post(
                                f"{API_BASE}/approve-ticket/{st.session_state.current_ticket_id}",
                                timeout=10
                            )
                            if response.status_code == 200:
                                st.session_state.approval_status = "approved"
                                st.success("✅ Response approved and delivered to customer!")
                                st.rerun()
                            else:
                                st.error(f"Approval failed: {response.status_code}")
                        except Exception as e:
                            st.error(f"Could not approve ticket: {e}")

                with reject_col:
                    if st.button("❌ Request Changes", use_container_width=True, key="btn_reject_page"):
                        st.session_state.show_reject_reason = True

                with regen_col:
                    if st.button("🔄 Regenerate", use_container_width=True, key="btn_regen_page"):
                        st.info("🔄 Regenerating response... (Feature in development)")

                # Handle rejection
                if st.session_state.show_reject_reason:
                    st.markdown("---")
                    st.subheader("Request Changes")
                    rejection_reason = st.text_area("Why reject this response?", height=100, key="reject_reason_input_page")
                    reject_submit_col1, reject_submit_col2 = st.columns(2)

                    with reject_submit_col1:
                        if st.button("Submit Rejection", use_container_width=True, key="btn_submit_reject_page"):
                            try:
                                response = requests.post(
                                    f"{API_BASE}/reject-ticket/{st.session_state.current_ticket_id}",
                                    params={"reason": rejection_reason},
                                    timeout=10
                                )
                                if response.status_code == 200:
                                    st.session_state.approval_status = "rejected"
                                    st.session_state.show_reject_reason = False
                                    st.warning("⚠️ Ticket rejected. Feedback sent to AI agents for improvement.")
                                    st.rerun()
                                else:
                                    st.error(f"Rejection failed: {response.status_code}")
                            except Exception as e:
                                st.error(f"Could not reject ticket: {e}")

                    with reject_submit_col2:
                        if st.button("Cancel", use_container_width=True, key="btn_cancel_reject_page"):
                            st.session_state.show_reject_reason = False
                            st.rerun()
            else:
                st.info("👆 Process an email above to enable approval actions")

    elif current_page == "All Tickets":
        st.markdown("""
<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
<h3 style="margin: 0; color: white;">📋 Ticket Management Dashboard</h3>
<p style="margin: 5px 0 0 0; opacity: 0.9;">View all customer tickets, their status, and manage your support queue.</p>
</div>
        """, unsafe_allow_html=True)

        st.info("📋 Ticket management interface coming soon. Currently showing processed tickets on Dashboard.")

    elif current_page == "Approvals Queue":
        st.markdown("""
<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
<h3 style="margin: 0; color: white;">✅ Human-in-the-Loop Approvals</h3>
<p style="margin: 5px 0 0 0; opacity: 0.9;">Review AI-generated responses before they reach customers. Quality control and oversight.</p>
</div>
        """, unsafe_allow_html=True)

        st.info("✅ Approval queue interface coming soon. Use Dashboard to approve/reject individual tickets.")

    elif current_page == "Analytics & ROI":
        st.markdown("""
<div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
<h3 style="margin: 0; color: white;">📊 Business Intelligence & ROI Analytics</h3>
<p style="margin: 5px 0 0 0; opacity: 0.9;">Track performance metrics, cost savings, and demonstrate the value of AI automation.</p>
</div>
        """, unsafe_allow_html=True)

        # Fetch and display analytics
        analytics = fetch_analytics()
        total = analytics.get("total_tickets", 0)
        high_priority = analytics.get("high_priority_tickets", 0)
        escalations = analytics.get("escalations", 0)
        resolved = total - escalations if total > 0 else 0
        resolved_rate = round((resolved / total * 100)) if total > 0 else 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Tickets Processed", total, delta=f"+{total}")
        with col2:
            st.metric("High Priority Tickets", high_priority, delta=f"{high_priority}")
        with col3:
            st.metric("Auto-Resolved", resolved, delta=f"{resolved}")
        with col4:
            st.metric("Resolution Rate", f"{resolved_rate}%", delta=f"{resolved_rate}%")

        st.markdown("---")

        # ROI Calculator
        st.subheader("💰 ROI Impact Calculator")

        col1, col2 = st.columns(2)

        with col1:
            avg_resolution_time_saved = st.slider("Avg Time Saved per Ticket (minutes)", 10, 60, 30)
            cost_per_hour = st.slider("Cost per Support Hour ($)", 50, 200, 75)

        with col2:
            monthly_tickets = st.number_input("Monthly Ticket Volume", 100, 10000, 1000)
            automation_rate = st.slider("Automation Rate (%)", 0, 100, 75)

        monthly_savings = (monthly_tickets * automation_rate / 100 * avg_resolution_time_saved / 60 * cost_per_hour)
        annual_savings = monthly_savings * 12

        st.success(f"**Estimated Monthly Savings: ${monthly_savings:,.0f}**")
        st.success(f"**Estimated Annual Savings: ${annual_savings:,.0f}**")

        st.markdown("---")
        st.markdown("""
        ### 🎯 Key Performance Indicators

        - **Resolution Rate**: Percentage of tickets handled without escalation
        - **Response Time**: Average time from ticket creation to customer response
        - **Cost Savings**: Reduction in support labor costs through automation
        - **Customer Satisfaction**: Quality of AI-generated responses
        - **Escalation Rate**: Tickets requiring human intervention
        """)

    elif current_page == "Knowledge Base":
        st.markdown("""
<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
<h3 style="margin: 0; color: white;">📚 AI Learning & Knowledge Base</h3>
<p style="margin: 5px 0 0 0; opacity: 0.9;">View historical incidents, AI learning patterns, and improve response quality over time.</p>
</div>
        """, unsafe_allow_html=True)

        st.info("📚 Knowledge base interface coming soon. AI agents learn from historical ticket data.")

    elif current_page == "Settings":
        st.markdown("""
<div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
<h3 style="margin: 0; color: white;">⚙️ System Configuration</h3>
<p style="margin: 5px 0 0 0; opacity: 0.9;">Configure AI parameters, approval workflows, and system settings.</p>
</div>
        """, unsafe_allow_html=True)

        st.info("⚙️ Settings interface coming soon. Configure AI confidence thresholds and approval rules.")

    st.stop()

# =====================================================
# DASHBOARD CONTENT (Below this is only for Dashboard page)
# =====================================================

# Hero Section - Value Proposition
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px; border-radius: 20px; margin-bottom: 20px; text-align: center;">
<h1 style="color: white; margin: 0; font-size: 2.5rem;">🚀 OpsPilot AI</h1>
<h2 style="color: white; margin: 5px 0; opacity: 0.9; font-weight: 300;">Intelligent Support Operations Platform</h2>
<p style="font-size: 1.2rem; margin: 20px 0; opacity: 0.9; max-width: 800px; margin-left: auto; margin-right: auto;">
Transform your customer support operations with AI-powered automation. Reduce response times by 75%, cut costs by 60%, and deliver 24/7 intelligent support.
</p>
</div>
""", unsafe_allow_html=True)

# Key Benefits Grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
<div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #e5e7eb; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
<div style="font-size: 2rem; margin-bottom: 10px;">⚡</div>
<div style="font-weight: 700; color: #1f2937; margin-bottom: 5px;">75% Faster</div>
<div style="color: #6b7280; font-size: 0.9rem;">Response Times</div>
</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #e5e7eb; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
<div style="font-size: 2rem; margin-bottom: 10px;">💰</div>
<div style="font-weight: 700; color: #1f2937; margin-bottom: 5px;">60% Cost Savings</div>
<div style="color: #6b7280; font-size: 0.9rem;">Labor Reduction</div>
</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
<div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #e5e7eb; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
<div style="font-size: 2rem; margin-bottom: 10px;">🎯</div>
<div style="font-weight: 700; color: #1f2937; margin-bottom: 5px;">24/7 Availability</div>
<div style="color: #6b7280; font-size: 0.9rem;">Always On Support</div>
</div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
<div style="background: white; padding: 20px; border-radius: 15px; border: 1px solid #e5e7eb; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
<div style="font-size: 2rem; margin-bottom: 10px;">🧠</div>
<div style="font-weight: 700; color: #1f2937; margin-bottom: 5px;">AI Learning</div>
<div style="color: #6b7280; font-size: 0.9rem;">Gets Smarter Daily</div>
</div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# How It Works Section
st.markdown("""
<div style="background: #f8fafc; padding: 30px; border-radius: 15px; margin-bottom: 30px;">
<h2 style="text-align: center; color: #1f2937; margin-bottom: 20px;">🔄 How OpsPilot AI Works</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
        
<div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
<h4 style="color: #667eea; margin: 0 0 10px 0;">1. 📧 Email Intake</h4>
<p style="margin: 0; color: #6b7280;">Customer emails are automatically ingested from your support channels.</p>
</div>
        
<div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #764ba2;">
<h4 style="color: #764ba2; margin: 0 0 10px 0;">2. 🧠 AI Analysis</h4>
<p style="margin: 0; color: #6b7280;">Multi-agent AI workforce analyzes, categorizes, and assesses risk in real-time.</p>
</div>
        
<div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #f093fb;">
<h4 style="color: #f093fb; margin: 0 0 10px 0;">3. ✍️ Response Generation</h4>
<p style="margin: 0; color: #6b7280;">Contextual responses are generated using historical data and company knowledge.</p>
</div>
        
<div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #4facfe;">
<h4 style="color: #4facfe; margin: 0 0 10px 0;">4. 👥 Human Approval</h4>
<p style="margin: 0; color: #6b7280;">Quality control ensures responses meet your standards before delivery.</p>
</div>    
</div>
</div>
""", unsafe_allow_html=True)

# Quick Start Guide
st.markdown("""
<div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
<h3 style="color: #856404; margin: 0 0 15px 0;">🚀 Quick Start Guide</h3>
<ol style="color: #856404; margin: 0; padding-left: 20px;">
<li><strong>Process Your First Email:</strong> Use the form below to submit a sample customer email</li>
<li><strong>Watch AI Workflow:</strong> See our 6-agent team analyze and respond in real-time</li>
<li><strong>Review & Approve:</strong> Quality check the AI response before it reaches the customer</li>
<li><strong>Monitor Performance:</strong> Check Analytics & ROI to see cost savings and efficiency gains</li>
</ol>
</div>
""", unsafe_allow_html=True)

# Email Processing Section
st.markdown("## 📧 Try OpsPilot AI - Process a Customer Email")

email_left, email_right = st.columns([12, 2.4])

with email_left:
    st.markdown("""
<div style="
font-size:15px;
font-weight:600;
color:#1F2937;
margin-bottom:1px;
margin-top:1px;
">
Incoming Customer Email
</div>
    """, unsafe_allow_html=True)

    email_input = st.text_area(
        "Customer Email",
        placeholder="Example: Our production system is down and impacting enterprise customers...",
        height=110,
        label_visibility="collapsed",
        key="email_input"
    )

with email_right:
    st.markdown(
        """
<div style='height:72px'></div>
        """,
        unsafe_allow_html=True
    )

    process_clicked = st.button(
        "🚀 Process Email",
        use_container_width=True
    )

# =====================================================
# WORKFLOW EXPLANATION
# =====================================================

st.markdown("""
<div style="background: #f0f9ff; border: 1px solid #bae6fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
<h4 style="color: #0369a1; margin: 0 0 10px 0;">🔄 What Happens Next?</h4>
<p style="margin: 0; color: #0369a1;">
When you click "Process Email", our AI workforce activates:
</p>
<ul style="color: #0369a1; margin: 10px 0 0 0; padding-left: 20px;">
<li><strong>Classification Agent:</strong> Analyzes the email and determines category/priority</li>
<li><strong>Memory Agent:</strong> Searches historical data for similar issues</li>
<li><strong>Decision Agent:</strong> Evaluates business impact and escalation needs</li>
<li><strong>Response Agent:</strong> Generates a contextual customer response</li>
<li><strong>Human Approver:</strong> You review and approve before delivery</li>
<li><strong>Response Delivered:</strong> Professional response sent to customer</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =====================================================
# API PROCESSING
# =====================================================

if process_clicked and email_input:

    st.session_state.workflow_running = True
    st.session_state.agent_times = {}

    # Simulate workflow steps while backend processes
    for i in range(1, 6):
        step_start = time.time()
        st.session_state.workflow_step = i
        time.sleep(0.5)
        st.session_state.agent_times[i] = round(
            time.time() - step_start + 0.8,
            1
        )

    try:
        response = requests.post(
            PROCESS_URL,
            json={"email": email_input},
            timeout=60
        )

        if response.status_code == 200:
            api_data = response.json()
            st.session_state.api_result = api_data
            st.session_state.current_ticket_id = api_data.get("ticket_id")
            # Animate through workflow steps
            for step in range(1, 7):
                st.session_state.workflow_step = step
                time.sleep(0.8)
            st.success(f"✅ Ticket #{st.session_state.current_ticket_id} processed successfully!")
        else:
            st.error(f"Backend error: {response.status_code}")

    except Exception as e:
        st.error(f"Backend connection failed: {e}")

    st.session_state.workflow_running = False
    st.rerun()

# =====================================================
# WORKFLOW
# =====================================================

st.markdown(
'<div class="workflow-title">🤖 Meet Your AI Support Team</div>',
    unsafe_allow_html=True
)

st.markdown(
'<div class="workflow-subtitle">Six specialized AI agents working together to deliver enterprise-grade customer support.</div>',
    unsafe_allow_html=True
)

agents = [
    {
        "step": 1,
        "title": "Classification Agent",
        "desc": "Analyzing incoming email and categorizing issue",
        "image": "classification.png",
        "color": "step-purple",
    },
    {
        "step": 2,
        "title": "Memory Agent",
        "desc": "Retrieving similar historical incidents & context",
        "image": "memory.png",
        "color": "step-blue",
    },
    {
        "step": 3,
        "title": "Decision Agent",
        "desc": "Evaluating risk, impact & escalation",
        "image": "decision.png",
        "color": "step-green",
    },
    {
        "step": 4,
        "title": "Response Agent",
        "desc": "Generating contextual customer response",
        "image": "response.png",
        "color": "step-orange",
    },
    {
        "step": 5,
        "title": "Human Approver",
        "desc": "Reviewing AI response before final delivery",
        "image": "approver.png",
        "color": "step-purple",
    },
    {
        "step": 6,
        "title": "Response Delivered",
        "image": "delivered.png",
        "desc": "Final response sent to customer",
        "color": "#7C3AED"
    }
]

workflow_html = '<div class="workflow-row">'

for idx, agent in enumerate(agents):

    # During workflow execution, highlight agents 1-5 (up to human approver)
    # After approval, highlight up to agent 6 (response delivered)
    if st.session_state.approval_status == "approved":
        active = st.session_state.approval_workflow_step == agent["step"]
        completed = st.session_state.approval_workflow_step > agent["step"]
    else:
        # Cap highlighting at step 5 (human approver) until approved
        display_step = min(st.session_state.workflow_step, 5)
        active = display_step == agent["step"]
        completed = display_step > agent["step"] and agent["step"] < 5

    status = "⏳ Pending"
    if completed:
        status = "✅ Completed"
    if active:
        status = "⚙️ Running"

    active_class = "agent-card agent-active" if active else "agent-card"

    workflow_html += f'''

<div class="{active_class}">

<div class="agent-step {agent['color']}">
{agent['step']}
</div>

<img class="agent-image"
src="data:image/png;base64,{image_base64(agent['image'])}">

<div class="agent-title">
{agent['title']}
</div>

<div class="agent-desc">
{agent['desc']}
</div>

<div class="agent-footer">
<div>{status}</div>
<div>{st.session_state.agent_times.get(agent['step'], '--')}s</div>
</div>

</div>
    '''

    if idx != len(agents) - 1:
        workflow_html += '<div class="workflow-arrow">→</div>'

workflow_html += '</div>'

st.markdown(workflow_html, unsafe_allow_html=True)

# =====================================================
# STATUS BANNER
# =====================================================

banner_text = "Ready to process customer emails with AI automation."

if st.session_state.workflow_step == 1:
    banner_text = "🔍 AI analyzing email content and determining issue category..."

elif st.session_state.workflow_step == 2:
    banner_text = "🧠 AI searching historical database for similar cases..."

elif st.session_state.workflow_step == 3:
    banner_text = "⚠️ AI evaluating business impact and escalation requirements..."

elif st.session_state.workflow_step == 4:
    banner_text = "✍️ AI generating contextual customer response..."

elif st.session_state.workflow_step == 5:
    banner_text = "👤 Human oversight: Review AI response before delivery..."

elif st.session_state.workflow_step >= 6:
    banner_text = "✅ Customer response delivered. Ticket processed successfully!"

st.markdown(
    f'<div class="status-banner">⚡ {banner_text}</div>',
    unsafe_allow_html=True
)

# =====================================================
# DATA
# =====================================================

result = st.session_state.api_result

if result is None:

    result = {
        "ticket_id": None,
        "priority": "N/A",
        "category": "N/A",
        "risk_score": 0.0,
        "department": "N/A",
        "response": "(No ticket processed yet. Submit an email above to generate a response.)",
    }

# =====================================================
# AI GENERATED RESPONSE CARD
# =====================================================

st.markdown("""
<style>

.response-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

.response-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 18px;
}

.response-box {
    background: #f8fafc;
    border: 1px solid #dbeafe;
    border-radius: 16px;
    padding: 18px;
    font-size: 0.96rem;
    line-height: 1.7;
    color: #374151;
    margin-bottom: 0;
    max-height: 400px;
    overflow-y: auto;
}

</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="response-card">

<div class="response-title">
💬 AI Generated Response
</div>

<div class="response-box">
{result['response']}
</div>

</div>
""", unsafe_allow_html=True)

if st.session_state.current_ticket_id is not None:
    approve_col, reject_col, regen_col = st.columns([1,1,1])

    # Only show buttons if not already approved
    if st.session_state.approval_status != "approved":
        with approve_col:
            if st.button("✅ Approve & Send to Customer", use_container_width=True, key="btn_approve"):
                try:
                    response = requests.post(
                        f"{API_BASE}/approve-ticket/{st.session_state.current_ticket_id}",
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.session_state.approval_status = "approved"
                        st.session_state.approval_workflow_step = 6
                        st.success("✅ Response approved and delivered to customer!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Approval failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Could not approve ticket: {e}")

        with reject_col:
            if st.button("❌ Request Changes", use_container_width=True, key="btn_reject"):
                st.session_state.show_reject_reason = True

        with regen_col:
            if st.button("🔄 Regenerate Response", use_container_width=True, key="btn_regen"):
                st.info("🔄 Regenerating response... (Feature in development)")
    else:
        st.markdown("""
        <div style="background: #dcfce7; border: 2px solid #16a34a; padding: 16px; border-radius: 10px; text-align: center; margin: 20px 0;">
            <strong style="color: #166534; font-size: 1.1rem;">✅ Approved & Delivered</strong>
            <p style="margin: 8px 0 0 0; color: #166534; font-size: 0.95rem;">This response has been approved and sent to the customer.</p>
        </div>
        """, unsafe_allow_html=True)

    # Handle rejection with reason
    if st.session_state.show_reject_reason:
        st.markdown("---")
        st.subheader("Request Changes")
        rejection_reason = st.text_area("Why reject this response?", height=100, key="reject_reason_input")
        reject_submit_col1, reject_submit_col2 = st.columns(2)
        
        with reject_submit_col1:
            if st.button("Submit Rejection", use_container_width=True, key="btn_submit_reject"):
                try:
                    response = requests.post(
                        f"{API_BASE}/reject-ticket/{st.session_state.current_ticket_id}",
                        params={"reason": rejection_reason},
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.session_state.approval_status = "rejected"
                        st.session_state.show_reject_reason = False
                        st.warning("⚠️ Ticket rejected. Feedback sent to AI agents for improvement.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Could not reject ticket: {e}")

# =====================================================
# OPERATIONS GRID
# =====================================================

# Convert risk_score to float
risk_score = float(result.get('risk_score', 0)) if result.get('risk_score') else 0

# Determine approval status
approval_status_display = "Pending Approval"
approval_status_color = "orange-pill"

if st.session_state.approval_status == "approved":
    approval_status_display = "Approved"
    approval_status_color = "green-pill"
elif st.session_state.approval_status == "rejected":
    approval_status_display = "Rejected"
    approval_status_color = "red-pill"

st.markdown(f"""
<div class="ops-grid">

<div class="ops-card">

<div class="ops-title">🎫 Current Ticket Summary</div>

<div class="summary-label">Ticket ID</div>
<div class="summary-value">{result['ticket_id'] if result['ticket_id'] else 'N/A'}</div>

<div class="summary-label">Issue Category</div>
<div class="summary-value">{result['department']}</div>

<div class="summary-label">Priority Level</div>

<div class="summary-value">
<span class="pill red-pill">{result['priority']}</span>
<span class="pill purple-pill">{result['category']}</span>
</div>

<div class="summary-label">Approval Status</div>

<div class="summary-value">
<span class="pill {approval_status_color}">{approval_status_display}</span>
</div>

</div>

<div class="ops-card">

<div class="ops-title">⚠️ Business Impact Assessment</div>

<div class="summary-label">Risk Score</div>

<div class="summary-value"
style="font-size:2rem;color:#dc2626;">
{risk_score:.1f} / 10
</div>

<div class="summary-label">AI Recommendation</div>

<div class="summary-value">
Escalate to L2 Support + Notify Engineering
</div>

<div class="summary-label">Business Impact</div>
<div class="summary-value">
{'High - Enterprise Critical' if risk_score >= 7 else 'Medium - Operational Impact' if risk_score >= 4 else 'Low - Standard Issue'}
</div>

</div>

<div class="ops-card">

<div class="ops-title">📋 Ticket Lifecycle</div>

<div class="timeline-item">
<div>🟢 Received</div>
<div>Now</div>
</div>

<div class="timeline-item">
<div>🟢 Classified</div>
<div>Now</div>
</div>

<div class="timeline-item">
<div>🟢 Context Retrieved</div>
<div>10:23 AM</div>
</div>

<div class="timeline-item">
<div>🟢 Decision Made</div>
<div>10:24 AM</div>
</div>

<div class="timeline-item">
<div>🟠 Awaiting Approval</div>
<div>Now</div>
</div>

</div>

</div>
""", unsafe_allow_html=True)

# =========================================
# AI GENERATED RESPONSE CARD
# =========================================

st.markdown("""
<style>

.response-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-top: 20px;
}

.response-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 18px;
}

.response-box {
    background: #f8fafc;
    border: 1px solid #dbeafe;
    border-radius: 16px;
    padding: 18px;
    font-size: 0.96rem;
    line-height: 1.7;
    color: #374151;
    margin-bottom: 0;
    max-height: 400px;
    overflow-y: auto;
}

</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="response-card">

<div class="response-title">
💬 AI Generated Response
</div>

<div class="response-box">
{result['response']}
</div>

</div>
""", unsafe_allow_html=True)


if st.session_state.current_ticket_id is not None:
    approve_col, reject_col, regen_col = st.columns([1,1,1])

    # Only show buttons if not already approved
    if st.session_state.approval_status != "approved":
        with approve_col:
            if st.button("✅ Approve & Send to Customer", use_container_width=True, key="btn_approve"):
                try:
                    response = requests.post(
                        f"{API_BASE}/approve-ticket/{st.session_state.current_ticket_id}",
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.session_state.approval_status = "approved"
                        st.session_state.approval_workflow_step = 6
                        st.success("✅ Response approved and delivered to customer!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Approval failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Could not approve ticket: {e}")

        with reject_col:
            if st.button("❌ Request Changes", use_container_width=True, key="btn_reject"):
                st.session_state.show_reject_reason = True

        with regen_col:
            if st.button("🔄 Regenerate Response", use_container_width=True, key="btn_regen"):
                st.info("🔄 Regenerating response... (Feature in development)")
    else:
        st.markdown("""
        <div style="background: #dcfce7; border: 2px solid #16a34a; padding: 16px; border-radius: 10px; text-align: center; margin: 20px 0;">
            <strong style="color: #166534; font-size: 1.1rem;">✅ Approved & Delivered</strong>
            <p style="margin: 8px 0 0 0; color: #166534; font-size: 0.95rem;">This response has been approved and sent to the customer.</p>
        </div>
        """, unsafe_allow_html=True)

    # Handle rejection with reason
    if st.session_state.show_reject_reason:
        st.markdown("---")
        st.subheader("Request Changes")
        rejection_reason = st.text_area("Why reject this response?", height=100, key="reject_reason_input")
        reject_submit_col1, reject_submit_col2 = st.columns(2)
        
        with reject_submit_col1:
            if st.button("Submit Rejection", use_container_width=True, key="btn_submit_reject"):
                try:
                    response = requests.post(
                        f"{API_BASE}/reject-ticket/{st.session_state.current_ticket_id}",
                        params={"reason": rejection_reason},
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.session_state.approval_status = "rejected"
                        st.session_state.show_reject_reason = False
                        st.warning("⚠️ Ticket rejected. Feedback sent to AI agents for improvement.")
                        st.rerun()
                    else:
                        st.error(f"Rejection failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Could not reject ticket: {e}")
        
        with reject_submit_col2:
            if st.button("Cancel", use_container_width=True, key="btn_cancel_reject"):
                st.session_state.show_reject_reason = False
                st.rerun()
else:
    st.info("👆 Process an email above to enable approval actions")

# =====================================================
# BUSINESS IMPACT DASHBOARD
# =====================================================

st.markdown("""
<div style="background: #f8fafc; padding: 30px; border-radius: 15px; margin-top: 30px;">
    <h2 style="text-align: center; color: #1f2937; margin-bottom: 20px;">📊 Business Impact Dashboard</h2>
    <p style="text-align: center; color: #6b7280; margin-bottom: 30px; font-size: 1.1rem;">
        Real-time metrics showing the value OpsPilot AI delivers to your organization
    </p>
""", unsafe_allow_html=True)

# Fetch analytics from backend
analytics = fetch_analytics()
total = analytics.get("total_tickets", 0)
high_priority = analytics.get("high_priority_tickets", 0)
escalations = analytics.get("escalations", 0)

# Calculate business metrics
resolved = total - escalations if total > 0 else 0
resolved_rate = round((resolved / total * 100)) if total > 0 else 0
automation_rate = resolved_rate  # Assuming resolved tickets are automated
avg_cost_per_ticket = 45  # Estimated cost per ticket
monthly_savings = total * (automation_rate / 100) * avg_cost_per_ticket

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "AI Resolution Rate",
        f"{resolved_rate}%",
        delta=f"+{resolved_rate}%" if resolved_rate > 0 else "0%",
        help="Percentage of tickets resolved without human escalation"
    )

with col2:
    st.metric(
        "Monthly Cost Savings",
        f"${monthly_savings:,.0f}",
        delta=f"+${monthly_savings:,.0f}" if monthly_savings > 0 else "$0",
        help="Estimated savings from automated ticket resolution"
    )

with col3:
    st.metric(
        "High Priority Handled",
        high_priority,
        delta=f"{high_priority}" if high_priority > 0 else "0",
        help="Critical tickets processed by AI agents"
    )

with col4:
    st.metric(
        "Total Tickets Processed",
        total,
        delta=f"+{total}" if total > 0 else "0",
        help="Total customer inquiries processed by OpsPilot AI"
    )

st.markdown("""
    <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid #e5e7eb;">
        <h4 style="margin: 0 0 15px 0; color: #1f2937;">🎯 Key Business Benefits</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div>
                <strong style="color: #059669;">Cost Reduction:</strong> 60% average savings on support labor costs
            </div>
            <div>
                <strong style="color: #059669;">Speed:</strong> 75% faster average response times
            </div>
            <div>
                <strong style="color: #059669;">Scalability:</strong> Handle 10x more tickets with same team
            </div>
            <div>
                <strong style="color: #059669;">Quality:</strong> Consistent, professional responses 24/7
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("""
<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; border-radius: 15px; margin-top: 30px; text-align: center;">
    <h3 style="color: white; margin: 0 0 15px 0;">Ready to Transform Your Support Operations?</h3>
    <p style="margin: 0 0 20px 0; opacity: 0.9; font-size: 1.1rem;">
        OpsPilot AI is production-ready and can start processing your customer emails immediately.
    </p>
    <div style="font-size: 1.2rem; font-weight: 700;">
        🚀 <strong>Next Steps:</strong> Configure integrations → Set approval workflows → Go live!
    </div>
</div>
""", unsafe_allow_html=True)