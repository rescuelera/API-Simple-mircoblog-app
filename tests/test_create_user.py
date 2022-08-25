import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateUserBody
from data.response_models.user import User


@allure.story("User functionality")
class TestCreateUser:
    @pytest.mark.smoke
    @allure.title("Check create user positive")
    def test_create_user_ok(self, user_api):
        data = dataclasses.asdict(CreateUserBody())
        r: Response = user_api.post_user(body=data)
        assert r.status_code == 200, "Status code must be 200"
        json_obj = r.json()
        User(**json_obj)
        with soft_assertions():
            assert isinstance(json_obj, dict), "json_obj must be dict"
            assert json_obj["name"] == data["name"], f"json_obj['name'] must be equal {data['name']}"
            assert json_obj["email"] == data["email"], f"json_obj['email'] must be equal {data['email']}"
            assert json_obj["is_admin"] is False, "is_admin must be equal False"
            assert json_obj["is_active"] is False, "is_active must be equal False"

    @allure.title("Check create user negative without mandatory fields")
    @pytest.mark.parametrize("missing_param", ["name", "email", "password"])
    def test_create_user_without_mandatory_fields(self, missing_param, user_api):
        data = dataclasses.asdict(CreateUserBody())
        data.pop(missing_param)
        r: Response = user_api.post_user(body=data)
        assert r.status_code == 422, "Status code must be 422"
        json_obj = r.json()
        assert isinstance(json_obj, dict), "json_obj must be dict"
        with soft_assertions():
            assert "detail" in json_obj
            assert json_obj["detail"][0]["loc"] == [
                "body",
                missing_param,
            ], f"json_obj['detail'][0]['loc'] must be equal 'body', {missing_param}"
            assert (
                json_obj["detail"][0]["msg"] == "field required"
            ), "json_obj['detail'][0]['msg'] must be equal 'field required'"
            assert (
                json_obj["detail"][0]["type"] == "value_error.missing"
            ), "json_obj['detail'][0]['type'] must be equal 'value_error.missing'"

    @allure.title("Check create user negative with empty body")
    def test_create_user_with_empty_body(self, user_api):
        r: Response = user_api.post_user(body={})
        assert r.status_code == 422, "Status code must be 422"
        json_obj = r.json()
        assert isinstance(json_obj, dict), "json_obj must be dict"
        response = {
            "detail": [
                {"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"},
                {"loc": ["body", "email"], "msg": "field required", "type": "value_error.missing"},
                {"loc": ["body", "password"], "msg": "field required", "type": "value_error.missing"},
            ]
        }
        assert json_obj == response, f"json_obj must be equal {response}"
