from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oasis-article",
    version="0.1.7",
    author="Sunwood-ai-labs",
    author_email="sunwood.ai.labs@gmail.com",
    description="WordPressへの投稿を自動化するパッケージ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sunwood-ai-labs/OASIS",
    packages=find_packages(include=['oasis', 'oasis.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "python-dotenv",
        "matplotlib",
        "japanize-matplotlib",
        "numpy",
        "tenacity",
        "litellm",
        "loguru",
        "click",
        "art",
    ],
    entry_points={
        "console_scripts": [
            "oasis=oasis.cli:main",
        ],
    },
    # パッケージに含めるデータファイル
    package_data={
        'oasis': [
            'models/*',
            'services/*',
        ],
    },
    include_package_data=True,
)
