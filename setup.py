from setuptools import setup, find_packages

setup(
    name='apronpy',
    version='0.6.5',
    author='Caterina Urban',
    author_email='caterina.urban@gmail.com',
    description='Python Interface for the APRON Numerical Abstract Domain Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/caterinaurban/apronpy',
    packages=find_packages(),
)
