# Event Planner

[![Build Status](https://travis-ci.org/enterprise-python/event-planner.svg?branch=develop)](https://travis-ci.org/enterprise-python/event-planner)

# Requirements

* python3 (Python 3.6)
* python3-venv

# Installation

```bash
git clone https://github.com/fisheye36/event-planner.git
cd event-planner/
python3 -m venv .env
. .env/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
