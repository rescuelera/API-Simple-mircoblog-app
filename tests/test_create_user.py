import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateUserBody
from data.response_models.user import User
from steps.user import UsersApiSteps


@allure.story("User functionality")
class TestCreateUser:
    @pytest.mark.smoke
    @allure.title("Check create user positive")
    def test_create_user_ok(self):
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

    @allure.title("Check create user negative without mandatory fields")
    @pytest.mark.parametrize("missing_param", ["name", "email", "password"])
    def test_create_user_without_mandatory_fields(self, missing_param):
        data = dataclasses.asdict(CreateUserBody())
        data.pop(missing_param)
        api = UsersApiSteps()
        r: Response = api.post_user(body=data)
        assert r.status_code == 422
        json_obj = r.json()
        assert isinstance(json_obj, dict)
        with soft_assertions():
            assert "detail" in json_obj
            assert json_obj["detail"][0]["loc"] == ["body", missing_param]
            assert json_obj["detail"][0]["msg"] == "field required"
            assert json_obj["detail"][0]["type"] == "value_error.missing"

    @allure.title("Check create user negative with empty body")
    def test_create_user_with_empty_body(self):
        data = {}
        api = UsersApiSteps()
        r: Response = api.post_user(body=data)
        assert r.status_code == 422
        json_obj = r.json()
        assert isinstance(json_obj, dict)
        responce = {
            "detail": [
                {"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"},
                {"loc": ["body", "email"], "msg": "field required", "type": "value_error.missing"},
                {"loc": ["body", "password"], "msg": "field required", "type": "value_error.missing"},
            ]
        }
        assert json_obj == responce
