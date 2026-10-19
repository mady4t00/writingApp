"""Gemini APIとの通信をまとめたモジュール。"""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DEFAULT_MODEL = "gemini-3.6-flash"


def get_api_key() -> str | None:
    """`.env`のGEMINI_API_KEYを優先し、なければセッション上の入力値を使う。"""
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key
    return st.session_state.get("gemini_api_key")


@st.cache_resource(show_spinner=False)
def _build_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def get_client() -> genai.Client:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("Gemini APIキーが設定されていません。")
    return _build_client(api_key)


def generate_stream(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.7,
    model: str = DEFAULT_MODEL,
):
    """Geminiにプロンプトを送信し、テキストチャンクを順次yieldするジェネレータ。

    st.write_stream にそのまま渡せる形式。
    """
    client = get_client()
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    response = client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=config,
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text
