import streamlit as st
import requests
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="OpsPilot AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
.main .block-container {
    max-width: 1420px;
    padding-top: 18px;
    padding-left: 28px;
    padding-right: 28px;
    margin:auto;
}
/* =====================================================
GLOBAL
===================================================== */

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background-color: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081028 0%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* =====================================================
SIDEBAR
===================================================== */

.sidebar-logo {
    color: white;
    font-size: 34px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 35px;
}

.sidebar-item {
    color: #d1d5db;
    padding: 14px 18px;
    border-radius: 14px;
    margin-bottom: 12px;
    font-size: 16px;
    font-weight: 600;
}

.sidebar-active {
    background: linear-gradient(90deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
}

/* =====================================================
HEADER
===================================================== */

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 8px;
}

.main-subtitle {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 20px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #64748b;
    margin-bottom: 25px;
}

/* =====================================================
WORKFLOW CARDS
===================================================== */

.agent-card{
    width:100%;
    height:255px;
    background:#ffffff;
    border:1px solid #E5E7EB;
    border-radius:18px;
    position:relative;
    padding:16px;
    overflow:hidden;
    box-shadow:0 2px 10px rgba(0,0,0,0.04);
}

.agent-card:hover {
    transform: translateY(-4px);
}

.agent-running {
    border: 3px solid #22c55e;
    background: #f0fdf4;
    box-shadow: 0 0 30px rgba(34,197,94,0.18);
}

.agent-number {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    color: white;
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 14px;
}

.agent-image{
    width:92px;
    height:92px;
    object-fit:contain;
    display:block;
    margin:20px auto 12px auto;
}

.agent-name {
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 12px;
}

.agent-desc{
    text-align:center;
    color:#6B7280;
    font-size:11px;
    line-height:1.55;
    padding:0 8px;
    min-height:42px;
}

.agent-status {
    margin-top: 24px;
    font-size: 18px;
    font-weight: 700;
}

.workflow-banner {
    background: #ecfdf5;
    border: 1px solid #86efac;
    border-radius: 14px;
    padding: 14px 20px;
    color: #166534;
    font-weight: 700;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 28px;
}

/* =====================================================
PANELS
===================================================== */

.info-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 12px rgba(15,23,42,0.05);
    min-height: 320px;
}

.info-title {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 18px;
}

.metric-large {
    font-size: 44px;
    font-weight: 800;
    color: #dc2626;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
}

.badge-red {
    background: #fee2e2;
    color: #dc2626;
}

.badge-purple {
    background: #ede9fe;
    color: #7c3aed;
}

.badge-orange {
    background: #ffedd5;
    color: #ea580c;
}

/* =====================================================
KPI CARDS
===================================================== */

.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 12px rgba(15,23,42,0.04);
}

.kpi-number {
    font-size: 40px;
    font-weight: 800;
    color: #111827;
}

.kpi-label {
    color: #64748b;
    font-size: 15px;
    margin-top: 4px;
}

.kpi-trend {
    color: #16a34a;
    font-weight: 700;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
<style>

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top left, #1e3a8a 0%, transparent 30%),
            linear-gradient(180deg, #050816 0%, #081028 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
        width: 290px !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 18px;
        padding-left: 18px;
        padding-right: 18px;
    }

    .sidebar-logo-wrap {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 40px;
        margin-top: 6px;
    }

    .sidebar-logo-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 22px;
        font-weight: 700;
        box-shadow: 0 0 18px rgba(124,58,237,0.45);
    }

    .sidebar-logo-text {
        color: white;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .sidebar-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 18px;
        border-radius: 16px;
        margin-bottom: 10px;
        color: rgba(255,255,255,0.88);
        font-size: 18px;
        font-weight: 600;
        transition: all 0.25s ease;
        cursor: pointer;
    }

    .sidebar-item:hover {
        background: rgba(255,255,255,0.05);
    }

    .sidebar-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .sidebar-icon {
        font-size: 18px;
        width: 22px;
    }

    .sidebar-active {
        background: linear-gradient(90deg, #7c3aed 0%, #6d28d9 100%);
        box-shadow: 0 0 25px rgba(124,58,237,0.45);
    }

    .notification-pill {
        background: #7c3aed;
        color: white;
        min-width: 28px;
        height: 28px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        padding-left: 8px;
        padding-right: 8px;
    }

    .sidebar-footer {
        margin-top: 150px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        padding: 24px;
        background: rgba(255,255,255,0.02);
        backdrop-filter: blur(12px);
    }

    .footer-title {
        color: white;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 18px;
    }

    .footer-status {
        display: flex;
        align-items: center;
        gap: 10px;
        color: rgba(255,255,255,0.92);
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 26px;
    }

    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 999px;
        background: #22c55e;
        box-shadow: 0 0 12px #22c55e;
    }

    .footer-divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin-top: 24px;
        margin-bottom: 24px;
    }

    .footer-quote {
        color: white;
        text-align: center;
        font-size: 16px;
        line-height: 1.6;
        font-weight: 500;
    }

    .footer-bot {
        margin-top: 22px;
        text-align: center;
        font-size: 36px;
    }

</style>
    """, unsafe_allow_html=True)

    # =====================================================
    # LOGO
    # =====================================================

    st.markdown("""
<div class="sidebar-logo-wrap">

<div class="sidebar-logo-icon">
            ✨
</div>

<div class="sidebar-logo-text">
OpsPilot AI
</div>

</div>
    """, unsafe_allow_html=True)

    # =====================================================
    # MENU
    # =====================================================

    menu_items = [
        ("🏠", "Dashboard", True, ""),
        ("📩", "New Email / Ticket", False, ""),
        ("🎫", "All Tickets", False, ""),
        ("☑️", "Approvals", False, "3"),
        ("📊", "Analytics", False, ""),
        ("🕘", "Knowledge Base", False, ""),
        ("⚙️", "Settings", False, ""),
        ("ℹ️", "About", False, "")
    ]

    for icon, label, active, badge in menu_items:

        active_class = "sidebar-item sidebar-active" if active else "sidebar-item"

        badge_html = ""

        if badge:
            badge_html = f'''
<div class="notification-pill">
{badge}
</div>
            '''

        st.markdown(f"""
<div class="{active_class}">

<div class="sidebar-left">

<div class="sidebar-icon">
{icon}
</div>

<div>
{label}
</div>

</div>

{badge_html}

</div>
        """, unsafe_allow_html=True)

    # =====================================================
    # FOOTER CARD
    # =====================================================

    st.markdown("""
      
<div class="sidebar-footer">

<div class="footer-title">
System Status
</div>

<div class="footer-status">

<div class="status-dot"></div>

<div>
All Systems Operational
</div>

</div>

<div class="footer-divider"></div>

<div class="footer-quote">
            “AI + Human<br>
            in the Loop for<br>
            Reliable Operations”
</div>

<div class="footer-bot">
            🤖
</div>

</div>
    """, unsafe_allow_html=True)
# =====================================================
# HEADER
# =====================================================

left, right = st.columns([6, 2])

with left:

    st.markdown(
        '<div class="main-title">OpsPilot AI — Agentic Workflow Automation Platform</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">Intelligent Support Operations. Multi-Agent Orchestration. Smarter Decisions.</div>',
        unsafe_allow_html=True
    )

with right:

    process_clicked = st.button(
        "🚀 Process Email",
        use_container_width=True
    )
st.divider()
customer_email = st.text_area(
    "📩 Incoming Customer Email",
    height=160,
    placeholder="Example: Our production system is down and impacting enterprise customers..."
)

# =====================================================
# AI WORKFORCE SECTION
# =====================================================

st.markdown("""
<div style="
font-size:36px;
font-weight:800;
margin-top:20px;
margin-bottom:4px;
color:#111827;
">
AI WORKFORCE – THE AGENTIC WORKFLOW
</div>

<div style="
color:#667085;
font-size:15px;
margin-bottom:30px;
">
Every agent plays a specialized role in resolving customer issues intelligently.
</div>
""", unsafe_allow_html=True)

# =====================================================
# CARD CSS
# =====================================================

st.markdown("""

<style>

.workflow-wrapper{
    width:100%;
    display:grid;
    grid-template-columns:
        1fr 30px
        1fr 30px
        1fr 30px
        1fr 30px
        1fr 30px
        1fr;
    gap:10px;
    align-items:center;
    margin-top:24px;
}

.workflow-arrow{
    font-size:42px;
    font-weight:700;
    color:#111827;
    text-align:center;
}

.agent-card{
    width:100%;
    height:255px;
    background:#ffffff;
    border:1px solid #E5E7EB;
    border-radius:18px;
    position:relative;
    padding:16px;
    overflow:hidden;
    box-shadow:0 2px 10px rgba(0,0,0,0.04);
}

.agent-active {
    border:2px solid #22c55e;
    box-shadow:
        0 0 20px rgba(34,197,94,0.18);
    background:#fbfffc;
}

.agent-step {
    position:absolute;
    top:14px;
    left:14px;
    width:30px;
    height:30px;
    border-radius:999px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:13px;
    font-weight:700;
}

.step-purple { background:#7c3aed; }
.step-blue { background:#2563eb; }
.step-green { background:#16a34a; }
.step-orange { background:#f97316; }

.running-pill {
    position:absolute;
    top:14px;
    right:14px;
    background:#dcfce7;
    color:#15803d;
    font-size:10px;
    font-weight:700;
    padding:6px 10px;
    border-radius:999px;
    border:1px solid #86efac;
}

.agent-image{
    width:92px;
    height:92px;
    object-fit:contain;
    display:block;
    margin:20px auto 12px auto;
}

.agent-title{
    text-align:center;
    font-size:15px;
    font-weight:800;
    line-height:1.35;
    margin-bottom:8px;
}

.agent-desc{
    text-align:center;
    color:#6B7280;
    font-size:11px;
    line-height:1.55;
    padding:0 8px;
    min-height:42px;
}

.agent-footer {
    position:absolute;
    left:18px;
    right:18px;
    bottom:18px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:12px;
    font-weight:700;
}

.status-complete {
    color:#16a34a;
}

.status-running {
    color:#16a34a;
}

.status-pending {
    color:#6b7280;
}

@media (max-width: 1700px) {

    .workflow-wrapper{
    width:100%;
    display:grid;
    grid-template-columns:
        1fr 30px
        1fr 30px
        1fr 30px
        1fr 30px
        1fr 30px
        1fr;
    gap:10px;
    align-items:center;
    margin-top:24px;
}

    .workflow-arrow{
    font-size:42px;
    font-weight:700;
    color:#111827;
    text-align:center;
}
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# WORKFLOW ROW
# =====================================================

st.markdown(f"""
<div class="workflow-wrapper">
<!-- CARD 1 -->
<div class="agent-card">
<div class="agent-step step-purple">1</div>
<img class="agent-image" src="data:image/png;base64,{get_base64_image('assets/classification.png')}">
<div class="agent-title" style="color:#7c3aed;">
Classification Agent
</div>

<div class="agent-desc">
Analyzing incoming email and categorizing issue
</div>

<div class="agent-footer">

<div class="status-complete">
✅ Completed
</div>

<div>
2.1s
</div>

</div>

</div>

<div class="workflow-arrow">→</div>
<!-- CARD 2 -->
<div class="agent-card">

<div class="agent-step step-blue">2</div>
<img class="agent-image"
src="data:image/png;base64,{get_base64_image('assets/memory.png')}">

<div class="agent-title" style="color:#2563eb;">
Memory Agent
</div>

<div class="agent-desc">
Retrieving similar historical incidents & context (RAG)
</div>

<div class="agent-footer">
<div class="status-complete">
✅ Completed </div>

<div>
3.4s
</div>
</div>
</div>

<div class="workflow-arrow">→</div>
<!-- CARD 3 -->
<div class="agent-card agent-active">

<div class="agent-step step-green">3</div>

<div class="running-pill">
RUNNING
</div>

<img class="agent-image"
src="data:image/png;base64,{get_base64_image('assets/decision.png')}">

<div class="agent-title" style="color:#16a34a;">
Decision Agent
</div>

<div class="agent-desc">
Evaluating risk, impact & determining escalation
</div>

<div class="agent-footer">

<div class="status-running">
⚙️ In Progress...
</div>

<div>
1.8s
</div>

</div>
</div>

<div class="workflow-arrow">→</div>
<!-- CARD 4 -->
<div class="agent-card">

<div class="agent-step step-orange">4</div>

<img class="agent-image"
src="data:image/png;base64,{get_base64_image('assets/response.png')}">
<div class="agent-title" style="color:#f97316;">
Response Agent
</div>

<div class="agent-desc">
Generating contextual response for the customer
</div>

<div class="agent-footer">
<div class="status-pending">
⏳ Pending
</div>

<div>
--
</div>
</div>
</div>

<div class="workflow-arrow">→</div>
<!-- CARD 5 -->
<div class="agent-card">
<div class="agent-step step-purple">5</div>

<img class="agent-image"
src="data:image/png;base64,{get_base64_image('assets/approver.png')}">

<div class="agent-title" style="color:#7c3aed;">
Human<br>Approver
</div>

<div class="agent-desc">
Reviewing AI response before final delivery
</div>

<div class="agent-footer">

<div class="status-pending">
⏳ Pending
</div>

<div>
--
</div>
</div>
</div>

<div class="workflow-arrow">→</div>
<!-- CARD 6 -->
<div class="agent-card">

<img class="agent-image"
style="margin-top:42px;width:145px;height:145px;"
src="data:image/png;base64,{get_base64_image('assets/delivered.png')}">

<div class="agent-title" style="color:#7c3aed;">
Response<br>Delivered
</div>
<div class="agent-desc">
Final response sent to customer
</div>
<div class="agent-footer">
<div class="status-pending">
⏳ Pending
</div>
<div>
--
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# LIVE WORKFLOW STATUS
# =====================================================

st.markdown("""
<style>

.live-status-banner {
    width:100%;
    background:#edfdf3;
    border:1px solid #b7ebc6;
    border-radius:14px;
    padding:18px 24px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:14px;
    margin-top:6px;
    margin-bottom:26px;
    color:#166534;
    font-size:18px;
    font-weight:700;
    box-shadow:0 2px 8px rgba(34,197,94,0.08);
}

.live-status-icon {
    font-size:22px;
}

.operations-grid{
    display:grid;
    grid-template-columns:
        1fr 1fr 1.2fr 1fr;
    gap:18px;
    margin-top:20px;
}

.ops-card {
    background:white;
    border:1px solid #E5E7EB;
    border-radius:20px;
    padding:24px;
    box-shadow:
        0 2px 10px rgba(0,0,0,0.04);
    min-height:355px;
}

.ops-title {
    display:flex;
    align-items:center;
    gap:12px;
    font-size:17px;
    font-weight:800;
    color:#111827;
    margin-bottom:24px;
}

.ops-icon {
    font-size:20px;
}

.summary-grid {
    display:grid;
    grid-template-columns:110px 1fr;
    row-gap:18px;
    column-gap:12px;
    font-size:15px;
}

.summary-label {
    color:#667085;
    font-weight:600;
}

.summary-value {
    color:#111827;
    font-weight:700;
    line-height:1.5;
}

.priority-pill {
    display:inline-block;
    padding:6px 12px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
    background:#fee2e2;
    color:#dc2626;
}

.category-pill {
    display:inline-block;
    padding:6px 12px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
    background:#ede9fe;
    color:#7c3aed;
    margin-left:8px;
}

.status-pill {
    display:inline-block;
    padding:8px 14px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
    background:#ffedd5;
    color:#ea580c;
}

.risk-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    row-gap:24px;
    column-gap:18px;
}

.risk-label {
    color:#667085;
    font-size:14px;
    font-weight:600;
    margin-bottom:10px;
}

.risk-high {
    color:#dc2626;
    font-size:20px;
    font-weight:800;
}

.risk-score {
    color:#dc2626;
    font-size:42px;
    font-weight:800;
    line-height:1;
}

.risk-text {
    color:#111827;
    font-size:15px;
    line-height:1.7;
    font-weight:600;
}

.context-button {
    margin-top:16px;
    width:100%;
    background:#7c3aed;
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:14px;
    font-weight:700;
    cursor:pointer;
}

.response-box {
    border:1px solid #c7d2fe;
    background:#f8fbff;
    border-radius:14px;
    padding:18px;
    font-size:15px;
    line-height:1.75;
    color:#111827;
    min-height:210px;
}

.response-buttons {
    display:flex;
    gap:12px;
    margin-top:18px;
}

.approve-btn {
    flex:1;
    background:#16a34a;
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:14px;
    font-weight:700;
}

.reject-btn {
    flex:1;
    background:white;
    color:#dc2626;
    border:1px solid #fecaca;
    border-radius:12px;
    padding:12px;
    font-size:14px;
    font-weight:700;
}

.regenerate-btn {
    flex:1;
    background:white;
    color:#111827;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:12px;
    font-size:14px;
    font-weight:700;
}

.timeline {
    display:flex;
    flex-direction:column;
    gap:18px;
}

.timeline-row {
    display:flex;
    align-items:flex-start;
    justify-content:space-between;
    gap:14px;
}

.timeline-left {
    display:flex;
    gap:12px;
    align-items:flex-start;
}

.timeline-dot {
    width:12px;
    height:12px;
    border-radius:999px;
    margin-top:6px;
}

.green-dot { background:#22c55e; }
.blue-dot { background:#3b82f6; }
.orange-dot { background:#f59e0b; }
.gray-dot { background:#9ca3af; }

.timeline-text {
    font-size:15px;
    font-weight:700;
    color:#111827;
}

.timeline-time {
    font-size:13px;
    color:#667085;
    white-space:nowrap;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LIVE STATUS
# =====================================================

st.markdown("""
<div class="live-status-banner">

<div class="live-status-icon">
⚡
</div>

<div>
Decision Agent is currently evaluating the issue and determining the best course of action...
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# OPERATIONS GRID
# =====================================================

st.markdown("""
<div class="operations-grid">
<!-- SUMMARY -->
<div class="ops-card">
<div class="ops-title">
📦 Current Ticket Summary
</div>
<div class="summary-grid">

<div class="summary-label">Ticket ID</div>
<div class="summary-value">TCKT-2024-0058</div>
<div class="summary-label">Source</div>
<div class="summary-value">Email</div>
<div class="summary-label">Received At</div>
<div class="summary-value">May 21, 10:24 AM</div>

<div class="summary-label">Subject</div>
<div class="summary-value">
Production system outage affecting enterprise customers
</div>

<div class="summary-label">Priority</div>

<div class="summary-value">
<span class="priority-pill">High</span>
<span class="category-pill">System Outage</span>
</div>

<div class="summary-label">Status</div>

<div class="summary-value">
<span class="status-pill">Pending Approval</span>
</div>

</div>

</div>

<!-- RISK -->

<div class="ops-card">

<div class="ops-title">
🛡️ AI Decision & Risk Assessment
</div>

<div class="risk-grid">

<div>
<div class="risk-label">Business Impact</div>
<div class="risk-high">High</div>
</div>

<div>
<div class="risk-label">Risk Score</div>
<div class="risk-score">8.7 / 10</div>
</div>

</div>

<div style="margin-top:28px;">

<div class="risk-label">
Suggested Action
</div>

<div class="risk-text">
Escalate to L2 Support + Notify Engineering
</div>

</div>

<div style="margin-top:28px;">

<div class="risk-label">
Reasoning
</div>

<div class="risk-text">
High number of customers impacted. Similar incidents in the past caused SLA breach.
</div>

</div>

<div style="margin-top:28px;">

<div class="risk-label">
Similar Incidents Found
</div>

<div class="risk-text">
3
</div>

</div>

<button class="context-button">
View Context
</button>

</div>

<!-- RESPONSE -->

<div class="ops-card">

<div class="ops-title">
💬 AI Generated Response (Preview)
</div>
<div class="response-box">
Dear Customer,<br><br>
We understand that you are experiencing issues with our production system. Our engineering team has been notified and is actively working on resolving the issue. We will provide updates every 30 minutes until the issue is fully resolved.<br><br>
We apologize for the inconvenience caused.<br><br>
Best regards,<br>
OpsPilot AI Support Team
</div>
<div class="response-buttons">

<button class="approve-btn">
✅ Approve & Send
</button>

<button class="reject-btn">
❌ Request Changes
</button>

<button class="regenerate-btn">
🔄 Regenerate
</button>
</div>
</div>

<!-- TIMELINE -->
<div class="ops-card">
<div class="ops-title">
📋 Ticket Lifecycle
</div>
<div class="timeline">
<div class="timeline-row">
<div class="timeline-left">
<div class="timeline-dot green-dot"></div>
<div class="timeline-text">Received</div>
</div>
<div class="timeline-time">
May 21, 10:24 AM
</div>
</div>
<div class="timeline-row">
<div class="timeline-left">
<div class="timeline-dot green-dot"></div>
<div class="timeline-text">Classified</div>
</div>
<div class="timeline-time">
May 21, 10:24 AM
</div>
</div>
<div class="timeline-row">

<div class="timeline-left">
<div class="timeline-dot green-dot"></div>
<div class="timeline-text">Context Retrieved</div>
</div>

<div class="timeline-time">
May 21, 10:24 AM
</div>

</div>

<div class="timeline-row">

<div class="timeline-left">
<div class="timeline-dot blue-dot"></div>
<div class="timeline-text">Decision Made</div>
</div>

<div class="timeline-time">
May 21, 10:25 AM
</div>
</div>

<div class="timeline-row">
<div class="timeline-left">
<div class="timeline-dot orange-dot"></div>
<div class="timeline-text" style="color:#f59e0b;">
Awaiting Approval
</div>
</div>

<div class="timeline-time">
May 21, 10:25 AM
</div>
</div>
<div class="timeline-row">

<div class="timeline-left">
<div class="timeline-dot gray-dot"></div>
<div class="timeline-text">
Delivered
</div>
</div>

<div class="timeline-time">
--
</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)