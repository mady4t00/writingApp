"""各ページで共通利用するページ設定・サイドバー・生成結果表示ロジック。"""
import streamlit as st

from utils.gemini_client import DEFAULT_MODEL, generate_stream, get_api_key

MODEL_OPTIONS = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite", "その他（自由入力）"]


def setup_page(title: str, icon: str) -> None:
    st.set_page_config(page_title=f"{title} | AIライティングツール", page_icon=icon, layout="wide")
    render_sidebar()
    st.title(f"{icon} {title}")


def render_sidebar() -> None:
    with st.sidebar:
        st.header("⚙️ 設定")

        api_key = get_api_key()
        if api_key:
            st.success("APIキー: 設定済み")
        else:
            st.warning("APIキーが未設定です")
            input_key = st.text_input(
                "Gemini APIキーを入力（このセッションのみ保持）",
                type="password",
                key="gemini_api_key_input",
            )
            if input_key:
                st.session_state["gemini_api_key"] = input_key
                st.rerun()

        st.divider()

        selected = st.selectbox("モデル", MODEL_OPTIONS, key="model_select")
        if selected == "その他（自由入力）":
            st.session_state["active_model"] = st.text_input(
                "モデルIDを入力", value=DEFAULT_MODEL, key="custom_model"
            )
        else:
            st.session_state["active_model"] = selected

        st.session_state["temperature"] = st.slider(
            "創造性（temperature）", 0.0, 1.0, 0.7, 0.1,
            help="値を上げるほど表現が多様・自由になり、下げるほど堅実になります。",
        )


def get_active_model() -> str:
    return st.session_state.get("active_model", DEFAULT_MODEL)


def get_temperature() -> float:
    return st.session_state.get("temperature", 0.7)


def generate_and_display(
    session_key: str,
    prompt: str,
    result_label: str = "生成結果",
    system_instruction: str | None = None,
) -> None:
    """Geminiで生成し、ストリーミング表示した結果をセッションに保存する。

    system_instruction を渡すと、固定の役割・出力要件をユーザー入力（prompt）とは
    別チャンネルでモデルに伝える。ユーザーが貼り付けたテキストに指示文が
    紛れ込んでいても上書きされにくくするため。
    """
    if not get_api_key():
        st.error("Gemini APIキーが設定されていません。サイドバーから設定してください。")
        return

    try:
        with st.spinner("生成中..."):
            st.markdown(f"**{result_label}（生成中）**")
            output = st.write_stream(
                generate_stream(
                    prompt,
                    system_instruction=system_instruction,
                    temperature=get_temperature(),
                    model=get_active_model(),
                )
            )
        st.session_state[session_key] = output
    except Exception as e:
        st.error(f"生成に失敗しました: {e}")


def show_result(session_key: str, result_label: str = "生成結果", file_name: str = "result.txt") -> None:
    output = st.session_state.get(session_key)
    if not output:
        return
    st.subheader(f"📋 {result_label}（保存済み・編集可）")
    st.text_area(
        result_label,
        value=output,
        height=350,
        label_visibility="collapsed",
        key=f"{session_key}_display",
    )
    st.download_button(
        "📥 テキストファイルとして保存",
        output,
        file_name=file_name,
        key=f"{session_key}_download",
    )
