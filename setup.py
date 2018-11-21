from setuptools import setup, find_packages

config = {
    'name': 'apronpy',
    'version': '0.1',
    'author': 'Caterina Urban',
    'author_email': 'caterina.urban@gmail.com',
    'description': 'Python Interface for the APRON Numerical Abstract Domain Library',
    'url': 'https://github.com/caterinaurban/apronpy',
    'packages': find_packages(),
}

setup(**config)
