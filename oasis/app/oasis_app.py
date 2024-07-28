import streamlit as st
import sys
import os

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

    # Input fields and options
    col1, col2 = st.columns(2)
    with col1:
        folder_path = st.text_input("処理するフォルダのパス", key="folder_path")
    with col2:
        post_options = st.multiselect(
            "投稿先を選択",
            ["WordPress", "Qiita", "Note", "Zenn"],
            default=["WordPress", "Qiita", "Note", "Zenn"]
        )

    # Custom cards
    col1, col2 = st.columns(2)
    with col1:
        custom_card("📁 選択されたフォルダ", folder_path if folder_path else "未選択")
    with col2:
        custom_card("🎯 選択された投稿先", ", ".join(post_options))

    # Streamlit button with custom CSS class
    start_process = st.button("🚀 処理開始", key="start_process", use_container_width=True)

    # Process logic
    if start_process:
        if folder_path:
            with st.spinner("処理中..."):
                result = oasis.process_folder(
                    folder_path,
                    post_to_wp="WordPress" in post_options,
                    post_to_qiita="Qiita" in post_options,
                    post_to_note="Note" in post_options,
                    post_to_zenn="Zenn" in post_options
                )
            
            st.success("✅ 処理が完了しました！")
            
            with st.expander("結果の詳細"):
                st.write(f"📘 タイトル: {result['title']}")
                st.write(f"🔗 スラグ: {result['slug']}")
                
                st.subheader("📁 カテゴリ")
                for category in result['categories']:
                    st.markdown(f"- **{category['name']}** (ID: `{category['slug']}`)")
                
                st.subheader("🏷️ タグ")
                for tag in result['tags']:
                    st.markdown(f"- **{tag['name']}** (ID: `{tag['slug']}`)")
        else:
            st.error("⚠️ フォルダパスを入力してください。")

if __name__ == "__main__":
    oasis = OASIS(
        base_url=Config.BASE_URL,
        auth_user=Config.AUTH_USER,
        auth_pass=Config.AUTH_PASS,
        qiita_token=Config.QIITA_TOKEN,
        zenn_output_path=r"C:\Prj\Zenn\articles"
    )
    run_streamlit_app(oasis)
