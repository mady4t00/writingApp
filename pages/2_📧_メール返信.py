import streamlit as st

from utils.common import generate_and_display, setup_page, show_result
from utils.prompts import email_reply_prompt

setup_page("メール返信", "📧")

original_email = st.text_area("受信したメール本文*", height=200, placeholder="返信したいメールの本文を貼り付けてください")
key_points = st.text_area("返信に盛り込みたい要点（任意）", height=100, placeholder="例: 来週の会議は出席できる、資料は明日送る")

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("返信のトーン", ["丁寧・フォーマル", "ややカジュアル", "謝罪", "お断り・辞退"])
with col2:
    sender_name = st.text_input("差出人名（任意）")

if st.button("返信文を生成", type="primary", disabled=not original_email):
    system_instruction, prompt = email_reply_prompt(original_email, key_points, tone, sender_name)
    generate_and_display("email_output", prompt, "生成された返信文", system_instruction=system_instruction)

show_result("email_output", "生成された返信文", "email_reply.txt")
