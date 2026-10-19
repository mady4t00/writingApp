import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import translate_prompt

setup_page("翻訳", "🌐")

text = st.text_area("翻訳したい文章*", height=250, placeholder="翻訳したい文章を貼り付けてください")

language_options = ["英語", "中国語（簡体字）", "中国語（繁体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語", "その他（自由入力）"]
selected_language = st.selectbox("翻訳先の言語", language_options)
if selected_language == "その他（自由入力）":
    target_language = st.text_input("言語名を入力", placeholder="例: タイ語")
else:
    target_language = selected_language

if st.button("翻訳する", type="primary", disabled=not (text and target_language)):
    system_instruction, prompt = translate_prompt(text, target_language)
    generate_and_display(
        "translate_output", prompt, f"翻訳結果（{target_language}）", system_instruction=system_instruction
    )

show_result("translate_output", "翻訳結果", "translation.txt")
