import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import proofread_prompt

setup_page("添削", "✏️")

text = st.text_area("添削したい文章*", height=300, placeholder="添削したい文章を貼り付けてください")
focus = st.selectbox(
    "重点的にチェックする観点",
    ["誤字脱字・文法全般", "より自然でこなれた表現にする", "敬語・ビジネスマナー", "簡潔さ（冗長な表現の削減）"],
)

if st.button("添削する", type="primary", disabled=not text):
    system_instruction, prompt = proofread_prompt(text, focus)
    generate_and_display("proofread_output", prompt, "添削結果", system_instruction=system_instruction)

show_result("proofread_output", "添削結果", "proofread.txt")
