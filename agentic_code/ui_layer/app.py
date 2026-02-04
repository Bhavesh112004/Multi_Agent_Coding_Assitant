import streamlit as st
import os
import sys

# Maintain logic separation
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(root_path, "src"))

from agentic_code.crew import AgenticCodeCrew

st.set_page_config(page_title="Agentic Code: Project Hub", layout="wide")

# --- ADVANCED CSS FOR NEON UI MATCHING ---
st.markdown("""
    <style>
    /* Remove default Streamlit padding */
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    .main { background-color: #0b0e14; }
    
    /* Header & Circles */
    .header-box { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #1f2937; padding-bottom: 10px; }
    .title-text { font-size: 38px; font-weight: 800; color: #ffffff; text-shadow: 0 0 8px rgba(0, 191, 255, 0.6); margin: 0; }
    .status-group { display: flex; gap: 40px; }
    .neon-circle { width: 50px; height: 50px; border-radius: 50%; border: 4px solid #39FF14; box-shadow: 0 0 15px #39FF14; display: flex; align-items: center; justify-content: center; }
    .busy-circle { width: 50px; height: 50px; border-radius: 50%; border: 4px solid #FF9100; box-shadow: 0 0 15px #FF9100; }
    .status-label { color: #58a6ff; font-weight: bold; font-size: 14px; margin-left: 10px; }

    /* The Center Terminal / Project Box */
    .stTextArea textarea { background-color: #0d1117 !important; color: #39FF14 !important; border: 1px solid #1f6feb !important; box-shadow: 0 0 5px rgba(31, 111, 235, 0.5); font-family: 'Consolas', monospace; }
    
    /* Neon Monitor Cards (Right Side) */
    .monitor-card {
        background: #161b22;
        border: 2px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        position: relative;
    }
    .res-glow { border-left: 6px solid #00BFFF; box-shadow: -4px 0 12px rgba(0, 191, 255, 0.4); }
    .cod-glow { border-left: 6px solid #FFD700; box-shadow: -4px 0 12px rgba(255, 215, 0, 0.4); }
    .rev-glow { border-left: 6px solid #39FF14; box-shadow: -4px 0 12px rgba(57, 255, 20, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- TOP BRANDING & STATUS CIRCLES ---
st.markdown("""
    <div class="header-box">
        <div>
            padding-top: 10px;
            <h1 class="title-text">⚡ Agentic Code: Project Hub</h1>
            <p style="color: #8b949e; margin: 0; font-size: 14px;">Dedicated Developer Interface for AI-Driven Automation</p>
        </div>
        <div class="status-group">
            <div style="display: flex; align-items: center;"><div class="neon-circle"></div><span class="status-label">SYSTEM</span></div>
            <div style="display: flex; align-items: center;"><div class="busy-circle"></div><span class="status-label">AGENT</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN THREE-SECTION LAYOUT ---
col_arch, col_task, col_mon = st.columns([1, 1.8, 1], gap="medium")

# 1. Left: Archive
with col_arch:
    st.subheader("📂 Project Archive")
    results_dir = os.path.join(root_path, "Results")
    if os.path.exists(results_dir):
        folders = sorted([f for f in os.listdir(results_dir)], reverse=True)
        st.selectbox("History", folders, label_visibility="collapsed")
        st.button("📁 OPEN FOLDER", use_container_width=True)
    st.markdown("---")
    st.write("**Project Meta**")
    st.write("- **Framework:** CrewAI")
    st.write("- **Status:** Local Node Ready")

# 2. Middle: Task
# 2. Middle: Task
with col_task:
    st.subheader("🚀 New Agentic Task")
    prompt = st.text_area("Prompt", height=400, label_visibility="collapsed", placeholder="Define your solution...")
    
    if st.button("EXECUTE AGENTIC FLOW", use_container_width=True):
        if prompt:
            with st.status("🛠️ Building...", expanded=True) as status:
                # 1. Run the Crew
                crew_instance = AgenticCodeCrew().crew()
                result = crew_instance.kickoff(inputs={'topic': prompt})
                
                # 2. Import the saving logic from your main.py
                from agentic_code.main import extract_and_save_files
                import datetime

                # 3. Create a unique folder for this run
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                project_dir = os.path.join(root_path, "Results", f"Project_{timestamp}")
                
                # 4. CRITICAL: Pass the agent's output to the saver
                # We use result.raw to get the plain text string
                extract_and_save_files(result.raw, project_dir)
                
                status.update(label="✅ Project Saved to Results!", state="complete")
            st.balloons()
        else:
            st.error("Please enter a prompt.")

# 3. Right: Monitor
with col_mon:
    st.subheader("📡 Real-Time Monitor")
    st.markdown("""
        <div class="monitor-card res-glow">
            <strong style="color: #00BFFF;">🔍 Researcher Agent</strong><br>
            <span style="font-size: 12px; color: #8b949e;">Analyzing Requirements...</span>
        </div>
        <div class="monitor-card cod-glow">
            <strong style="color: #FFD700;">👨‍💻 Coder Agent</strong><br>
            <span style="font-size: 12px; color: #8b949e;">Generating Python Logic...</span>
        </div>
        <div class="monitor-card rev-glow">
            <strong style="color: #39FF14;">🛡️ Reviewer Agent</strong><br>
            <span style="font-size: 12px; color: #8b949e;">Validating YAML Config...</span>
        </div>
    """, unsafe_allow_html=True)