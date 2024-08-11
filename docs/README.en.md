## O.A.S.I.S - Optimized Article Sorting Intelligent System

<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/OASIS.png" width="100%">
<br>
<h1 align="center"> O.A.S.I.S </h1>
<h2 align="center">
  ～ Optimized Article Sorting Intelligent System ～
<br>
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/oasis-article">
<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/oasis-article">
<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/oasis-article">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/oasis-article">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/oasis-article">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/oasis-article">
<a href="https://github.com/Sunwood-ai-labs/OASIS" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=OASIS&message=Sunwood-ai-labs&color=blue&logo=github"></a>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/OASIS">
<a href="https://github.com/Sunwood-ai-labs/OASIS"><img alt="forks - Sunwood-ai-labs" src="https://img.shields.io/github/forks/OASIS/Sunwood-ai-labs?style=social"></a>
<a href="https://github.com/Sunwood-ai-labs/OASIS"><img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/OASIS"></a>
<a href="https://github.com/Sunwood-ai-labs/OASIS"><img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/OASIS"></a>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/OASIS?color=red">
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/Sunwood-ai-labs/OASIS?sort=semver&color=orange">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/OASIS/publish-to-pypi.yml">
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[ Website ]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[ GitHub ]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[ Twitter ]</b></a> •
  <a href="https://hamaruki.com/"><b>[ Official Blog ]</b></a>
</p>
   <br>
   <a href="https://github.com/Sunwood-ai-labs/OASIS/blob/main/README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
   <a href="https://github.com/Sunwood-ai-labs/OASIS/blob/main/docs/README.en.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</h2>

</p>

>[!IMPORTANT]
>This repository's release notes, README, and nearly 90% of the commit messages are generated using [claude.ai](https://claude.ai/) and [ChatGPT4](https://chatgpt.com/) through [AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), and [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II).

OASIS is a Python package that automates posting from Markdown files to WordPress, Qiita, Note, and Zenn. It is packed with useful features such as automatic category and tag suggestions using LLMs, and automatic thumbnail image uploads.

## Update Information

- **v0.9.2**: 
  - Includes enhanced Zenn API V2 publishing settings, Instagram automatic posting (experimental feature), new tags added, README translation workflow, and other improvements.
  - See [Release Notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.9.2) for more details.

<details>
  <summary>Past Update Information</summary>

  ---
- **v0.8.0**: 
  - Added a Streamlit-based web UI.
  - Improved the command-line interface and added an option to launch the Streamlit application.
  - Added new categories and tags related to AI.
  - See [Release Notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.8.0) for more details.
- **v0.7.0**: 
  - Added cross-posting functionality to Zenn.
  - Implemented support for Mermaid diagrams in WordPress and Note.
  - See [Release Notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.7.0) for more details.
- **v0.6.0**: 
  - Added cross-posting functionality to Zenn.
  - Implemented support for Mermaid diagrams in WordPress and Note.
  - See [Release Notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.6.0) for more details.
- **v0.5.0**: 
  - Added iframely support to the link preview generation feature (experimental).
  - Note API v2 now allows direct insertion of HTML, making content posting faster than the traditional method.
  - See [Release Notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.5.0) for more details.
- **v0.4.3**: Significantly improved posting functionality to Note.
  - Supports more elements in Markdown.
  - See [Release Notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.3) for more details.
- **v0.4.0**: Added cross-posting functionality to Note. Automate article posting from Markdown files to Note, allowing you to easily share your content across multiple platforms. See [Release Notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.0) for more details.
- **Past Version Information:** [Releases](https://github.com/Sunwood-ai-labs/OASIS/releases)
</details>

  ---

## Demo

### CLI Demo

https://github.com/user-attachments/assets/742c5822-04ec-4f9b-98fb-42fc3a101ab6

### Web UI Demo

https://github.com/user-attachments/assets/ff0a2099-dcd0-4fe5-b60b-ded3f2f55fe4

## Getting Started

OASIS allows you to efficiently post from Markdown files to WordPress, Qiita, Note, and Zenn. It is packed with useful features such as automatic category and tag suggestions using LLMs, and automatic thumbnail image uploads.

## Installation

```bash
pip install -U oasis-article
```

## Usage

### Using from the command line:

```bash
oasis --folder_path /path/to/your/folder
```

#### Options

- `--folder_path`: Path to the folder to be processed
- `--qiita`: Post to Qiita as well
- `--note`: Post to Note as well
- `--wp`: Post to WordPress as well
- `--zenn`: Post to Zenn as well
- `--wp-user`: WordPress username
- `--wp-pass`: WordPress password
- `--wp-url`: WordPress URL
- `--qiita-token`: Qiita API token
- `--note-email`: Note email address
- `--note-password`: Note password
- `--note-user-id`: Note user ID
- `--note-publish`: Publish to Note (if not specified, it will be saved as a draft)
- `--firefox-binary-path`: Path to the Firefox executable
- `--firefox-profile-path`: Path to the Firefox profile to use
- `--firefox-headless`: Headless mode for Firefox
- `--zenn-output-path`: Output folder for generating article files (.md) with ZennAPI V2
- `-app`, `--streamlit-app`: Launch the Streamlit-based web UI

Example:

```bash
oasis --folder_path example\article\roomba01 --qiita --note --wp --zenn --firefox-headless
oasis --folder_path article_draft\21_Hunk --qiita --note --wp --zenn --firefox-headless
```

### Using from a Python script:

```python
from oasis import OASIS

oasis = OASIS()
result = oasis.process_folder("/path/to/your/folder", post_to_qiita=True, post_to_note=True, post_to_wp=True, post_to_zenn=True)  # Also post to Qiita, Note, WordPress, Zenn
print(result)
```

### Using the web UI:

```bash
oasis -app
```

or

```bash
oasis --streamlit-app
```

## Configuration

Use environment variables for configuration:
Refer to [.env.example](.env.example).

- `AUTH_USER`: WordPress username
- `AUTH_PASS`: WordPress password
- `BASE_URL`: WordPress site URL
- `LLM_MODEL`: LLM model to use (default: "gemini/gemini-1.5-pro-latest")
- `QIITA_TOKEN`: Qiita API token (required for posting to Qiita)
- `NOTE_EMAIL`: Email address associated with your Note account
- `NOTE_PASSWORD`: Password for your Note account
- `NOTE_USER_ID`: Note user ID
- `FIREFOX_BINARY_PATH`: Path to the Firefox executable (optional)
- `FIREFOX_PROFILE_PATH`: Path to the Firefox profile to use (optional)

## Sample Scripts

The `example/script` folder contains sample scripts to try out various OASIS features.

- `demo_note_api.py`: Sample script for posting articles to Note using Note API v1
- `demo_note_api_v2.py`: Sample script for posting articles to Note using Note API v2
- `demo_qiita_api.py`: Sample script for posting articles to Qiita using the Qiita API
- `demo_url2card.py`: Sample script for generating website cards from URLs

These scripts provide a good starting point for understanding and trying out OASIS features.

## About ZennAPI V2

ZennAPI V2 leverages the integration between Zenn and GitHub. It generates Zenn article files (.md) in the folder specified by the `--zenn-output-path` option. When you push the generated article files to your GitHub repository, the articles will be published on Zenn.

## Contribution

If you would like to contribute to the development of OASIS, please visit the GitHub repository. We welcome issue reports and pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgements

We would like to thank the following individuals for their significant contributions to the development of OASIS:

- We referenced [Mr-SuperInsane/NoteClient](https://github.com/Mr-SuperInsane/NoteClient) for the development of the Note API.

</readme>