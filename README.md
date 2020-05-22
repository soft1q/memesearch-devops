# memesearch-devops [![Build Status](https://travis-ci.com/soft1q/memesearch-devops.svg?branch=master)](https://travis-ci.com/soft1q/memesearch-devops)

Source code of this web-site: https://cromtus.ru/memesearch/#/search

Repo for DevOps practice

## Build Requirements:
1. Packages
    1. python 3.5+
    2. node.js
    3. tesseract-ocr 3.04+
    4. pip3
    5. venv
2. Python packages can be found in requirements.txt 
3. Hardware & OS:
    1. Unix system
    2. At least 1 GB RAM
    3. At least 1 CPU
 
## Running the project:
 - Clone repo
 - `python -m venv venv`
 - `pip3 install -r requirements.txt`
 - `python manage-memesearch.py runserver`
 - In other terminal `cd frontend` then `npm run build`
