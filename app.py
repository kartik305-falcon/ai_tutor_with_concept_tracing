import streamlit as st
import pandas as pd

from rag_llm import ask_tutor
from auto_grader import grade_code
from concept_analytics import compute_mastery
from file_loader import load_pdf, load_image
from ingest import ingest_raw_text


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="AI C Tutor",
    layout="wide"
)

st.title("🧠 AI Tutor for C Programming")


# =========================
# Sidebar navigation
# =========================
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Tutor Chat", "Code Practice", "Concept Mastery"]
)


# =========================
# Session state
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =====================================================
# Tutor Chat Page
# =====================================================
if page == "Tutor Chat":
    st.header("📘 Tutor Chat")

    # -------- File Upload --------
    st.subheader("📤 Upload Study Material (PDF / Image)")

    uploaded_file = st.file_uploader(
        "Upload PDF or Image (used as tutor context)",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        with st.spinner("Processing file..."):
            if uploaded_file.type == "application/pdf":
                extracted_text = load_pdf(uploaded_file)
            else:
                extracted_text = load_image(uploaded_file)

            ingest_raw_text(
                extracted_text,
                source=uploaded_file.name
            )

        st.success(f"✅ '{uploaded_file.name}' indexed successfully!")

    st.divider()

    # -------- Chat History --------
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    # -------- Chat Input --------
    user_input = st.chat_input("Ask a question from uploaded file or C concepts...")

    if user_input:
        # User message
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Tutor response
        with st.spinner("Tutor is thinking..."):
            answer = ask_tutor(user_input)

        st.session_state.chat_history.append(("assistant", answer))
        with st.chat_message("assistant"):
            st.markdown(answer)


# =====================================================
# Code Practice Page
# =====================================================
elif page == "Code Practice":
    st.header("🧪 Code Practice — C Language")

    code = st.text_area(
        "C Code",
        height=300,
        value="""#include <stdio.h>

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", a + b);
    return 0;
}
"""
    )

    st.markdown("### Test Cases (one per line: input => expected output)")
    test_input = st.text_area(
        "Test Cases",
        height=150,
        value="3 4 => 7\n10 20 => 30"
    )

    if st.button("▶ Run & Grade"):
        test_cases = []

        for line in test_input.strip().splitlines():
            if "=>" not in line:
                continue
            inp, exp = line.split("=>", 1)
            test_cases.append({
                "input": inp.strip(),
                "expected": exp.strip()
            })

        if not test_cases:
            st.error("No valid test cases found.")
        else:
            with st.spinner("Running and grading code..."):
                result = grade_code(code, test_cases)

            st.subheader("📊 Results")
            st.write(f"**Score:** {result['score']}")

            for item in result["details"]:
                if item["status"] == "passed":
                    st.success(f"Test {item['test']} passed")
                else:
                    st.error(f"Test {item['test']} failed")
                    if "error" in item:
                        st.code(item["error"])
                    if "weak_concepts" in item:
                        st.write(
                            "⚠ Weak concepts:",
                            ", ".join(item["weak_concepts"])
                        )


# =====================================================
# Concept Mastery Dashboard
# =====================================================
elif page == "Concept Mastery":
    st.header("📊 Concept Mastery Dashboard")

    mastery = compute_mastery()

    if not mastery:
        st.info("No learning data available yet.")
    else:
        concepts = []
        attempts = []
        confidence = []

        for concept, data in mastery.items():
            concepts.append(concept)
            attempts.append(data["attempts"])
            confidence.append(data["avg_confidence"])

        # ---- Table ----
        st.subheader("📋 Mastery Table")
        df_table = pd.DataFrame({
            "Concept": concepts,
            "Attempts": attempts,
            "Avg Confidence": confidence
        })
        st.dataframe(df_table)

        # ---- Bar Chart ----
        st.subheader("📈 Confidence per Concept")
        df_chart = pd.DataFrame({
            "Concept": concepts,
            "Confidence": confidence
        }).set_index("Concept")

        st.bar_chart(df_chart)

        # ---- Weak concepts ----
        st.subheader("⚠ Weak Concepts")
        weak = [
            c for c, d in mastery.items()
            if d["avg_confidence"] < 0.5
        ]

        if weak:
            for c in weak:
                st.warning(c)
        else:
            st.success("No weak concepts detected 🎉")

        # ---- Strong concepts ----
        st.subheader("✅ Strong Concepts")
        strong = [
            c for c, d in mastery.items()
            if d["avg_confidence"] >= 0.8
        ]

        if strong:
            for c in strong:
                st.success(c)
        else:
            st.info("No strong concepts yet")
