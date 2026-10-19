import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import bullet_expand_prompt

setup_page("箇条書き展開", "🧩")

bullets = st.text_area("箇条書き・メモ*", height=250, placeholder="例:\n- 新商品Aを来月発売\n- 価格は2980円\n- 学生向けの機能を強化")

col1, col2 = st.columns(2)
with col1:
    output_format = st.selectbox("出力形式", ["ブログ記事風の文章", "ビジネス報告書風の文章", "お知らせ・案内文", "自由な文章"])
with col2:
    length = st.selectbox("分量目安", ["短め", "標準", "長め"])

if st.button("文章に展開する", type="primary", disabled=not bullets):
    system_instruction, prompt = bullet_expand_prompt(bullets, output_format, length)
    generate_and_display("expand_output", prompt, "展開結果", system_instruction=system_instruction)

show_result("expand_output", "展開結果", "expanded.txt")
