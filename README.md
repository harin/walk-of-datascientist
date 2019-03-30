# About

The goal of this project is to analyze the path data scientist from top tech companies took before becoming a data scientist at that company.

# Usage

This project uses the following devtools

- virtualenv
- autoenv

# Installation

You should have a selenium driver installed. For chrome, see the following link
https://sites.google.com/a/chromium.org/chromedriver/downloads

```python
virtualenv .
source ./bin/activate
pip install -r requirements.txt
```

# Usage

The script uses the following environment variables

BEGIN_URL = starting crawling page
LOGIN_EMAIL = email to login linkedin with
PASSWORD = password for linkedin

```python
python scrape.py
```
