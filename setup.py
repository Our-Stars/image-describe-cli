from setuptools import setup, find_packages

setup(
    name="image-describe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["openai>=1.0"],
    entry_points={
        "console_scripts": [
            "image-describe=image_describe.cli:main",
        ],
    },
)
