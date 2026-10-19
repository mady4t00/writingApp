import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import blog_prompt

setup_page("ブログ執筆", "📝")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("テーマ・トピック*", placeholder="例: 在宅ワークの生産性を上げる方法")
    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）")
with col2:
    audience = st.text_input("想定読者（任意）", placeholder="例: 20代の新社会人")
    length = st.selectbox("文字数目安", ["短め（600字程度）", "標準（1200字程度）", "長め（2000字程度）"])

tone = st.selectbox("トーン", ["丁寧・解説調", "フレンドリー", "専門的", "エモーショナル"])

if st.button("記事を生成", type="primary", disabled=not topic):
    system_instruction, prompt = blog_prompt(topic, keywords, audience, length, tone)
    generate_and_display("blog_output", prompt, "生成された記事", system_instruction=system_instruction)

show_result("blog_output", "生成された記事", "blog_article.txt")
