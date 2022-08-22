## Simple mircoblog app API tests
This repo contains steps and tests for API test automation for API Autotests
Simple mircoblog app project.

### Installation
This repo uses 3.9 python.
* Create virtualenv with python 3.9 and activate it.
* Copy pip.conf in your virtualenv root folder
* Run `pip install -r requirements.txt`

Everything should be installed for now.

### Locally execution all tests
to run tests locally: `pytest`

### Locally execution smoke tests
`pytest -m smoke`

### Allure locally
* `pytest`
* `allure serve allure_results`

#### Linters & pre-commit hooks

black + flake8 + isort are used to keep the code nice and readable.

To install pre-commit run:  
`pre-commit install`

Everything is set for now!

If for some reason you really need to commit something that won't pass linters in CI, uninstall pre-commit using:  
`pre-commit uninstall
