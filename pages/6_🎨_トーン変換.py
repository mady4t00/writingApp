import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import tone_convert_prompt

setup_page("トーン・文体変換", "🎨")

text = st.text_area("変換したい文章*", height=250, placeholder="文体を変換したい文章を貼り付けてください")

tone_options = ["丁寧語（です・ます調）", "ビジネス敬語", "カジュアル・くだけた口調", "フレンドリー", "学術的・論文調", "その他（自由入力）"]
selected_tone = st.selectbox("変換先のトーン", tone_options)
if selected_tone == "その他（自由入力）":
    target_tone = st.text_input("トーンを入力", placeholder="例: 子供にもわかる優しい言葉")
else:
    target_tone = selected_tone

if st.button("変換する", type="primary", disabled=not (text and target_tone)):
    system_instruction, prompt = tone_convert_prompt(text, target_tone)
    generate_and_display("tone_output", prompt, "変換結果", system_instruction=system_instruction)

show_result("tone_output", "変換結果", "tone_converted.txt")
