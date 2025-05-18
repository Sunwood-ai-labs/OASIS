## O.A.S.I.S

**～ Optimized Article Sorting Intelligent System ～**

<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/OASIS.png" width="100%">
</p>

<p align="center">
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
</p>

<p align="center">
  <a href="https://hamaruki.com/"><b>[ Website ]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[ GitHub ]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[ Twitter ]</b></a> •
  <a href="https://hamaruki.com/"><b>[ Official Blog ]</b></a>
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/OASIS/blob/main/README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
  <a href="https://github.com/Sunwood-ai-labs/OASIS/blob/main/docs/README.en.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</p>


>[!IMPORTANT]
>This repository's release notes, README, and nearly 90% of commit messages are generated using [claude.ai](https://claude.ai/) and [ChatGPT4](https://chatgpt.com/) powered by [AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), and [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II).

OASIS is a Python package that automates posting from Markdown files to WordPress, Qiita, Note, and Zenn. It is packed with convenient features such as automatic category and tag suggestions using LLMs and automatic thumbnail image uploading.

## What's New

- **v0.9.3**: 
  - Updated English README and improved command-line option descriptions.
  - For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.9.3).
- **v0.9.2**: 
  - Includes features for setting Zenn API V2 to public, enhancement of Instagram auto-posting (experimental feature), addition of new tags, README translation workflow, and other improvements.
  - For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.9.2).

<details>
  <summary>View Past Updates</summary>

  ---
- **v0.8.0**: 
  - Added Streamlit-based web UI.
  - Improved the command-line interface and added Streamlit application launch options.
  - Added new categories and tags related to AI.
  - For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.8.0).
- **v0.7.0**: 
  - Added cross-posting to Zenn.
  - Support for rendering Mermaid diagrams on WordPress and Note.
  - For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.7.0).
- **v0.6.0**: 
  - Added cross-posting to Zenn.
  - Support for rendering Mermaid diagrams on WordPress and Note.
  - For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.6.0).
- **v0.5.0**: 
  - Added iframely support to the link preview generation function (experimental feature).
  - Note API v2 now allows you to post content faster than before by inserting HTML directly.
  - For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.5.0).
- **v0.4.3**: Significantly improved posting to Note.
  - Support for more Markdown elements.
  - For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.3).
- **v0.4.0**: Added cross-posting to Note. Automate article posting from Markdown files to Note, making it easy to share content on multiple platforms. For details, see the [release notes](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.0).
- **Past versions:** [Releases](https://github.com/Sunwood-ai-labs/OASIS/releases)
</details>

  ---

## Demo

### CLI Demo

https://github.com/user-attachments/assets/742c5822-04ec-4f9b-98fb-42fc3a101ab6

### Web UI Demo

https://github.com/user-attachments/assets/ff0a2099-dcd0-4fe5-b60b-ded3f2f55fe4

## Getting Started

OASIS allows you to efficiently post from Markdown files to WordPress, Qiita, Note, and Zenn. It comes with convenient features such as automatic category and tag suggestions using LLMs and automatic thumbnail image uploading.

## Installation

```bash
pip install -U oasis-article
```

## Usage

### Using the Command Line:

```bash
oasis --folder_path /path/to/your/folder
```

### Options

OASIS provides numerous options to customize various settings and functionalities. Here is a list of the main options:

#### Basic Options
- `--folder_path`: Path to the folder to process (required)
- `-app`, `--streamlit-app`: Launch the Streamlit-based web UI

#### Specifying Posting Destinations
- `--qiita`: Post to Qiita as well
- `--note`: Post to Note as well
- `--wp`: Post to WordPress as well
- `--zenn`: Post to Zenn as well

#### WordPress Settings
- `--wp-user`: WordPress username
- `--wp-pass`: WordPress password
- `--wp-url`: WordPress URL

#### Qiita Settings
- `--qiita-token`: Qiita API token
- `--qiita-post-publish`: Post Qiita articles with public settings (default is private)

#### Note Settings
- `--note-email`: Note email address
- `--note-password`: Note password
- `--note-user-id`: Note user ID
- `--note-publish`: Publish to Note (default is save as draft)

#### Zenn Settings
- `--zenn-output-path`: Output folder for generating article files with Zenn API V2
- `--zenn-publish`: Set the article to public with Zenn API V2

#### Firefox Settings
- `--firefox-binary-path`: Path to the Firefox executable
- `--firefox-profile-path`: Path to the Firefox profile to use
- `--firefox-headless`: Headless mode for Firefox

#### Other
- `--llm-model`: LLM model to use
- `--max-retries`: Maximum number of retries for LLM requests

### Example Usage

```bash
oasis --folder_path example\article\roomba01 --qiita --qiita-post-publish --note --wp --zenn --firefox-headless
oasis --folder_path article_draft\21_Hunk --qiita --note --wp --zenn --firefox-headless
```

### Using from a Python Script:

```python
from oasis import OASIS

oasis = OASIS()
result = oasis.process_folder("/path/to/your/folder", post_to_qiita=True, post_to_note=True, post_to_wp=True, post_to_zenn=True)  # Also post to Qiita, Note, WordPress, and Zenn
print(result)
```

### Using the Web UI:

```bash
oasis -app
```

or

```bash
oasis --streamlit-app
```

## Configuration

Use environment variables for configuration:
Refer to [.env.example](.env.example) for an example.

- `AUTH_USER`: WordPress username
- `AUTH_PASS`: WordPress password
- `BASE_URL`: WordPress site URL
- `LLM_MODEL`: LLM model to use (default: "gemini/gemini-1.5-pro-latest")
- `QIITA_TOKEN`: Qiita API token (required for posting to Qiita)
- `NOTE_EMAIL`: Email address associated with the Note account
- `NOTE_PASSWORD`: Note account password
- `NOTE_USER_ID`: Note user ID
- `FIREFOX_BINARY_PATH`: Path to the Firefox executable (optional)
- `FIREFOX_PROFILE_PATH`: Path to the Firefox profile to use (optional)

## Sample Scripts

The `example/script` folder contains sample scripts for trying out various OASIS features.

- `demo_note_api.py`: Sample script for posting articles to Note using Note API v1
- `demo_note_api_v2.py`: Sample script for posting articles to Note using Note API v2
- `demo_qiita_api.py`: Sample script for posting articles to Qiita using the Qiita API
- `demo_url2card.py`: Sample script for generating website cards from URLs

These scripts are a good starting point for understanding and experimenting with OASIS functionality.

## About ZennAPI V2

ZennAPI V2 leverages the integration of Zenn and GitHub. It generates Zenn article files (.md) in the folder specified by the `--zenn-output-path` option. Push the generated article files to a GitHub repository to publish the article on Zenn.

## Contributions

If you'd like to contribute to the development of OASIS, please visit the GitHub repository. We welcome issue reports and pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgements

We would like to express our gratitude to the individuals who have made significant contributions to the development of OASIS.

- We referred to [Mr-SuperInsane/NoteClient](https://github.com/Mr-SuperInsane/NoteClient) for the development of the Note API.