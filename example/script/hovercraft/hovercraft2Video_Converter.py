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
import cv2
import numpy as np

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

def capture_slides_as_png(output_dir, fps=30, duration=5):
    options = Options()
    # options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    driver.get(f'http://localhost:{PORT}/index.html')

    slides = driver.find_elements(By.CLASS_NAME, 'step')
    
    frame_count = 0
    for i in tqdm(range(len(slides)), desc="スライドのキャプチャ"):
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f".step:nth-child({i+1})"))
        )
        
        # 各スライドをfps * duration回キャプチャ
        for j in range(fps * duration):
            driver.save_screenshot(f'{output_dir}/slide_{frame_count:05d}.png')
            frame_count += 1
            time.sleep(1/fps)
        
        if i < len(slides) - 1:
            # トランジション中のフレームもキャプチャ
            webdriver.ActionChains(driver).send_keys(Keys.RIGHT).perform()
            for j in range(fps):  # 1秒間のトランジションを仮定
                driver.save_screenshot(f'{output_dir}/slide_{frame_count:05d}.png')
                frame_count += 1
                time.sleep(1/fps)

    driver.quit()

def create_video_from_images(image_folder, output_video_name, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video_name, fourcc, fps, (width, height))

    for image in tqdm(images, desc="動画の作成"):
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(2)

    output_dir = 'slide_mov'
    os.makedirs(output_dir, exist_ok=True)

    capture_slides_as_png(output_dir, fps=30, duration=5)

    print("全てのスライドのキャプチャが完了しました。")

    create_video_from_images(output_dir, 'presentation_video.mp4', fps=30)

    print("動画の作成が完了しました。")
