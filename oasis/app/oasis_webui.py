import streamlit as st
import sys
import os
from datetime import datetime
from oasis.config import Config
from oasis.services.oasis_runner import run_oasis

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oasis.oasis import OASIS
from oasis.config import Config

def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def custom_card(title, content):
    return st.markdown(f"""
    <div class="card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def run_streamlit_app():
    st.set_page_config(page_title="OASIS App", page_icon="🌵", layout="wide")
    
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    local_css(css_path)

    # Custom HTML structure
    st.markdown("""
    <div class="dashboard">
        <div class="header">
            <img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/OASIS.png" alt="OASIS Logo" width="600">
            <h1>🌵 OASIS Dashboard</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- サイドバーでパラメータ入力 ---
    st.sidebar.header("⚙️ 詳細パラメータ設定")
    from oasis.config import Config

    llm_model = st.sidebar.text_input("LLMモデル名", value=Config.LLM_MODEL or "")
    max_retries = st.sidebar.number_input("LLMリトライ回数", min_value=1, max_value=100, value=10)
    wp_url = st.sidebar.text_input("WordPress URL", value=Config.BASE_URL or "")
    wp_user = st.sidebar.text_input("WordPressユーザー名", value=Config.AUTH_USER or "", type="password")
    wp_pass = st.sidebar.text_input("WordPressパスワード", value=Config.AUTH_PASS or "", type="password")
    qiita_token = st.sidebar.text_input("Qiita APIトークン", value=Config.QIITA_TOKEN or "", type="password")
    qiita_post_publish = st.sidebar.checkbox("Qiita公開設定", value=False)
    note_email = st.sidebar.text_input("Noteメールアドレス", value=Config.NOTE_EMAIL or "", type="password")
    note_password = st.sidebar.text_input("Noteパスワード", value=Config.NOTE_PASSWORD or "", type="password")
    note_user_id = st.sidebar.text_input("NoteユーザーID", value=Config.NOTE_USER_ID or "")
    note_publish = st.sidebar.checkbox("Note公開", value=False)
    note_api_ver = st.sidebar.text_input("Note API Ver", value="v2")
    zenn_output_path = st.sidebar.text_input("Zenn出力パス", value=r"C:\Prj\Zenn\articles")
    zenn_publish = st.sidebar.checkbox("Zenn公開", value=False)
    firefox_binary_path = st.sidebar.text_input("Firefoxバイナリパス", value="")
    firefox_profile_path = st.sidebar.text_input("Firefoxプロファイルパス", value="")
    firefox_headless = st.sidebar.checkbox("Firefoxヘッドレス", value=False)

    # File upload section
    st.markdown("### 📝 記事のアップロード")
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_markdown = st.file_uploader("マークダウンファイル (.md)", type=['md'], key="markdown")
    with col2:
        uploaded_image = st.file_uploader("サムネイル画像 (任意)", type=['png', 'jpg', 'jpeg'], key="image")

    # Post options
    st.markdown("### 🎯 投稿設定")
    post_options = st.multiselect(
        "投稿先を選択",
        ["WordPress", "Qiita", "Note", "Zenn"],
        default=["WordPress", "Qiita", "Note", "Zenn"]
    )

    # Preview cards
    col1, col2 = st.columns(2)
    with col1:
        custom_card("📄 マークダウンファイル",
                   uploaded_markdown.name if uploaded_markdown else "未選択")
    with col2:
        custom_card("🖼️ サムネイル画像",
                   uploaded_image.name if uploaded_image else "未選択")

    # Process button and logic
    start_process = st.button("🚀 処理開始", key="start_process", use_container_width=True)

    if start_process:
        if not uploaded_markdown:
            st.error("⚠️ マークダウンファイルをアップロードしてください。")
            return

        try:
            # Create draft directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            draft_dir = os.path.join(Config.WEBUI_DRAFT_DIR, timestamp)
            os.makedirs(draft_dir, exist_ok=True)

            # Save uploaded files directly under the timestamp directory
            md_path = os.path.join(draft_dir, os.path.basename(uploaded_markdown.name))
            with open(md_path, "wb") as f:
                f.write(uploaded_markdown.getbuffer())

            img_path = None
            if uploaded_image:
                img_path = os.path.join(draft_dir, os.path.basename(uploaded_image.name))
                with open(img_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())

            # --- パラメータをdictでまとめてrun_oasisに渡す ---
            params = {
                "markdown": md_path,
                "image": img_path,
                "folder": None,
                "llm_model": llm_model or None,
                "max_retries": max_retries,
                "wp_url": wp_url or None,
                "wp_user": wp_user or None,
                "wp_pass": wp_pass or None,
                "qiita_token": qiita_token or None,
                "qiita_post_publish": qiita_post_publish,
                "note_email": note_email or None,
                "note_password": note_password or None,
                "note_user_id": note_user_id or None,
                "note_publish": note_publish,
                "note_api_ver": note_api_ver or "v2",
                "zenn_output_path": zenn_output_path or r"C:\Prj\Zenn\articles",
                "zenn_publish": zenn_publish,
                "firefox_binary_path": firefox_binary_path or None,
                "firefox_profile_path": firefox_profile_path or None,
                "firefox_headless": firefox_headless,
                "wp": "WordPress" in post_options,
                "qiita": "Qiita" in post_options,
                "note": "Note" in post_options,
                "zenn": "Zenn" in post_options,
            }

            with st.spinner("処理中..."):
                result = run_oasis(params)

            st.success("✅ 処理が完了しました！")
            
            with st.expander("結果の詳細"):
                st.write(f"📘 タイトル: {result['title']}")
                st.write(f"🔗 スラグ: {result['slug']}")
                st.write("📁 作成されたフォルダ:", os.path.dirname(md_path))
                
                st.subheader("📁 カテゴリ")
                for category in result['categories']:
                    st.markdown(f"- **{category['name']}** (ID: `{category['slug']}`)")
                
                st.subheader("🏷️ タグ")
                for tag in result['tags']:
                    st.markdown(f"- **{tag['name']}** (ID: `{tag['slug']}`)")

        except Exception as e:
            st.error(f"⚠️ エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    run_streamlit_app()
