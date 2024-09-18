from setuptools import find_packages, setup

setup(
name='Sarvam',

version='0.0.1',

author= 'Sagar',

author_email='sagarbag25@gmail.com',

install_requires=["groq", "langchain", "streamlit", "python-dotenv", "PyPDF2"],

packages=find_packages()
)