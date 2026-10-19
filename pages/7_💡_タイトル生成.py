import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import title_generate_prompt

setup_page("タイトル・見出し生成", "💡")

content = st.text_area("記事本文*", height=300, placeholder="タイトルを考えたい記事の本文を貼り付けてください")

col1, col2 = st.columns(2)
with col1:
    num_suggestions = st.slider("提案数", 3, 10, 5)
with col2:
    style = st.selectbox("方向性", ["SEOを意識した検索されやすいタイトル", "クリックしたくなるキャッチーなタイトル", "シンプルで簡潔なタイトル"])

if st.button("タイトルを生成", type="primary", disabled=not content):
    system_instruction, prompt = title_generate_prompt(content, num_suggestions, style)
    generate_and_display("title_output", prompt, "タイトル案", system_instruction=system_instruction)

show_result("title_output", "タイトル案", "titles.txt")
