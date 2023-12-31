from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'tax-calculator',
    author = 'Xiangyu Wang',
    author_email = 'wwrechard@gmail.com',
    description = 'A simple tax estimation tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = 'MIT',
    keywords = 'tax estimation',
    url = 'https://github.com/wwrechard/tax-calculator',
    packages = find_packages(),
    zip_safe= False,
    classifiers = [
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3',
    ],
    include_package_data = False,
    install_requires = [
      'numpy',
      'streamlit',
    ],
    tests_require = [
    ],
    extras_require = {
    },
)
