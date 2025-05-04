import streamlit as st
import sys
import os
from datetime import datetime
from oasis.config import Config

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

def run_streamlit_app(oasis: OASIS):
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

            # Process files
            with st.spinner("処理中..."):
                result = oasis.process_files(
                    md_path,
                    img_path,
                    post_to_wp="WordPress" in post_options,
                    post_to_qiita="Qiita" in post_options,
                    post_to_note="Note" in post_options,
                    post_to_zenn="Zenn" in post_options
                )

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
    oasis = OASIS(
        base_url=Config.BASE_URL,
        auth_user=Config.AUTH_USER,
        auth_pass=Config.AUTH_PASS,
        qiita_token=Config.QIITA_TOKEN,
        zenn_output_path=r"C:\Prj\Zenn\articles"
    )
    run_streamlit_app(oasis)
