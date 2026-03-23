import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'urfu-schedule-bot'
author = 'Your Name'
copyright = '2026, Your Name'
release = '0.1.0'
language = 'ru'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
