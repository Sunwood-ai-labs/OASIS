import requests
from bs4 import BeautifulSoup
import re
import os

def get_site_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else ''
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else ''
    
    og_image = soup.find('meta', property='og:image')
    image_url = og_image['content'] if og_image else ''
    
    return {
        'title': title,
        'description': description,
        'image_url': image_url,
        'url': url
    }

def create_card_html(metadata):
    html = f"""
    <a href="{metadata['url']}" style="text-decoration: none; color: inherit;">
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; max-width: 400px; font-family: Arial, sans-serif; cursor: pointer; transition: box-shadow 0.3s;">
            <h2 style="margin-top: 0;">{metadata['title']}</h2>
            <p>{metadata['description']}</p>
            {f'<img src="{metadata["image_url"]}" style="max-width: 100%; height: auto;">' if metadata['image_url'] else ''}
            <p style="color: #0066cc; margin-bottom: 0;">{metadata['url']}</p>
        </div>
    </a>
    <style>
        a:hover > div {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
    </style>
    """
    return html

def generate_site_card(url):
    metadata = get_site_metadata(url)
    return create_card_html(metadata)

def save_html_to_file(html_content, filename):
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Site Card</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(full_html)
    print(f"HTMLファイルが {filename} として保存されました。")

def generate_and_save_site_card(url, filename):
    card_html = generate_site_card(url)
    save_html_to_file(card_html, filename)

# 使用例
url = "https://github.com/Sunwood-ai-labs/OASIS"
filename = "site_card.html"
generate_and_save_site_card(url, filename)
