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
