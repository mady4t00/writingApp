import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import summarize_prompt

setup_page("要約", "📄")

text = st.text_area("要約したい文章*", height=300, placeholder="長文をここに貼り付けてください")
style = st.selectbox(
    "要約の形式",
    ["一言で（1文）", "短め（3行程度）", "箇条書き（要点3〜5個）", "詳しめ（元の1/3程度の分量）"],
)

if st.button("要約する", type="primary", disabled=not text):
    system_instruction, prompt = summarize_prompt(text, style)
    generate_and_display("summary_output", prompt, "要約結果", system_instruction=system_instruction)

show_result("summary_output", "要約結果", "summary.txt")
