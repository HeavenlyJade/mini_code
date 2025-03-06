# backend
Ikas Advanced Process Control System.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Requirements
* python 3.9

## Installation

### Using poetry
Make sure you have installed [poetry](https://python-poetry.org/)

```bash
poetry install
```

### Using requirements.txt
```bash
pip install -r requirements.txt
```
## Usage

```bash
gunicorn autoapp:app
        --bind 127.0.0.1:5000
        -w 4
        -k gevent
        --access-logfile -
        --error-logfile -
```

## License
IKAS


