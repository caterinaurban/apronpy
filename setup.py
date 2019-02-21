from setuptools import setup, find_packages

setup(
    name='apronpy',
    version='0.2.1',
    author='Caterina Urban',
    author_email='caterina.urban@gmail.com',
    description='Python Interface for the APRON Numerical Abstract Domain Library',
    long_description=open('README.md').read(),
    url='https://github.com/caterinaurban/apronpy',
    packages=find_packages(),
)
