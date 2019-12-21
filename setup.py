from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='async-process-server', 
    version='0.0.1dev',
    description='Runs a server that manages background processes asynchronously', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/the_jocr/async-process-server',
    author='Jordan Crawford',
    author_email='Jordanac95@gmail.com',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'aiofiles',
        'starlette',
        'uvicorn',
    ],
    extras_require={ }, 
    entry_points={  
        'console_scripts': [
            'process-server=server.main:main',
        ],
    },
)
