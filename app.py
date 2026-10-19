import streamlit as st

from utils.common import render_sidebar
from utils.gemini_client import get_api_key

st.set_page_config(page_title="AIライティングツール", page_icon="🖋️", layout="wide")
render_sidebar()

st.title("🖋️ AIライティングツール")
st.caption("Gemini APIを使った個人用オールインワン・ライティング支援ツール")

if not get_api_key():
    st.info("👈 サイドバーからGemini APIキーを設定すると、各機能が使えるようになります。")

st.subheader("機能一覧")

features = [
    ("pages/1_📝_ブログ執筆.py", "📝", "ブログ執筆", "テーマやキーワードから記事ドラフトを生成します"),
    ("pages/2_📧_メール返信.py", "📧", "メール返信", "受信メールと返信の要点から返信文を作成します"),
    ("pages/3_📄_要約.py", "📄", "要約", "長文を指定した形式・長さで要約します"),
    ("pages/4_✏️_添削.py", "✏️", "添削", "誤字脱字や表現を校正し、修正点を解説します"),
    ("pages/5_🌐_翻訳.py", "🌐", "翻訳", "文章を指定した言語に翻訳します"),
    ("pages/6_🎨_トーン変換.py", "🎨", "トーン・文体変換", "文体を丁寧語・カジュアルなどに変換します"),
    ("pages/7_💡_タイトル生成.py", "💡", "タイトル・見出し生成", "本文からタイトル案を複数提案します"),
    ("pages/8_🧩_箇条書き展開.py", "🧩", "箇条書き展開", "メモ・箇条書きを自然な文章に展開します"),
]

cols = st.columns(2)
for i, (page_path, icon, name, desc) in enumerate(features):
    with cols[i % 2]:
        with st.container(border=True):
            st.page_link(page_path, label=f"**{icon} {name}**")
            st.caption(desc)
