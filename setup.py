# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

p_version = "2.0.2"

with open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="shablbot",
    version=p_version,
    author="Alexandr Drachenin",
    author_email="alexdrachenin98@gmail.com",
    packages=find_packages(),
    url="https://github.com/Blackgard/shablbot",
    download_url="https://github.com/Blackgard/shablbot/tarball/v{0}".format(p_version),
    license="MIT",
    description="Бот написанный на Python для социальной сети Вконтакте, работающий через VkBotLongPull",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=[
        "python",
        "bot",
        "vk",
        "template"
    ],
    python_requires='>=3.9',
    install_requires = [
        "vk-api==11.9.4",
        "requests==2.26.0",
        "pytz==2021.1",
        "loguru==0.5.3",
        "python-dotenv==0.19.0",
        "pydantic==1.8.2",
        "anytree==2.8.0",
        "certifi==2021.10.8",
        "charset-normalizer==2.0.7",
        "colorama==0.4.4",
        "idna==3.3",
        "six==1.16.0",
        "typing-extensions==3.10.0",
        "urllib3==1.26.7",
        "win32-setctime==1.0.3"
    ],
)
