from oasis.oasis import OASIS
from oasis.config import Config
from oasis.logger import logger

def run_oasis(params):
    """
    OASISの投稿処理をCLI/GUI共通で実行する関数だよ！✨
    params: dict型で全パラメータを受け取る
    """
    oasis = OASIS(
        base_url=params.get("wp_url") or Config.BASE_URL,
        auth_user=params.get("wp_user") or Config.AUTH_USER,
        auth_pass=params.get("wp_pass") or Config.AUTH_PASS,
        llm_model=params.get("llm_model"),
        max_retries=params.get("max_retries", 10),
        qiita_token=params.get("qiita_token") or Config.QIITA_TOKEN,
        qiita_post_private=not params.get("qiita_post_publish", False),
        note_email=params.get("note_email") or Config.NOTE_EMAIL,
        note_password=params.get("note_password") or Config.NOTE_PASSWORD,
        note_user_id=params.get("note_user_id") or Config.NOTE_USER_ID,
        note_publish=params.get("note_publish", False),
        note_api_ver=params.get("note_api_ver", "v2"),
        firefox_binary_path=params.get("firefox_binary_path"),
        firefox_profile_path=params.get("firefox_profile_path"),
        firefox_headless=params.get("firefox_headless", False),
        zenn_output_path=params.get("zenn_output_path", r"C:\Prj\Zenn\articles"),
        zenn_publish=params.get("zenn_publish", False)
    )

    logger.info(
        f"使用中のLLMモデル: {oasis.config.LLM_MODEL}, 最大リトライ回数: {params.get('max_retries', 10)}"
    )

    if params.get("folder"):
        result = oasis.process_folder(
            params["folder"],
            post_to_qiita=params.get("qiita", False),
            post_to_note=params.get("note", False),
            post_to_wp=params.get("wp", False),
            post_to_zenn=params.get("zenn", False)
        )
    else:
        result = oasis.process_files(
            params.get("markdown"),
            params.get("image"),
            post_to_qiita=params.get("qiita", False),
            post_to_note=params.get("note", False),
            post_to_wp=params.get("wp", False),
            post_to_zenn=params.get("zenn", False)
        )

    logger.info("投稿が正常に作成されました！")
    logger.info(f"タイトル: {result['title']}")
    logger.info("-" * 80)
    logger.info(f"スラグ: {result['slug']}")
    logger.info(f">>> categories :")
    for category in result['categories']:
        logger.info(f"- {category['name']} (ID: {category['slug']})")
    logger.info(">>> tags :")
    for tag in result['tags']:
        logger.info(f"- {tag['name']} (ID: {tag['slug']})")
    return result