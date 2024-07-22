import markdown
from jinja2 import Template
from weasyprint import HTML
from pdf2image import convert_from_path
from litellm import completion
import os
import argparse
from loguru import logger

# loguruの設定
logger.add("process.log", rotation="500 MB")

# Poppler のパスを設定 (Windows の場合)
POPPLER_PATH = r"C:\Prj\poppler-24.07.0\Library\bin"  # 実際のパスに変更してください

def read_markdown(file_path):
    logger.info(f"マークダウンファイル '{file_path}' を読み込んでいます")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    logger.success(f"マークダウンファイルの読み込みが完了しました")
    return content

def convert_to_slides(markdown_text):
    logger.info("マークダウンをスライド形式に変換しています")
    prompt = f"Convert the following markdown to slide format:\n\n{markdown_text}"
    response = completion(
        model="gemini-1.5-pro-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    slide_content = response.choices[0].message.content
    logger.success("スライド形式への変換が完了しました")
    
    with open("intermediate_slide_content.txt", "w", encoding='utf-8') as f:
        f.write(slide_content)
    logger.info("中間スライドコンテンツを 'intermediate_slide_content.txt' に保存しました")
    
    return slide_content

def markdown_to_html(markdown_text):
    logger.info("マークダウンをHTMLに変換しています")
    html_content = markdown.markdown(markdown_text)
    logger.success("HTMLへの変換が完了しました")
    
    with open("intermediate_html_content.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    logger.info("中間HTMLコンテンツを 'intermediate_html_content.html' に保存しました")
    
    return html_content

def create_slide_html(slide_content):
    logger.info("スライドHTMLを生成しています")
    template = Template('''
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .slide { width: 1024px; height: 768px; padding: 40px; }
        </style>
    </head>
    <body>
        <div class="slide">
            {{ content }}
        </div>
    </body>
    </html>
    ''')
    html = template.render(content=slide_content)
    logger.success("スライドHTMLの生成が完了しました")
    
    with open("intermediate_slide_html.html", "w", encoding='utf-8') as f:
        f.write(html)
    logger.info("中間スライドHTMLを 'intermediate_slide_html.html' に保存しました")
    
    return html

def html_to_pdf(html_content, output_path):
    logger.info(f"HTMLをPDFに変換しています。出力先: {output_path}")
    HTML(string=html_content).write_pdf(output_path)
    logger.success("PDFへの変換が完了しました")

def pdf_to_image(pdf_path, image_path):
    logger.info(f"PDFを画像に変換しています。出力先: {image_path}")
    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=1, poppler_path=POPPLER_PATH)
        if images:
            images[0].save(image_path, 'PNG')
            logger.success("画像への変換が完了しました")
        else:
            logger.error("PDFから画像への変換に失敗しました：画像が生成されませんでした")
    except Exception as e:
        logger.error(f"PDFから画像への変換中にエラーが発生しました: {str(e)}")
        raise

def main(input_file, output_image, start_step):
    logger.info(f"処理を開始します。開始ステップ: {start_step}")
    
    if start_step <= 1:
        markdown_text = read_markdown(input_file)
    else:
        with open("intermediate_slide_content.txt", "r", encoding='utf-8') as f:
            markdown_text = f.read()
    
    if start_step <= 2:
        slide_text = convert_to_slides(markdown_text)
    else:
        with open("intermediate_slide_content.txt", "r", encoding='utf-8') as f:
            slide_text = f.read()
    
    if start_step <= 3:
        html_content = markdown_to_html(slide_text)
    else:
        with open("intermediate_html_content.html", "r", encoding='utf-8') as f:
            html_content = f.read()
    
    if start_step <= 4:
        slide_html = create_slide_html(html_content)
    else:
        with open("intermediate_slide_html.html", "r", encoding='utf-8') as f:
            slide_html = f.read()
    
    pdf_path = 'temp.pdf'
    if start_step <= 5:
        html_to_pdf(slide_html, pdf_path)
    
    if start_step <= 6:
        pdf_to_image(pdf_path, output_image)

    logger.success(f"スライド画像が {output_image} に保存されました")
    logger.info("全ての処理が完了しました")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="マークダウンをスライド画像に変換します")
    parser.add_argument("input_file", nargs='?', default=r"article_draft\54_Big\README.md", 
                        help="入力のマークダウンファイルのパス (デフォルト: %(default)s)")
    parser.add_argument("output_image", nargs='?', default="output.png", 
                        help="出力する画像ファイルのパス (デフォルト: %(default)s)")
    parser.add_argument("--start-step", type=int, default=5, choices=range(1, 7),
                        help="処理を開始するステップ (1-6) (デフォルト: %(default)s)")
    args = parser.parse_args()

    main(args.input_file, args.output_image, args.start_step)
