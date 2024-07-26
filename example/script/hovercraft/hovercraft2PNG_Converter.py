import os
import time
import threading
import http.server
import socketserver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from tqdm import tqdm

# HTTPサーバーの設定
PORT = 8000
DIRECTORY = "output"  # Hovercraftの出力ディレクトリ

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"サーバーが http://localhost:{PORT} で起動しました")
        httpd.serve_forever()

def capture_slides_as_png(output_dir):
    # Firefoxドライバーの設定（headlessモード）
    options = Options()
    # options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    # サーバーで提供されているHTMLファイルを開く
    driver.get(f'http://localhost:{PORT}/index.html')

    # スライドの数を取得
    slides = driver.find_elements(By.CLASS_NAME, 'step')
    
    for i in tqdm(range(len(slides))):
        # 現在のスライドが表示されるまで待機
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f".step:nth-child({i+1})"))
        )
        
        time.sleep(5)
        # スクリーンショットを撮影
        driver.save_screenshot(f'{output_dir}/slide_{i+1}.png')
        
        # 次のスライドへ移動（最後のスライドでは実行しない）
        if i < len(slides) - 1:
            # 右キーを押して次のスライドに移動
            webdriver.ActionChains(driver).send_keys(Keys.RIGHT).perform()
        
        time.sleep(1)  # アニメーションが完了するのを待つ

    driver.quit()

if __name__ == "__main__":
    # サーバーを別スレッドで起動
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # サーバーの起動を待つ
    time.sleep(2)

    # スライドのキャプチャを実行
    capture_slides_as_png('slide_images')

    print("全てのスライドのキャプチャが完了しました。")
