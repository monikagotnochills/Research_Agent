import streamlit as st
import streamlit.components.v1 as components
import time
import base64
from pathlib import Path
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dwight AI - Research Agent",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Background images → base64 data URIs, cached ────────────────────────────
@st.cache_data(show_spinner=False)
def _bg_data_uri():
    path = Path(__file__).parent / "assets" / "bg.jpg"
    if not path.exists():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/jpeg;base64,{b64}"


@st.cache_data(show_spinner=False)
def _bg_pipeline_data_uri():
    path = Path(__file__).parent / "assets" / "bg_pipeline.jpg"
    if not path.exists():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/jpeg;base64,{b64}"


@st.cache_data(show_spinner=False)
def _blue_capsule_data_uri():
    path = Path(__file__).parent / "assets" / "blue_capsule.png"
    if not path.exists():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/png;base64,{b64}"


BG_URI = _bg_data_uri()
BG_PIPELINE_URI = _bg_pipeline_data_uri()
CAPSULE_URI = _blue_capsule_data_uri()

# ── Autocomplete suggestion data ─────────────────────────────────────────────
TOPIC_SUGGESTIONS = [
    "Quantum Computing breakthroughs in 2025",
    "CRISPR gene editing therapeutics",
    "Fusion energy progress and milestones",
    "AI in healthcare diagnostics",
    "Climate change mitigation technologies",
    "Large Language Models architecture trends",
    "Robotics and autonomous systems",
    "Space exploration and colonization",
    "Brain-computer interface advances",
    "Solid-state battery technology",
    "Cybersecurity threats and zero-trust",
    "Autonomous driving level 5 safety",
    "mRNA vaccines for cancer treatment",
    "DeFi protocols and smart contracts",
    "Metaverse and spatial computing",
]


# ── Design system ────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
  --primary:#1a73e8;
  --primary-active:#1557b0;
  --primary-light:rgba(26,115,232,0.08);
  --on-primary:#ffffff;
  --ink:#0d0d0d;
  --ink-2:#1a1a2e;
  --ink-muted:#4a4a6a;
  --ink-faint:#8b8ba0;
  --surface:rgba(255,255,255,0.85);
  --surface-strong:rgba(255,255,255,0.92);
  --border:rgba(26,115,232,0.12);
  --border-light:rgba(255,255,255,0.6);
  --shadow:0 4px 24px rgba(0,40,120,0.08);
  --shadow-lg:0 8px 40px rgba(0,40,120,0.12);
  --green:#0f9d58;
  --green-bg:rgba(15,157,88,0.06);
  --radius:16px;
  --radius-sm:12px;
  --radius-xs:8px;
  --glass-bg:rgba(255,255,255,0.42);
  --glass-border:rgba(255,255,255,0.5);
  --glass-shadow:0 8px 32px rgba(30,42,120,0.12), inset 0 1px 0 rgba(255,255,255,0.6);
}

/* ── Base ── */
html, body, [class*="css"]{
  font-family:'Plus Jakarta Sans',-apple-system,system-ui,'Segoe UI',sans-serif;
  color:var(--ink);
}

/* Background — swapped dynamically */
.stApp{
  background:
    url("__BG__") center center / cover no-repeat fixed,
    linear-gradient(135deg, #eaf1fb 0%, #dae6f7 100%);
  min-height:100vh;
}

/* Drifting cloud layer */
.sky{ position:fixed; inset:0; z-index:0; pointer-events:none; overflow:hidden; }
.cloud{
  position:absolute; height:90px; opacity:.5; filter:blur(9px);
  background:
    radial-gradient(70px 70px at 70px 55px, rgba(255,255,255,.92), transparent 70%),
    radial-gradient(90px 60px at 145px 48px, rgba(255,255,255,.88), transparent 72%),
    radial-gradient(60px 48px at 205px 60px, rgba(255,255,255,.82), transparent 72%);
  will-change:left, transform;
}
.cloud.c1{ width:260px; top:9%;  animation:drift 95s linear infinite, bob 11s ease-in-out infinite; }
.cloud.c2{ width:380px; top:22%; animation:drift 150s linear infinite -50s, bob 14s ease-in-out infinite -3s; opacity:.36; }
.cloud.c3{ width:200px; top:36%; animation:drift 120s linear infinite -80s, bob 9s ease-in-out infinite -5s; opacity:.44; }
@keyframes drift{ from{ left:-400px; } to{ left:112vw; } }
@keyframes bob{ 0%,100%{ transform:translateY(0); } 50%{ transform:translateY(16px); } }

/* Reusable liquid-glass surface */
.glass{
  background:var(--glass-bg);
  backdrop-filter:blur(18px) saturate(1.5);
  -webkit-backdrop-filter:blur(18px) saturate(1.5);
  border:1px solid var(--glass-border);
  box-shadow:var(--glass-shadow);
}

/* Workspace container */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-workspace_container),
.st-key-workspace_container {
  background: url("__PIPELINE_BG__") center center / cover no-repeat !important;
  border-radius: 24px !important;
  padding: 32px 24px !important;
  margin-top: 2rem !important;
  box-shadow: 0 12px 48px rgba(0,40,120,0.15) !important;
  animation: zoomIn .5s cubic-bezier(0.16,1,0.3,1) both !important;
}

/* Custom spinner */
.spinner-dot {
  width: 16px; height: 16px;
  border: 2.5px solid rgba(26,115,232,0.15);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Suggestion chip buttons */
div[class*="st-key-chip_"] button {
  background: rgba(255,255,255,0.55) !important;
  color: var(--ink-2) !important;
  border: 1.5px solid rgba(26,115,232,0.12) !important;
  border-radius: 20px !important;
  font-size: 0.8rem !important;
  padding: 0.28rem 0.7rem !important;
  font-weight: 600 !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
  transition: all 0.2s ease !important;
  font-family: 'Plus Jakarta Sans',sans-serif !important;
}
div[class*="st-key-chip_"] button:hover {
  background: #fff !important;
  border-color: var(--primary) !important;
  color: var(--primary) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(26,115,232,0.12) !important;
}

#MainMenu, footer, header{ visibility:hidden; }

.block-container{
  padding:1.5rem 3rem 2rem;
  max-width:1200px;
  position:relative;
  z-index:2;
}

/* ── Brand bar ── */
.brand{
  display:flex; align-items:center; gap:.7rem;
  margin:.2rem 0 1.5rem; padding:0;
}
.brand-mark{
  width:42px; height:42px; border-radius:12px;
  background:linear-gradient(135deg, #0d0d0d 0%, #2a2a3e 100%);
  color:#fff;
  display:flex; align-items:center; justify-content:center;
  font-weight:800; font-size:1.2rem; letter-spacing:-.04em;
  box-shadow:0 4px 16px rgba(0,0,0,0.2);
  font-family:'Plus Jakarta Sans',sans-serif;
}
.brand-name{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-weight:800; font-size:1.5rem; letter-spacing:-.03em;
  color:#0d0d0d;
}
.brand-tag{
  margin-left:auto;
  font-size:0.68rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
  color:var(--primary);
  background:var(--glass-bg);
  backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
  border:1px solid var(--glass-border);
  border-radius:9999px; padding:6px 16px;
  font-family:'Plus Jakarta Sans',sans-serif;
}

/* ── Hero section ── */
.hero{
  margin-bottom:1.6rem;
  animation:fadeUp .6s ease both;
}
.hero-eyebrow{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.74rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
  color:var(--primary); margin-bottom:.6rem;
  text-shadow:0 1px 8px rgba(255,255,255,0.8);
}
.hero h1{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:clamp(2rem,4.4vw,3.2rem); font-weight:800; line-height:1.06;
  letter-spacing:-.04em; color:#0d0d0d; margin:0 0 .8rem;
  text-shadow:0 1px 12px rgba(255,255,255,0.6);
}
.hero h1 span{
  background:linear-gradient(135deg, #1a73e8 0%, #6a9cf0 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text;
}
.hero-sub{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.02rem; font-weight:500; line-height:1.65; color:var(--ink-2);
  max-width:640px; margin:0;
  text-shadow:0 1px 10px rgba(255,255,255,0.9);
}
.hero-keywords{
  display:flex; flex-wrap:wrap; gap:8px; margin-top:1.2rem;
}
.hero-kw{
  font-family:'JetBrains Mono',monospace;
  font-size:.68rem; font-weight:500; letter-spacing:.03em;
  color:var(--ink-muted);
  background:rgba(255,255,255,0.5);
  border:1px solid rgba(26,115,232,0.1);
  border-radius:6px; padding:4px 10px;
}

/* ── Input styling ── */
.stTextInput > label{
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:.82rem !important; font-weight:700 !important; color:#0d0d0d !important;
  letter-spacing:.02em;
  text-shadow:0 1px 8px rgba(255,255,255,0.7);
}
.stTextInput > div > div > input{
  background:rgba(255,255,255,0.66) !important;
  backdrop-filter:blur(12px) !important; -webkit-backdrop-filter:blur(12px) !important;
  border:1px solid rgba(255,255,255,0.5) !important;
  border-radius:var(--radius-sm) !important;
  color:#0d0d0d !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:.95rem !important;
  padding:.75rem 1rem !important;
  transition:border-color .2s, box-shadow .2s !important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.5) !important;
}
.stTextInput > div > div > input:focus{
  border-color:var(--primary) !important;
  box-shadow:0 0 0 3px rgba(26,115,232,.15) !important;
}
.stTextInput > div > div{ background:transparent !important; }
.stTextInput input::placeholder{ color:var(--ink-faint) !important; }

/* ── Primary button ── */
.stButton > button{
  background:#0d0d0d !important;
  color:#ffffff !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-weight:600 !important;
  font-size:.95rem !important;
  border:none !important;
  border-radius:9999px !important;
  padding:.7rem 2rem !important;
  width:100%;
  transition:all .2s ease !important;
  box-shadow:0 2px 8px rgba(0,0,0,.15) !important;
  letter-spacing:.01em;
}
.stButton > button:hover{
  background:#1a1a2e !important;
  transform:translateY(-1px) !important;
  box-shadow:0 4px 16px rgba(0,0,0,.2) !important;
}
.stButton > button:active{ transform:scale(.98) !important; }

/* ── Download button ── */
.stDownloadButton > button{
  background:var(--surface-strong) !important;
  color:var(--ink) !important;
  border:1.5px solid var(--border) !important;
  border-radius:9999px !important;
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-weight:600 !important;
  font-size:.88rem !important;
  padding:.55rem 1.4rem !important;
  transition:all .2s ease !important;
}
.stDownloadButton > button:hover{
  background:#fff !important;
  border-color:var(--primary) !important;
}

/* ── Section title ── */
.section-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.72rem; font-weight:700; letter-spacing:.07em;
  color:var(--ink-2); text-transform:uppercase;
  margin:.3rem 0 .8rem;
}

/* ── Pipeline step rows ── */
.step{
  display:flex; align-items:center; gap:.8rem;
  background:var(--surface);
  border:1.5px solid var(--border);
  border-radius:var(--radius); padding:14px 16px; margin-bottom:.5rem;
  box-shadow:var(--shadow);
  transition:all .3s ease;
  animation:fadeUp .4s ease both;
}
.step:hover{ transform:translateY(-1px); box-shadow:var(--shadow-lg); }
.step.active{
  border-color:var(--primary);
  box-shadow:0 0 0 3px rgba(26,115,232,.1), var(--shadow);
  background:rgba(26,115,232,0.03);
}
.step.done{
  border-color:var(--green);
  background:var(--green-bg);
}
.step-dot{
  width:10px; height:10px; border-radius:9999px; flex:0 0 10px;
  background:var(--ink-faint);
  transition:background .3s ease;
}
.step.active .step-dot{
  background:var(--primary);
  animation:pulse 1.2s ease-in-out infinite;
}
.step.done .step-dot{ background:var(--green); }
.step-body{ display:flex; flex-direction:column; gap:2px; min-width:0; flex:1; }
.step-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.88rem; font-weight:600; color:var(--ink);
}
.step-desc{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.74rem; color:var(--ink-muted); font-weight:400;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.step-status{
  margin-left:auto; font-family:'JetBrains Mono',monospace;
  font-size:.65rem; font-weight:600; letter-spacing:.05em;
  flex-shrink:0;
}
.s-wait{ color:var(--ink-faint); }
.s-run{ color:var(--primary); }
.s-done{ color:var(--green); }

/* ── Notification toast ── */
.notification{
  background:var(--surface-strong);
  border:1.5px solid var(--border);
  border-left:4px solid var(--primary);
  border-radius:var(--radius-xs);
  padding:12px 16px;
  margin-bottom:.5rem;
  animation:slideIn .4s ease both;
  box-shadow:var(--shadow);
}
.notification.done{ border-left-color:var(--green); }
.notif-title{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.8rem; font-weight:700; color:var(--ink);
  margin-bottom:2px;
}
.notif-desc{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.74rem; color:var(--ink-muted); font-weight:400;
}
.notif-time{
  font-size:.64rem; color:var(--ink-faint);
  font-family:'JetBrains Mono',monospace;
  margin-top:4px;
}

/* ── Report panel with LIQUID GLASS effect ── */
.report-panel{
  position:relative;
  background:linear-gradient(135deg, rgba(255,255,255,0.48) 0%, rgba(255,255,255,0.18) 100%) !important;
  backdrop-filter:blur(24px) saturate(1.6) !important;
  -webkit-backdrop-filter:blur(24px) saturate(1.6) !important;
  border:1px solid rgba(255,255,255,0.6) !important;
  border-radius:24px;
  padding:36px 32px;
  margin-top:1rem;
  animation:fadeUp .5s ease both;
  box-shadow:
    0 16px 40px rgba(0,40,120,0.08),
    inset 0 1px 0 rgba(255,255,255,0.7),
    inset 0 -1px 3px rgba(120,140,220,0.1) !important;
  z-index:1;
  overflow:hidden;
}
.report-panel::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(circle at 20% 20%, rgba(26,115,232,0.06) 0%, transparent 60%);
  pointer-events: none;
  z-index: -1;
}
.report-panel .panel-label{
  display:inline-flex; align-items:center; gap:.5rem;
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
  margin-bottom:1.2rem; padding-bottom:.8rem;
  border-bottom:1.5px solid var(--border);
  width:100%;
}
.report-panel .panel-label.blue{ color:var(--primary); }
.report-panel .panel-label.green{ color:var(--green); }

/* Professional report typography */
/* Ensure generated research text is dark, readable, and slightly larger */
.report-panel *{ color:#0d0d0d !important; }

.report-panel p{
  font-family:'Source Serif 4','Georgia',serif;
  font-size:1.05rem;
  color:#0d0d0d;
  line-height:1.78;
  margin-bottom:.8rem;
}
.report-panel li{
  font-family:'Source Serif 4','Georgia',serif;
  font-size:1rem;
  color:#0d0d0d;
  line-height:1.72;
  margin-bottom:.3rem;
}
.report-panel code{
  font-family:'JetBrains Mono',monospace;
  font-size:.86rem;
  background:rgba(26,115,232,0.06);
  padding:2px 6px;
  border-radius:4px;
  color:#0d0d0d;
}

.report-panel h1{
  font-family:'Playfair Display','Georgia',serif;
  font-size:1.65rem; font-weight:800; color:#0d0d0d;
  letter-spacing:-.02em; margin:1rem 0 .5rem; line-height:1.25;
}
.report-panel h2{
  font-family:'Playfair Display','Georgia',serif;
  font-size:1.35rem; font-weight:700; color:#1a1a2e;
  letter-spacing:-.01em; margin:1rem 0 .4rem; line-height:1.3;
}
.report-panel h3{
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.05rem; font-weight:700; color:var(--ink-2);
  margin:.8rem 0 .3rem; line-height:1.4;
}
.report-panel p{
  font-family:'Source Serif 4','Georgia',serif;
  font-size:0.98rem; color:#1a1a2e; line-height:1.78;
  margin-bottom:.8rem;
}
.report-panel li{
  font-family:'Source Serif 4','Georgia',serif;
  font-size:.95rem; color:#1a1a2e; line-height:1.72;
  margin-bottom:.3rem;
}
.report-panel a{
  color:var(--primary); text-decoration:underline;
  text-underline-offset:3px; font-weight:500;
}
.report-panel a:hover{ color:var(--primary-active); }
.report-panel ul, .report-panel ol{
  padding-left:1.3rem; margin-bottom:.8rem;
}
.report-panel strong{ font-weight:700; color:#0d0d0d; }
.report-panel code{
  font-family:'JetBrains Mono',monospace;
  font-size:.82rem; background:rgba(26,115,232,0.06);
  padding:2px 6px; border-radius:4px; color:var(--ink-2);
}

/* ── Feedback panel with LIQUID GLASS effect ── */
.feedback-panel{
  position:relative;
  background:linear-gradient(135deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 100%) !important;
  backdrop-filter:blur(24px) saturate(1.6) !important;
  -webkit-backdrop-filter:blur(24px) saturate(1.6) !important;
  border:1px solid rgba(15,157,88,0.22) !important;
  border-radius:24px;
  padding:36px 32px;
  margin-top:1rem;
  animation:fadeUp .5s ease both;
  box-shadow:
    0 16px 40px rgba(15,157,88,0.04),
    inset 0 1px 0 rgba(255,255,255,0.7) !important;
  z-index:1;
  overflow:hidden;
}
.feedback-panel::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(circle at 20% 20%, rgba(15,157,88,0.05) 0%, transparent 60%);
  pointer-events: none;
  z-index: -1;
}
.feedback-panel .panel-label{
  display:inline-flex; align-items:center; gap:.5rem;
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
  margin-bottom:1.2rem; padding-bottom:.8rem;
  border-bottom:1.5px solid rgba(15,157,88,0.15);
  width:100%;
  color:var(--green);
}
.feedback-panel h1, .feedback-panel h2, .feedback-panel h3{
  font-family:'Playfair Display','Georgia',serif; color:#0d0d0d; letter-spacing:-.01em;
}
.feedback-panel p, .feedback-panel li{
  font-family:'Source Serif 4','Georgia',serif;
  font-size:.95rem; color:#1a1a2e; line-height:1.72;
}
.feedback-panel strong{ font-weight:700; color:#0d0d0d; }

/* ── Raw output expander ── */
.raw{
  font-family:'JetBrains Mono',monospace; font-size:.78rem; line-height:1.7;
  color:var(--ink-2); white-space:pre-wrap; word-break:break-word;
}
details summary{
  font-family:'Plus Jakarta Sans',sans-serif !important;
  font-size:.82rem !important; color:var(--ink-2) !important;
  cursor:pointer; font-weight:600;
}
[data-testid="stExpander"]{
  background:var(--surface) !important;
  border:1.5px solid var(--border) !important;
  border-radius:var(--radius-sm) !important;
}

/* ── Footer ── */
.footer{
  font-family:'Plus Jakarta Sans',sans-serif;
  text-align:center; font-size:.74rem; color:var(--ink-muted); font-weight:500;
  margin-top:2rem; padding-top:1rem;
  border-top:1px solid var(--border);
  letter-spacing:.02em;
}

/* ── Spinner / alerts ── */
.stSpinner > div{ border-top-color:var(--primary) !important; }
[data-testid="stAlert"]{
  background:var(--surface-strong) !important;
  border:1.5px solid var(--border) !important;
  border-radius:var(--radius-sm) !important;
}

/* ── 3D Cube Loader ── */
.cube-loader-wrap{
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  height:240px; position:relative; margin-bottom:20px;
}
.cubes{
  position:relative;
  transform-style:preserve-3d;
}
.loop{
  transform:rotateX(-35deg) rotateY(-45deg) translateZ(1.5625em);
}
@keyframes s{
  to{ transform:scale3d(0.2,0.2,0.2); }
}
.item{
  margin:-1.5625em;
  width:3.125em; height:3.125em;
  transform-origin:50% 50% -1.5625em;
  box-shadow:0 0 0.125em currentColor;
  background:currentColor;
  animation:s 0.6s cubic-bezier(0.45,0.03,0.51,0.95) infinite alternate;
}
.item:before, .item:after{
  position:absolute; width:inherit; height:inherit;
  transform-origin:0 100%;
  box-shadow:inherit; background:currentColor; content:"";
}
.item:before{ bottom:100%; transform:rotateX(90deg); }
.item:after{ left:100%; transform:rotateY(90deg); }
.item:nth-child(1){ margin-top:6.25em; color:#1a73e8; animation-delay:-1.2s; }
.item:nth-child(1):before{ color:#4a90d9; }
.item:nth-child(1):after{ color:#3182ce; }
.item:nth-child(2){ margin-top:3.125em; color:#2b6cb0; animation-delay:-1s; }
.item:nth-child(2):before{ color:#5a9bd5; }
.item:nth-child(2):after{ color:#4090c0; }
.item:nth-child(3){ margin-top:0em; color:#3182ce; animation-delay:-0.8s; }
.item:nth-child(3):before{ color:#6aabdf; }
.item:nth-child(3):after{ color:#4e9cd4; }
.item:nth-child(4){ margin-top:-3.125em; color:#4a90d9; animation-delay:-0.6s; }
.item:nth-child(4):before{ color:#80b8e6; }
.item:nth-child(4):after{ color:#65a4df; }
.item:nth-child(5){ margin-top:-6.25em; color:#63a3e0; animation-delay:-0.4s; }
.item:nth-child(5):before{ color:#96c5ec; }
.item:nth-child(5):after{ color:#7cb4e6; }
.item:nth-child(6){ margin-top:-9.375em; color:#80b8e6; animation-delay:-0.2s; }
.item:nth-child(6):before{ color:#b0d4f1; }
.item:nth-child(6):after{ color:#98c8ec; }

/* Status text BELOW the loader */
.loader-status{
  text-align:center;
  margin-top:10px;
  animation:fadeUp .4s ease both;
  width:100%;
}
.loader-status-text{
  display:inline-flex; align-items:center; justify-content:center; gap:0.5rem;
  font-family:'Plus Jakarta Sans','Inter',sans-serif;
  font-size:.88rem; font-weight:600; color:var(--ink);
}
.loader-status-done{
  font-family:'Plus Jakarta Sans','Inter',sans-serif;
  font-size:.88rem; font-weight:600; color:var(--green);
  text-align:center;
}

/* ── Animations ── */
@keyframes zoomIn{
  from{ opacity:0; transform:scale(0.92) translateY(20px); }
  to{ opacity:1; transform:scale(1) translateY(0); }
}
@media (hover:hover){ html, body, .stApp{ cursor:none; } }
@keyframes fadeUp{
  from{ opacity:0; transform:translateY(8px); }
  to{ opacity:1; transform:none; }
}
@keyframes slideIn{
  from{ opacity:0; transform:translateX(-12px); }
  to{ opacity:1; transform:none; }
}
@keyframes pulse{
  0%,100%{ box-shadow:0 0 0 0 rgba(26,115,232,.5); }
  50%{ box-shadow:0 0 0 6px rgba(26,115,232,0); }
}

/* ── Responsive — Mobile Friendly ── */
@media (max-width:1024px){
  .block-container{ padding:1rem 1.4rem 1.4rem; }
  .hero h1{ font-size:clamp(1.7rem,6vw,2.4rem); }
  .report-panel, .feedback-panel{ padding:24px 18px; }
  .step{ padding:12px 14px; gap:.6rem; }
  .step-desc{ white-space:normal; }
  div[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-workspace_container),
  .st-key-workspace_container { padding:24px 16px !important; }
}
@media (max-width:640px){
  .block-container{ padding:.6rem .8rem 1rem; }
  .brand-tag{ display:none; }
  .brand-name{ font-size:1.2rem; }
  .brand-mark{ width:36px; height:36px; font-size:1rem; }
  [data-testid="column"]{ width:100% !important; flex:1 1 100% !important; }
  .report-panel, .feedback-panel{ padding:18px 14px; border-radius:14px; }
  .hero h1{ font-size:clamp(1.5rem,7vw,2rem); }
  .hero-sub{ font-size:.92rem; }
  .hero-keywords{ gap:6px; }
  .hero-kw{ font-size:.62rem; padding:3px 8px; }
  .step{ padding:10px 12px; gap:.5rem; border-radius:12px; }
  .step-title{ font-size:.82rem; }
  .step-desc{ font-size:.7rem; }
  .step-status{ font-size:.6rem; }
  .notification{ padding:10px 14px; }
  .notif-title{ font-size:.76rem; }
  .notif-desc{ font-size:.7rem; }
  .cube-loader-wrap{ padding:12px 0; height:200px; }
  .loader-status{ margin-top:0px; padding-top:10px; }
  .loader-status-text{ font-size:.8rem; }
  div[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-workspace_container),
  .st-key-workspace_container { padding:16px 10px !important; border-radius:16px !important; margin-top:1rem !important; }
}

@media (prefers-reduced-motion:reduce){
  *{ animation:none !important; transition:none !important; }
}
</style>
"""

# ── Render CSS with dynamic background ────────────────────────────────────────
current_bg = BG_PIPELINE_URI if st.session_state.get("page", "home") == "pipeline" else BG_URI
_pipeline_bg = BG_PIPELINE_URI if BG_PIPELINE_URI else ""
st.markdown(
    _CSS.replace("__BG__", current_bg).replace("__PIPELINE_BG__", _pipeline_bg),
    unsafe_allow_html=True,
)

# ── Liquid-glass cursor ──────────────────────────────────────────────────────
components.html("""
<script>
const doc = window.parent.document;
if (!doc.getElementById('lg-cursor')) {
  const ring = doc.createElement('div'); ring.id = 'lg-cursor';
  const dot  = doc.createElement('div'); dot.id  = 'lg-cursor-dot';
  doc.body.appendChild(ring); doc.body.appendChild(dot);
  const s = doc.createElement('style');
  s.textContent = `
    #lg-cursor{position:fixed;left:0;top:0;width:30px;height:30px;border-radius:9px;
      transform:translate(-50%,-50%) rotate(0deg);pointer-events:none;z-index:2147483647;
      background:linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.03) 50%, rgba(255,255,255,0.08) 100%);
      backdrop-filter:blur(1px) saturate(1.25) brightness(1.04);
      -webkit-backdrop-filter:blur(1px) saturate(1.25) brightness(1.04);
      border:1px solid rgba(255,255,255,0.45);
      box-shadow:0 4px 14px rgba(50,60,150,0.14),inset 0 1px 1px rgba(255,255,255,0.8),inset 0 -1px 3px rgba(120,140,220,0.18);
      transition:width .18s ease,height .18s ease,border-radius .18s ease,transform .2s ease;}
    #lg-cursor::before{content:'';position:absolute;inset:0;border-radius:inherit;
      background:linear-gradient(135deg, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0) 42%);
      mix-blend-mode:screen;pointer-events:none;}
    #lg-cursor-dot{display:none;}
    @media (hover:none){#lg-cursor,#lg-cursor-dot{display:none;}}
  `;
  doc.head.appendChild(s);
  let x=innerWidth/2, y=innerHeight/2, rx=x, ry=y;
  doc.addEventListener('mousemove', e => { x=e.clientX; y=e.clientY; dot.style.left=x+'px'; dot.style.top=y+'px'; });
  (function loop(){ rx+=(x-rx)*0.35; ry+=(y-ry)*0.35;
    ring.style.left=rx+'px'; ring.style.top=ry+'px'; requestAnimationFrame(loop); })();
  doc.addEventListener('mouseover', e => {
    const hot = !!e.target.closest('button,a,.chip,input,textarea,summary,[role="button"]');
    ring.style.width = hot? '50px':'34px'; ring.style.height = hot? '50px':'34px';
    ring.style.borderRadius = hot? '14px':'10px';
  });
  doc.addEventListener('mousedown', ()=>{ ring.style.transform = 'translate(-50%,-50%) rotate(8deg) scale(0.82)'; });
  doc.addEventListener('mouseup', ()=>{ ring.style.transform = 'translate(-50%,-50%) rotate(0deg) scale(1)'; });
}
</script>
""", height=0)

# ── JS-driven clouds ─────────────────────────────────────────────────────────
components.html("""
<script>
const doc = window.parent.document;
if (!doc.getElementById('js-clouds')) {
  const layer = doc.createElement('div'); layer.id = 'js-clouds';
  layer.style.cssText = 'position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;';
  doc.body.insertBefore(layer, doc.body.firstChild);
  const defs = [
    {w:300, top:0.10, spd:45, amp:18, bs:0.35, op:0.50, blur:9},
    {w:440, top:0.24, spd:32, amp:26, bs:0.22, op:0.36, blur:11},
    {w:240, top:0.40, spd:60, amp:14, bs:0.45, op:0.44, blur:8},
  ];
  const W = () => window.parent.innerWidth;
  const H = () => window.parent.innerHeight;
  const clouds = defs.map((d, i) => {
    const el = doc.createElement('div');
    el.style.cssText =
      'position:absolute;height:90px;will-change:transform;opacity:'+d.op+
      ';filter:blur('+d.blur+'px);width:'+d.w+'px;background:'+
      'radial-gradient(70px 70px at 70px 55px, rgba(255,255,255,.92), transparent 70%),'+
      'radial-gradient(90px 60px at 145px 48px, rgba(255,255,255,.88), transparent 72%),'+
      'radial-gradient(60px 48px at 205px 60px, rgba(255,255,255,.82), transparent 72%);';
    layer.appendChild(el);
    return {el, d, x: (W()+d.w) * (i/defs.length) - d.w, phase: i*1.7};
  });
  let last = performance.now();
  (function tick(now){
    const dt = Math.min(0.05, (now - last)/1000); last = now;
    const t = now/1000;
    for (const c of clouds){
      c.x -= c.d.spd * dt;
      if (c.x < -c.d.w) c.x = W() + c.d.w;
      const y = c.d.top * H() + Math.sin(t*c.d.bs + c.phase) * c.d.amp;
      c.el.style.transform = 'translate('+c.x+'px,'+y+'px)';
    }
    requestAnimationFrame(tick);
  })(last);
}
</script>
""", height=0)

# ── Dynamic Autocomplete datalist injection into parent document ─────────────
components.html("""
<script>
const doc = window.parent.document;
const suggestions = [
  "Quantum Computing breakthroughs in 2025",
  "CRISPR gene editing therapeutics",
  "Fusion energy progress and milestones",
  "AI in healthcare diagnostics",
  "Climate change mitigation technologies",
  "Large Language Models architecture trends",
  "Robotics and autonomous systems",
  "Space exploration and colonization",
  "Brain-computer interface advances",
  "Solid-state battery technology",
  "Cybersecurity threats and zero-trust",
  "Autonomous driving level 5 safety",
  "mRNA vaccines for cancer treatment",
  "DeFi protocols and smart contracts",
  "Metaverse and spatial computing"
];
function bindDatalist() {
  const input = doc.querySelector('input[data-testid="stTextInputInput"]');
  if (input) {
    let datalist = doc.getElementById('topic-datalist');
    if (!datalist) {
      datalist = doc.createElement('datalist');
      datalist.id = 'topic-datalist';
      suggestions.forEach(item => {
        const option = doc.createElement('option');
        option.value = item;
        datalist.appendChild(option);
      });
      doc.body.appendChild(datalist);
    }
    input.setAttribute('list', 'topic-datalist');
    input.setAttribute('autocomplete', 'on');
  }
}
// Run repeatedly to account for Streamlit rerenders
setInterval(bindDatalist, 500);
</script>
""", height=0)


# ── Pipeline definition ───────────────────────────────────────────────────────
STEPS = [
    ("search", "Search Agent", "Discovers relevant web sources, articles, and references for the research topic."),
    ("reader", "Reader Agent", "Extracts and analyzes deep content from selected references."),
    ("writer", "Writer Agent", "Drafts a structured, synthesized, and sourced research report."),
    ("critic", "Critic Agent", "Reviews the draft for accuracy, consistency, and depth."),
]
STEP_KEYS = [s[0] for s in STEPS]

STEP_NOTIFICATIONS = {
    "search_start": ("Search Agent Activated", "Discovering relevant web sources, articles, and references for the research topic."),
    "search_done":  ("Search Agent Complete", "Successfully gathered authoritative sources and research material."),
    "reader_start": ("Reader Agent Activated", "Extracting and analyzing deep content from selected references."),
    "reader_done":  ("Reader Agent Complete", "Key insights extracted and processed from all sources."),
    "writer_start": ("Writer Agent Activated", "Drafting a structured, synthesized, and sourced research report."),
    "writer_done":  ("Writer Agent Complete", "Research narrative synthesized and report drafted."),
    "critic_start": ("Critic Agent Activated", "Reviewing the draft for accuracy, consistency, and depth."),
    "critic_done":  ("Critic Agent Complete", "Content reviewed for factual accuracy. Final assessment ready."),
}


def step_state(key):
    """Resolve the visual state of a pipeline step from session results."""
    r = st.session_state.results
    if key in r:
        return "done"
    if st.session_state.running:
        for k in STEP_KEYS:
            if k not in r:
                return "running" if k == key else "waiting"
    return "waiting"


def render_pipeline():
    label = {
        "waiting": ("WAITING", "s-wait"),
        "running": ("RUNNING", "s-run"),
        "done":    ("DONE",    "s-done"),
    }
    for key, title, desc in STEPS:
        state = step_state(key)
        txt, cls = label[state]
        card_cls = {"running": "active", "done": "done"}.get(state, "")
        st.markdown(f"""
        <div class="step {card_cls}">
            <div class="step-dot"></div>
            <div class="step-body">
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
            <div class="step-status {cls}">{txt}</div>
        </div>
        """, unsafe_allow_html=True)


def render_notification(key, is_done=False):
    """Render a notification toast for a pipeline step."""
    suffix = "_done" if is_done else "_start"
    notif_key = key + suffix
    if notif_key in STEP_NOTIFICATIONS:
        title, desc = STEP_NOTIFICATIONS[notif_key]
        done_cls = "done" if is_done else ""
        timestamp = time.strftime("%H:%M:%S")
        st.markdown(f"""
        <div class="notification {done_cls}">
            <div class="notif-title">{title}</div>
            <div class="notif-desc">{desc}</div>
            <div class="notif-time">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)


def render_cube_loader():
    """Render the 3D cube loading animation."""
    st.markdown("""
    <div class="cube-loader-wrap">
        <div class="loop cubes">
            <div class="item cubes"></div>
            <div class="item cubes"></div>
            <div class="item cubes"></div>
            <div class="item cubes"></div>
            <div class="item cubes"></div>
            <div class="item cubes"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "done", "pipeline_started", "page", "topic_input_value"):
    if key not in st.session_state:
        if key == "results":
            st.session_state[key] = {}
        elif key == "page":
            st.session_state[key] = "home"
        elif key == "topic_input_value":
            st.session_state[key] = ""
        else:
            st.session_state[key] = False


# ── Brand bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand">
    <div class="brand-mark">D</div>
    <div class="brand-name">Dwight AI</div>
    <div class="brand-tag">Multi-Agent Research</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Autonomous Multi-Agent Research Pipeline</div>
        <h1>Your next-level<br><span>research engine.</span></h1>
        <p class="hero-sub">
            Dwight AI orchestrates four specialised agents &mdash; search, read, write, and critique
            &mdash; that collaborate in sequence to transform any topic into a polished, well-sourced
            research report in minutes, not hours.
        </p>
        <div class="hero-keywords">
            <span class="hero-kw">Multi-Agent</span>
            <span class="hero-kw">LangChain</span>
            <span class="hero-kw">Deep Research</span>
            <span class="hero-kw">Auto-Sourced</span>
            <span class="hero-kw">AI Critic</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input area ──
    topic = st.text_input(
        "Research Topic",
        value=st.session_state.topic_input_value,
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
    )

    # Quick topic chips
    st.markdown('<div style="font-size:0.74rem; font-weight:600; color:var(--ink-muted); margin-top:0.9rem; margin-bottom:0.3rem; letter-spacing:.03em;">QUICK START</div>', unsafe_allow_html=True)
    cols_chips = st.columns(4)
    chips = ["Quantum Computing", "CRISPR Gene Editing", "Fusion Energy", "AI in Healthcare"]

    chip_clicked = False
    clicked_chip_name = ""
    for i, chip_name in enumerate(chips):
        with cols_chips[i]:
            if st.button(chip_name, key=f"chip_{i}", use_container_width=True):
                chip_clicked = True
                clicked_chip_name = chip_name

    run_btn = st.button("Run Research Pipeline", use_container_width=True)

    if run_btn or chip_clicked:
        target_topic = clicked_chip_name if chip_clicked else topic
        if not target_topic or not target_topic.strip():
            st.warning("Please enter a research topic first.")
        else:
            st.session_state.topic_input_value = target_topic
            st.session_state.results = {}
            st.session_state.running = True
            st.session_state.done = False
            st.session_state.page = "pipeline"
            st.session_state.pipeline_started = True
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PIPELINE (Running)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "pipeline":
    with st.container(key="workspace_container"):
        topic_val = st.session_state.topic_input_value

        st.markdown(f"""
        <div style="margin-bottom:1.2rem; text-align:center;">
            <div style="font-family:'Plus Jakarta Sans','Inter',sans-serif; font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:#0d0d0d; margin-bottom:.3rem;">RESEARCH WORKSPACE</div>
            <div style="font-family:'Plus Jakarta Sans','Inter',sans-serif; font-size:1.4rem; font-weight:800; color:#0d0d0d; letter-spacing:-.03em;">{topic_val}</div>
        </div>
        """, unsafe_allow_html=True)

        # Side-by-side layout: pipeline on left, loader on right
        col_left, col_right = st.columns([6, 4])

        with col_left:
            # Blue capsule next to/above pipeline
            st.markdown(f"""
            <div class="blue-capsule-container">
                <img src="{CAPSULE_URI}" style="width:100%; height:12px; border-radius:9999px; display:block; margin-bottom:1rem;" />
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="section-title">Agent Pipeline</div>', unsafe_allow_html=True)
            pipeline_container = st.container()
            with pipeline_container:
                render_pipeline()

            st.markdown('<div class="section-title" style="margin-top:1.5rem;">Agent Activity</div>', unsafe_allow_html=True)
            notif_placeholder = st.empty()

        with col_right:
            st.markdown('<div class="section-title" style="text-align:center;">Agent Progress</div>', unsafe_allow_html=True)
            loader_container = st.container()
            with loader_container:
                render_cube_loader()

            # Active status spinner inside the right column below the loader
            # (kept separate so Streamlit's UI notifications don't appear above)
            status_container = st.empty()
            # Push the status text further down so it sits clearly below the cube loader
            st.markdown('<div style="height:90px"></div>', unsafe_allow_html=True)



        # ── Execute pipeline ──
        results = {}

        try:
            # Step 1 — Search
            with notif_placeholder.container():
                render_notification("search", is_done=False)
            status_container.markdown('<div class="loader-status"><div class="loader-status-text"><div class="spinner-dot"></div>Search Agent is gathering sources...</div></div>', unsafe_allow_html=True)

            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
            })
            results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(results)

            with notif_placeholder.container():
                render_notification("search", is_done=True)
            status_container.markdown('<div class="loader-status"><div class="loader-status-done">Search Agent completed</div></div>', unsafe_allow_html=True)
            time.sleep(1)

            # Step 2 — Reader
            with notif_placeholder.container():
                render_notification("reader", is_done=False)
            status_container.markdown('<div class="loader-status"><div class="loader-status-text"><div class="spinner-dot"></div>Reader Agent is extracting insights...</div></div>', unsafe_allow_html=True)

            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(results)

            with notif_placeholder.container():
                render_notification("reader", is_done=True)
            status_container.markdown('<div class="loader-status"><div class="loader-status-done">Reader Agent completed</div></div>', unsafe_allow_html=True)
            time.sleep(1)

            # Step 3 — Writer
            with notif_placeholder.container():
                render_notification("writer", is_done=False)
            status_container.markdown('<div class="loader-status"><div class="loader-status-text"><div class="spinner-dot"></div>Writer Agent is drafting the report...</div></div>', unsafe_allow_html=True)

            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic": topic_val, "research": research_combined
            })
            st.session_state.results = dict(results)

            with notif_placeholder.container():
                render_notification("writer", is_done=True)
            status_container.markdown('<div class="loader-status"><div class="loader-status-done">Writer Agent completed</div></div>', unsafe_allow_html=True)
            time.sleep(1)

            # Step 4 — Critic
            with notif_placeholder.container():
                render_notification("critic", is_done=False)
            status_container.markdown('<div class="loader-status"><div class="loader-status-text"><div class="spinner-dot"></div>Critic Agent is reviewing the report...</div></div>', unsafe_allow_html=True)

            results["critic"] = critic_chain.invoke({"report": results["writer"]})
            st.session_state.results = dict(results)

            with notif_placeholder.container():
                render_notification("critic", is_done=True)
            status_container.markdown('<div class="loader-status"><div class="loader-status-done">Critic Agent completed</div></div>', unsafe_allow_html=True)
            time.sleep(1)

            st.session_state.running = False
            st.session_state.done = True
            st.session_state.page = "results"
            st.rerun()

        except Exception as e:
            st.session_state.running = False
            st.error(f"Pipeline failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "results":
    # Hero (compact)
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Research Complete</div>
        <h1>Your <span>research report</span><br>is ready.</h1>
    </div>
    """, unsafe_allow_html=True)

    st.text_input(
        "Research Topic",
        value=st.session_state.topic_input_value,
        disabled=True,
        key="topic_input_disabled",
    )

    # Results workspace
    with st.container(key="workspace_container"):
        topic_val = st.session_state.topic_input_value
        st.markdown(f"""
        <div style="margin-bottom:1.2rem; text-align:center;">
            <div style="font-family:'Plus Jakarta Sans','Inter',sans-serif; font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:#0d0d0d; margin-bottom:.3rem;">RESEARCH DELIVERABLES</div>
            <div style="font-family:'Plus Jakarta Sans','Inter',sans-serif; font-size:1.4rem; font-weight:800; color:#0d0d0d; letter-spacing:-.03em;">{topic_val}</div>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([4, 6])
        r = st.session_state.results

        with col_left:
            # Blue capsule next to/above pipeline
            st.markdown(f"""
            <div class="blue-capsule-container">
                <img src="{CAPSULE_URI}" style="width:100%; height:12px; border-radius:9999px; display:block; margin-bottom:1rem;" />
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="section-title">Agent Pipeline</div>', unsafe_allow_html=True)
            render_pipeline()

            st.markdown('<div class="section-title" style="margin-top:1.2rem;">Agent Activity</div>', unsafe_allow_html=True)
            render_notification("search", is_done=True)
            render_notification("reader", is_done=True)
            render_notification("writer", is_done=True)
            render_notification("critic", is_done=True)

        with col_right:
            st.markdown('<div class="section-title">Research Report</div>', unsafe_allow_html=True)

            if "writer" in r:
                st.markdown(
                    '<div class="report-panel">'
                    '<div class="panel-label blue">Final Research Report</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(r["writer"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    "Download Report (.md)",
                    data=r["writer"],
                    file_name=f"dwight_ai_report_{int(time.time())}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            if "critic" in r:
                st.markdown(
                    '<div class="feedback-panel">'
                    '<div class="panel-label">Critic Assessment</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(r["critic"])
                st.markdown("</div>", unsafe_allow_html=True)

            if "search" in r:
                with st.expander("Search results (raw)"):
                    st.markdown(f'<div class="raw">{r["search"]}</div>', unsafe_allow_html=True)

            if "reader" in r:
                with st.expander("Scraped content (raw)"):
                    st.markdown(f'<div class="raw">{r["reader"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start New Research", use_container_width=True):
            st.session_state.results = {}
            st.session_state.running = False
            st.session_state.done = False
            st.session_state.pipeline_started = False
            st.session_state.page = "home"
            st.session_state.topic_input_value = ""
            st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">Dwight AI &mdash; Autonomous multi-agent research assistant</div>
""", unsafe_allow_html=True)
