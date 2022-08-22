import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateUserBody
from data.response_models.user import User
from steps.user import UsersApiSteps


@allure.story("User functionality")
class TestGetUser:
    @allure.title("Check get user positive")
    @pytest.mark.smoke
    def test_get_user_ok(self):
        with allure.step("create user"):
            data = dataclasses.asdict(CreateUserBody())
            api = UsersApiSteps()
            r: Response = api.post_user(body=data)
            assert r.status_code == 200
            json_obj = r.json()
            User(**json_obj)
            with soft_assertions():
                assert isinstance(json_obj, dict)
                assert json_obj["name"] == data["name"]
                assert json_obj["email"] == data["email"]
                assert json_obj["is_admin"] is False
                assert json_obj["is_active"] is False

        with allure.step("get user"):
            api = UsersApiSteps()
            r: Response = api.get_user()
            assert r.status_code == 200
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            with soft_assertions():
                assert isinstance(json_obj, list)
                assert json_obj_last["name"] == data["name"]
                assert json_obj_last["email"] == data["email"]
                assert json_obj_last["is_admin"] is False
                assert json_obj_last["is_active"] is False
