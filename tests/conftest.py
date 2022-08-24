import pytest

from steps.mircoblog import MicroblogApiSteps
from steps.user import UsersApiSteps


@pytest.fixture
def microblog_api():
    return MicroblogApiSteps()


@pytest.fixture
def user_api():
    return UsersApiSteps()
