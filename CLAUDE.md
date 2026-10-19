# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際にClaude Code（claude.ai/code）へ向けたガイダンスを提供する。

## これは何か

個人用・単一ユーザー向けのAIライティングツール。Streamlitのマルチページアプリで構成されており、各ページがGemini APIをラップして1つのライティングタスク（ブログ執筆、メール返信、要約、添削、翻訳、トーン変換、タイトル生成、箇条書き展開）を担当する。認証もデータベースもなく、すべてローカル・単一セッションの状態のみで完結する。

## コマンド

```bash
# セットアップ（Windows用のvenvは.venvに作成済み）
.venv\Scripts\activate
pip install -r requirements.txt

# 起動
streamlit run app.py
```

テストスイート・リンター・ビルドステップは用意されていない。ブラウザなしで変更を簡易チェックする場合はバイトコンパイルを行う。

```bash
python -m py_compile app.py utils/*.py pages/*.py
```

APIキーは`.env`ファイルの`GEMINI_API_KEY`から取得する（`.env.example`をコピーして作成）。未設定の場合は、サイドバーからその場で入力した値が`st.session_state`にそのセッション限りで保持される。

## アーキテクチャ

**ページの型**: `pages/`内の各ファイルはすべて同じ3ステップ構成に従っており、変更・追加時もこの構成を崩さないこと。
1. `setup_page(title, icon)` — ページ設定と共通サイドバーの描画
2. `st.text_area`/`st.selectbox`で入力を集め、`utils/prompts.py`内の関数で`(system_instruction, prompt)`のタプルを組み立て、ボタン押下時に`generate_and_display(session_key, prompt, result_label, system_instruction=system_instruction)`を呼び出す
3. 末尾で無条件に`show_result(session_key, result_label, file_name)`を呼び、直近の生成結果を（編集可能な`st.text_area`＋ダウンロードボタンとして）再実行後も表示し続ける

新しいライティング機能を追加する場合は、(1) `utils/prompts.py`にプロンプト生成関数を追加、(2) `pages/`に番号付きファイルを追加（`N_<絵文字>_<名前>.py`というファイル名がサイドバー上の並び順・表示名を決める）、(3) `app.py`内の機能一覧に登録する、という3点が必要。

`utils/prompts.py`の各関数は`(system_instruction, user_content)`のタプルを返す。役割・出力要件などの固定指示は`system_instruction`側に、ユーザーが入力・貼り付けたデータは`user_content`側に置き、`user_content`側には`INJECTION_GUARD`（データ内の指示文を無視させる注意書き）を混在させないこと。これは、貼り付けテキスト（他人のメール本文や外部記事など）に紛れた指示文でモデルの挙動が乗っ取られる、いわゆるプロンプトインジェクションへの対策であり、新しいプロンプト関数を追加する際も同じ分離を踏襲すること。

**`utils/gemini_client.py`**: Gemini APIへのアクセスをすべて集約している。
- `get_api_key()`は`.env`を優先し、なければ`st.session_state["gemini_api_key"]`を参照する
- `get_client()`は`genai.Client`を構築し、`st.cache_resource`でAPIキー文字列自体をキーにキャッシュする（そのため、セッション中にキーを切り替えても正しくキャッシュが再構築される）
- `generate_stream(...)`が唯一の生成用エントリポイントで、`st.write_stream`にそのまま渡せるテキストチャンクのジェネレータを返す。非ストリーミング版は存在しない。`generate_and_display`とストリーミングUIがこの前提に依存しているため、理由なく追加しないこと。

**`utils/common.py`**: 全ページ共通のUI処理をまとめている。各ページ側でこのロジックを重複実装しないこと。
- `render_sidebar()`はAPIキー未設定時の入力フォールバック、モデル選択（`gemini-3.6-flash`/`gemini-3.5-flash`/`gemini-3.5-flash-lite`/自由入力）、temperatureスライダーを扱い、選択値を`st.session_state["active_model"]`/`["temperature"]`に保存する
- `generate_and_display(session_key, prompt, result_label, system_instruction=None)`は「APIキー確認 → ストリーミング生成 → `st.session_state[session_key]`へ保存」までを行う標準ヘルパー。`system_instruction`は`generate_stream`にそのまま渡され、`prompt`（ユーザー入力データ）とは別チャンネルでモデルに伝わる
- `show_result(session_key, result_label, file_name)`は、直前に生成が実行されたかどうかに関わらず`st.session_state[session_key]`の内容を描画する。これにより、他のウィジェット操作で再実行が起きても結果が消えずに残る

各ページは固有の`session_key`（例: `"blog_output"`、`"email_output"`）を使用している。ページごとの結果が混ざらないよう、この値は必ずページごとに一意にすること。
