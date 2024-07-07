
import requests
from bs4 import BeautifulSoup
import hashlib

def get_site_metadata(url):
    try:
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
    except:
        return {
            'title': url,
            'description': '',
            'image_url': '',
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


def generate_iframely_embed(url):
    # URLのハッシュを生成してユニークなIDとして使用
    url_hash = hashlib.md5(url.encode()).hexdigest()
    
    embed_html = f"""
    <div class="iframely-embed">
        <div class="iframely-responsive" style="padding-bottom: 0px; height: 450px;">
            <iframe allowfullscreen="" allow="autoplay *; encrypted-media *; ch-prefers-color-scheme *" 
                    src="//cdn.iframe.ly/{url_hash}?v=1&amp;app=1" 
                    style="box-shadow: rgba(0, 0, 0, 0.06) 0px 1px 3px;">
            </iframe>
        </div>
    </div>
    <script async="" src="//cdn.iframe.ly/embed.js" charset="utf-8"></script>
    """
    
    return embed_html
