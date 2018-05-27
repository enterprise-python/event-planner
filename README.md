# Event Planner

[![Build Status](https://travis-ci.org/enterprise-python/event-planner.svg?branch=develop)](https://travis-ci.org/enterprise-python/event-planner)
[![Coverage Status](https://coveralls.io/repos/github/enterprise-python/event-planner/badge.svg?branch=develop)](https://coveralls.io/github/enterprise-python/event-planner?branch=develop)

# Requirements

* python3 (minimum Python 3.4)
* python3-venv

# Installation

```bash
git clone https://github.com/fisheye36/event-planner.git
cd event-planner/
python3 -m venv .env
. .env/bin/activate
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
