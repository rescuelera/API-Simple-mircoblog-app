import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateUserBody
from data.response_models.user import User


@allure.story("User functionality")
class TestGetUser:
    @allure.title("Check get user positive")
    @pytest.mark.smoke
    def test_get_user_ok(self, user_api):
        with allure.step("create user"):
            data = dataclasses.asdict(CreateUserBody())
            r: Response = user_api.post_user(body=data)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            user_id = json_obj["id"]
            User(**json_obj)
            with soft_assertions():
                assert isinstance(json_obj, dict), "json_obj must be equal dict"
                assert json_obj["name"] == data["name"], f"json_obj['name'] must be equal {data['name']}"
                assert json_obj["email"] == data["email"], f"json_obj['email'] must be equal {data['email']}"
                assert json_obj["is_admin"] is False, "json_obj['is_admin'] must be equal False"
                assert json_obj["is_active"] is False, "json_obj['is_active'] must be equal False"

        with allure.step("get user"):
            r: Response = user_api.get_user()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            assert isinstance(json_obj, list), "json_obj must be list"
            for obj in json_obj:
                if obj["id"] == user_id:
                    with soft_assertions():
                        assert obj["name"] == data["name"], f"json_obj['name'] must be equal {data['name']}"
                        assert obj["email"] == data["email"], f"json_obj['email'] must be equal {data['email']}"
                        assert obj["is_admin"] is False, "json_obj['is_admin'] must be equal False"
                        assert obj["is_active"] is False, "json_obj['is_active'] must be equal False"
