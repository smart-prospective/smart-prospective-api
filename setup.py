import pathlib
from setuptools import setup

# The text of the README file
README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(name='smart-prospective-api',
      version='1.0.0',
      description='The Official Python client for Smart Prospective API',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/smart-prospective/smart-prospective-api',
      author='Smart Prospective',
      author_email='dev@smartprospective.com',
      license='MIT',
      packages=['smart_prospective_api'],
      install_requires=['requests'],
      zip_safe=False)
