import streamlit as st
import pandas as pd

from rag_llm import ask_tutor
from auto_grader import grade_code
from concept_analytics import compute_mastery
from file_loader import load_pdf, load_image
from ingest import ingest_raw_text
from trace_db import init_db
from quiz_generator import generate_adaptive_quiz

init_db()

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="CodeTutor AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Claude-inspired CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* ── App background ── */
.stApp {
    background-color: #1a1a1a;
    color: #e8e3dc;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #141414 !important;
    border-right: 1px solid #2a2a2a !important;
}
[data-testid="stSidebar"] * {
    color: #c9c3bc !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* ── Sidebar brand ── */
.brand-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e8e3dc !important;
    letter-spacing: -0.02em;
    padding: 0.25rem 0;
}

/* ── Nav radio ── */
[data-testid="stRadio"] label {
    font-size: 0.85rem !important;
    color: #9a9490 !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    transition: background 0.15s;
}
[data-testid="stRadio"] label:hover {
    background: #242424 !important;
    color: #e8e3dc !important;
}
[data-testid="stRadio"] [aria-checked="true"] + label,
[data-testid="stRadio"] [data-checked="true"] label {
    background: #2a2a2a !important;
    color: #e8e3dc !important;
}

/* ── Main content area ── */
.main .block-container {
    padding: 2rem 2.5rem 4rem 2.5rem;
    max-width: 900px;
}

/* ── Page header ── */
.page-header {
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #2a2a2a;
}
.page-header h1 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #e8e3dc;
    letter-spacing: -0.03em;
    margin: 0;
}
.page-header p {
    font-size: 0.82rem;
    color: #6b6560;
    margin: 4px 0 0 0;
}

/* ── Language pill buttons ── */
.stButton button {
    background: #242424 !important;
    border: 1px solid #2e2e2e !important;
    color: #9a9490 !important;
    border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
    padding: 0.35rem 0.75rem !important;
}
.stButton button:hover {
    background: #2e2e2e !important;
    border-color: #3a3a3a !important;
    color: #e8e3dc !important;
}
[data-testid="baseButton-primary"] {
    background: #cc785c !important;
    border-color: #cc785c !important;
    color: #fff !important;
}
[data-testid="baseButton-primary"]:hover {
    background: #b86a50 !important;
    border-color: #b86a50 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.75rem 0 !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: #222222 !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.5rem !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #242424 !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 12px !important;
    color: #e8e3dc !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #cc785c !important;
    box-shadow: 0 0 0 3px rgba(204,120,92,0.12) !important;
}
[data-testid="stChatInput"] textarea {
    color: #e8e3dc !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.9rem !important;
}

/* ── Text areas & inputs ── */
.stTextArea textarea, .stTextInput input {
    background: #1e1e1e !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 8px !important;
    color: #e8e3dc !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #cc785c !important;
    box-shadow: 0 0 0 3px rgba(204,120,92,0.12) !important;
}

/* ── Code blocks ── */
.stCode, code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: #1e1e1e !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 1rem 1.25rem;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    color: #6b6560 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    color: #e8e3dc !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #1e1e1e !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #9a9490 !important;
    font-size: 0.85rem !important;
}

/* ── Alerts ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    border: none !important;
}
.stSuccess { background: #1a2e1e !important; color: #6fcf8a !important; }
.stInfo    { background: #1a2230 !important; color: #7ab8e8 !important; }
.stWarning { background: #2e2412 !important; color: #e8b96f !important; }
.stError   { background: #2e1a1a !important; color: #e87a7a !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── Divider ── */
hr {
    border-color: #2a2a2a !important;
    margin: 1.25rem 0 !important;
}

/* ── Radio (quiz options) ── */
[data-testid="stRadio"] > div {
    gap: 0.4rem;
}
[data-testid="stRadio"] > div > label {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 0.6rem 1rem !important;
    width: 100%;
    font-size: 0.875rem !important;
    color: #c9c3bc !important;
    transition: all 0.15s;
    cursor: pointer;
}
[data-testid="stRadio"] > div > label:hover {
    border-color: #cc785c !important;
    color: #e8e3dc !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #cc785c !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #1a1a1a; }
::-webkit-scrollbar-thumb { background: #2e2e2e; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #3a3a3a; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #1e1e1e !important;
    border: 1px dashed #2e2e2e !important;
    border-radius: 10px !important;
    padding: 1rem;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #1e1e1e !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 8px !important;
    color: #e8e3dc !important;
}

/* ── Subheader / header text ── */
h1, h2, h3 {
    color: #e8e3dc !important;
    font-family: 'Sora', sans-serif !important;
    letter-spacing: -0.02em;
}
h2 { font-size: 1.1rem !important; font-weight: 600 !important; }
h3 { font-size: 0.95rem !important; font-weight: 500 !important; }

/* ── Caption / small text ── */
.stCaption, small, caption {
    color: #6b6560 !important;
    font-size: 0.75rem !important;
}

/* ── Recent history items ── */
.history-item {
    font-size: 0.78rem;
    color: #6b6560;
    padding: 4px 8px;
    border-radius: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: default;
    transition: background 0.12s;
}
.history-item:hover { background: #242424; color: #9a9490; }

/* ── Badge ── */
.lang-badge {
    display: inline-block;
    background: #cc785c22;
    color: #cc785c;
    border: 1px solid #cc785c44;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Language config
# =========================
LANGUAGE_CONFIG = {
    "C": {
        "icon": "⚙️",
        "color": "#7ab8e8",
        "default_code": """#include <stdio.h>

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", a + b);
    return 0;
}
""",
        "default_tests": "3 4 => 7\n10 20 => 30",
        "chat_placeholder": "Ask me anything about C programming...",
        "ingest_source_prefix": "c_upload",
    },
    "Python": {
        "icon": "🐍",
        "color": "#6fcf8a",
        "default_code": """a, b = map(int, input().split())
print(a + b)
""",
        "default_tests": "3 4 => 7\n10 20 => 30",
        "chat_placeholder": "Ask me anything about Python programming...",
        "ingest_source_prefix": "python_upload",
    },
    "Java": {
        "icon": "☕",
        "color": "#e8b96f",
        "default_code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        System.out.print(a + b);
    }
}
""",
        "default_tests": "3 4 => 7\n10 20 => 30",
        "chat_placeholder": "Ask me anything about Java programming...",
        "ingest_source_prefix": "java_upload",
    },
}

# =========================
# Session state
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {"C": [], "Python": [], "Java": []}
if "language" not in st.session_state:
    st.session_state.language = "C"

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.25rem 0;'>
        <div class='brand-title'>✦ CodeTutor AI</div>
    </div>
    """, unsafe_allow_html=True)

    # Language selector
    st.markdown("<div style='font-size:0.7rem;color:#4a4540;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;'>Language</div>", unsafe_allow_html=True)
    lang_cols = st.columns(3)
    for i, lang in enumerate(["C", "Python", "Java"]):
        with lang_cols[i]:
            icon = LANGUAGE_CONFIG[lang]["icon"]
            is_active = st.session_state.language == lang
            if st.button(
                f"{icon} {lang}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                key=f"lang_btn_{lang}"
            ):
                st.session_state.language = lang
                st.rerun()

    st.markdown("<hr style='margin:1.25rem 0;'>", unsafe_allow_html=True)

    # Navigation
    st.markdown("<div style='font-size:0.7rem;color:#4a4540;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio(
        "nav",
        ["💬  Tutor Chat", "🧪  Code Practice", "📊  Concept Mastery", "🧠  Quiz"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin:1.25rem 0;'>", unsafe_allow_html=True)

    # Recent history
    st.markdown("<div style='font-size:0.7rem;color:#4a4540;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.6rem;'>Recent</div>", unsafe_allow_html=True)
    current_lang = st.session_state.language
    chat_history = st.session_state.chat_history.get(current_lang, [])
    user_messages = [m for role, m in chat_history if role == "user"]
    if user_messages:
        for msg in user_messages[::-1][:5]:
            short = msg[:38] + "…" if len(msg) > 38 else msg
            st.markdown(f"<div class='history-item'>↳ {short}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.78rem;color:#3a3530;padding:4px 0;'>No history yet</div>", unsafe_allow_html=True)

    st.markdown("<div style='position:fixed;bottom:1.5rem;font-size:0.7rem;color:#3a3530;'>CodeTutor AI</div>", unsafe_allow_html=True)

# =========================
# Resolve active config
# =========================
active_lang = st.session_state.language
cfg = LANGUAGE_CONFIG[active_lang]
lang_key = active_lang.lower()

# =========================
# Page header
# =========================
page_meta = {
    "💬  Tutor Chat":      ("Tutor Chat",      f"Ask questions about {active_lang} and get step-by-step explanations."),
    "🧪  Code Practice":   ("Code Practice",   f"Write, run, and grade your {active_lang} code against test cases."),
    "📊  Concept Mastery": ("Concept Mastery", "Track your progress and identify areas to improve."),
    "🧠  Quiz":            ("Quiz",            f"Adaptive quiz generated from your weak concepts in {active_lang}."),
}
title, subtitle = page_meta.get(page, ("CodeTutor AI", ""))
st.markdown(f"""
<div class='page-header'>
    <h1>{cfg['icon']} {title} &nbsp;<span class='lang-badge'>{active_lang}</span></h1>
    <p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# Tutor Chat Page
# =====================================================
if "Tutor Chat" in page:

    with st.expander("📎  Attach study material  ·  PDF or Image", expanded=False):
        uploaded_file = st.file_uploader(
            "Drop a file here",
            type=["pdf", "png", "jpg", "jpeg"],
            key=f"upload_{active_lang}",
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            with st.spinner("Indexing file…"):
                if uploaded_file.type == "application/pdf":
                    extracted_text = load_pdf(uploaded_file)
                else:
                    extracted_text = load_image(uploaded_file)
                ingest_raw_text(
                    extracted_text,
                    source=f"{cfg['ingest_source_prefix']}_{uploaded_file.name}",
                    language=lang_key
                )
            st.success(f"'{uploaded_file.name}' indexed successfully.")

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # Chat history
    history = st.session_state.chat_history[active_lang]
    if not history:
        st.markdown("""
        <div style='text-align:center;padding:3rem 0 2rem 0;color:#3a3530;font-size:0.85rem;'>
            <div style='font-size:2rem;margin-bottom:0.75rem;'>✦</div>
            Start by asking a question below
        </div>
        """, unsafe_allow_html=True)

    for role, message in history:
        with st.chat_message(role):
            st.markdown(message)

    user_input = st.chat_input(cfg["chat_placeholder"])
    if user_input:
        st.session_state.chat_history[active_lang].append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.spinner("Thinking…"):
            answer = ask_tutor(user_input, language=lang_key)
        st.session_state.chat_history[active_lang].append(("assistant", answer))
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.rerun()

# =====================================================
# Code Practice Page
# =====================================================
elif "Code Practice" in page:

    col_code, col_tests = st.columns([3, 2], gap="medium")

    with col_code:
        st.markdown("<div style='font-size:0.75rem;color:#6b6560;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.4rem;'>Editor</div>", unsafe_allow_html=True)
        code = st.text_area(
            "code",
            height=320,
            value=cfg["default_code"],
            key=f"code_{active_lang}",
            label_visibility="collapsed"
        )

    with col_tests:
        st.markdown("<div style='font-size:0.75rem;color:#6b6560;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.4rem;'>Test Cases &nbsp;<span style='font-size:0.68rem;color:#4a4540;font-style:italic;text-transform:none;'>input => expected</span></div>", unsafe_allow_html=True)
        test_input = st.text_area(
            "tests",
            height=200,
            value=cfg["default_tests"],
            key=f"tests_{active_lang}",
            label_visibility="collapsed"
        )
        run_btn = st.button("▶  Run & Grade", type="primary", use_container_width=True)

    if run_btn:
        test_cases = []
        for line in test_input.strip().splitlines():
            if "=>" not in line:
                continue
            inp, exp = line.split("=>", 1)
            test_cases.append({"input": inp.strip(), "expected": exp.strip()})

        if not test_cases:
            st.error("No valid test cases found. Format: `input => expected`")
        else:
            with st.spinner(f"Running {active_lang} code…"):
                result = grade_code(code, test_cases, language=lang_key)

            st.markdown("<hr>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Score",  f"{result['score'] * 100:.0f}%")
            c2.metric("Passed", result["passed"])
            c3.metric("Total",  result["total"])

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            for item in result["details"]:
                if item["status"] == "passed":
                    st.success(f"✓  Test {item['test']} passed")
                else:
                    st.error(f"✗  Test {item['test']} — {item['status']}")
                    if "error" in item:
                        st.code(item["error"], language=lang_key)
                    if "got" in item:
                        ca, cb = st.columns(2)
                        ca.markdown(f"**Expected:** `{item['expected']}`")
                        cb.markdown(f"**Got:** `{item['got']}`")
                    if "weak_concepts" in item:
                        st.warning("Weak concepts: " + ", ".join(item["weak_concepts"]))

# =====================================================
# Concept Mastery Page
# =====================================================
elif "Concept Mastery" in page:

    mastery = compute_mastery()

    if not mastery:
        st.markdown("""
        <div style='text-align:center;padding:3rem 0;color:#3a3530;font-size:0.85rem;'>
            <div style='font-size:2rem;margin-bottom:0.75rem;'>📊</div>
            No learning data yet — start practising to see your progress.
        </div>
        """, unsafe_allow_html=True)
    else:
        concepts   = list(mastery.keys())
        attempts   = [mastery[c]["attempts"] for c in concepts]
        confidence = [mastery[c]["avg_confidence"] for c in concepts]

        # Summary row
        total_concepts = len(concepts)
        strong_count   = sum(1 for c in confidence if c >= 0.8)
        weak_count     = sum(1 for c in confidence if c < 0.5)

        s1, s2, s3 = st.columns(3)
        s1.metric("Concepts Tracked", total_concepts)
        s2.metric("Strong (≥ 80%)",   strong_count)
        s3.metric("Weak (< 50%)",     weak_count)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.75rem;color:#6b6560;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.75rem;'>Confidence per Concept</div>", unsafe_allow_html=True)
        df_chart = pd.DataFrame({"Concept": concepts, "Confidence": confidence}).set_index("Concept")
        st.bar_chart(df_chart, color="#cc785c")

        st.markdown("<hr>", unsafe_allow_html=True)

        col_weak, col_strong = st.columns(2, gap="large")
        with col_weak:
            st.markdown("<div style='font-size:0.75rem;color:#6b6560;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.6rem;'>⚠ Weak Concepts</div>", unsafe_allow_html=True)
            weak_list = [c for c in concepts if mastery[c]["avg_confidence"] < 0.5]
            if weak_list:
                for c in weak_list:
                    st.warning(f"  {c}")
            else:
                st.success("None detected 🎉")

        with col_strong:
            st.markdown("<div style='font-size:0.75rem;color:#6b6560;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.6rem;'>✦ Strong Concepts</div>", unsafe_allow_html=True)
            strong_list = [c for c in concepts if mastery[c]["avg_confidence"] >= 0.8]
            if strong_list:
                for c in strong_list:
                    st.success(f"  {c}")
            else:
                st.info("Keep practising to build strong concepts.")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.75rem;color:#6b6560;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.6rem;'>Full Mastery Table</div>", unsafe_allow_html=True)
        df_table = pd.DataFrame({
            "Concept":        concepts,
            "Attempts":       attempts,
            "Avg Confidence": [round(c, 2) for c in confidence]
        })
        st.dataframe(df_table, width=1200, hide_index=True)

# =====================================================
# Quiz Page
# =====================================================
elif "Quiz" in page:

    if "quiz" not in st.session_state:
        st.session_state.quiz = []
    if "weak_concepts" not in st.session_state:
        st.session_state.weak_concepts = []
    if "quiz_version" not in st.session_state:
        st.session_state.quiz_version = 0
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if not st.session_state.quiz:
        st.markdown("""
        <div style='text-align:center;padding:2.5rem 0 1.5rem 0;color:#3a3530;font-size:0.85rem;'>
            <div style='font-size:2rem;margin-bottom:0.75rem;'>🧠</div>
            Generate a quiz tailored to your weak concepts
        </div>
        """, unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("✦  Generate Quiz", type="primary", use_container_width=True):
            with st.spinner("Generating quiz…"):
                quiz, weak = generate_adaptive_quiz(active_lang)
            st.session_state.quiz = quiz
            st.session_state.weak_concepts = weak
            st.session_state.quiz_version += 1
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.rerun()

    if st.session_state.weak_concepts:
        weak_str = "  ·  ".join(st.session_state.weak_concepts)
        st.markdown(f"<div style='font-size:0.78rem;color:#6b6560;margin:0.5rem 0 1.25rem 0;'>Focusing on: <span style='color:#cc785c;'>{weak_str}</span></div>", unsafe_allow_html=True)

    if st.session_state.quiz:
        score = 0
        st.markdown("<hr>", unsafe_allow_html=True)

        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"<div style='font-size:0.7rem;color:#4a4540;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.3rem;'>Question {i+1} of {len(st.session_state.quiz)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.95rem;font-weight:500;color:#e8e3dc;margin-bottom:0.75rem;'>{q['question']}</div>", unsafe_allow_html=True)

            user_ans = st.radio(
                "ans",
                q["options"],
                index=None,
                key=f"{active_lang}_quiz_{st.session_state.quiz_version}_{i}",
                label_visibility="collapsed"
            )
            if user_ans == q["answer"]:
                score += 1

            st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        if not st.session_state.quiz_submitted:
            col_sub, _ = st.columns([1, 3])
            with col_sub:
                if st.button("Submit Quiz", type="primary", use_container_width=True):
                    st.session_state.quiz_submitted = True
                    st.session_state.quiz_score = score
                    st.rerun()

        if st.session_state.quiz_submitted:
            total = len(st.session_state.quiz)
            saved = st.session_state.quiz_score
            pct   = saved / total

            r1, r2, r3 = st.columns(3)
            r1.metric("Score",    f"{saved}/{total}")
            r2.metric("Correct",  f"{pct*100:.0f}%")
            r3.metric("Status",   "Improving 🎉" if pct >= 0.5 else "Keep going 💪")

            if pct < 0.5:
                st.warning("Still some weak areas — try generating a new quiz to keep practising.")
            else:
                st.success("Good work! Generate another quiz to keep the streak going.")
