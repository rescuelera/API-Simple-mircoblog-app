import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateUserBody
from data.response_models.user import User
from user_data import INVALID_ID, RESPONSE_USER_ID_WITH_INVALID_UID


@allure.story("User functionality")
class TestGetUserByUserId:
    @pytest.mark.smoke
    @allure.title("Check get user by user_id positive")
    def test_get_user_by_user_id_ok(self, user_api):
        with allure.step("create user"):
            data = dataclasses.asdict(CreateUserBody())
            r: Response = user_api.post_user(body=data)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            with soft_assertions():
                assert isinstance(json_obj, dict), "json_obj must be dict"
                assert json_obj["name"] == data["name"], f"json_obj['name'] must be equal {data['name']}"
                assert json_obj["email"] == data["email"], f"json_obj['email'] must be equal {data['email']}"
                assert json_obj["is_admin"] is False, "json_obj['is_admin'] must be equal False"
                assert json_obj["is_active"] is False, "json_obj['is_active'] must be equal False"

            user_id = json_obj["id"]
        with allure.step("get user"):
            r: Response = user_api.get_user()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            with soft_assertions():
                assert isinstance(json_obj, list)
                assert json_obj_last["name"] == data["name"], f"json_obj_last['name'] must be equal {data['name']}"
                assert json_obj_last["email"] == data["email"], f"json_obj_last['email'] must be equal {data['email']}"
                assert json_obj_last["is_admin"] is False, "json_obj_last['is_admin'] must be equal False"
                assert json_obj_last["is_active"] is False, "json_obj_last['is_active'] must be equal False"
                assert json_obj_last["id"] == user_id, f"json_obj_last['id'] must be equal {user_id}"

        with allure.step("get user by user id"):
            r: Response = user_api.get_user_by_id(user_id=user_id)
            json_obj = r.json()
            User(**json_obj)
            with soft_assertions():
                assert isinstance(json_obj, dict), "json_obj must be equal dict"
                assert r.status_code == 200, "Status code must be 200"
                assert json_obj["name"] == data["name"], f"json_obj_last['name'] must be equal {data['name']}"
                assert json_obj["email"] == data["email"], f"json_obj_last['email'] must be equal {data['email']}"
                assert json_obj["id"] == user_id, f"json_obj_last['id'] must be equal {user_id}"
                assert json_obj["is_admin"] is False, "json_obj_last['is_admin'] must be equal False"
                assert json_obj["is_active"] is False, "json_obj_last['is_active'] must be equal False"
                assert json_obj["id"] == user_id, f"json_obj_last['id'] must be equal {user_id}"

    @allure.title("Check get user by non-existenting user_id")
    @pytest.mark.parametrize(
        "non_existent_user_id",
        [
            0,
            -1,
            36893488147419103232,
        ],
        ids=["0", "-1", "36893488147419103232"],
    )
    def test_get_user_with_non_existent_user_id(self, non_existent_user_id, user_api):
        r: Response = user_api.get_user_by_id(user_id=non_existent_user_id)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 200, "Status code must be 200"
            assert json_obj is None, "json_obj must be equal None"

    @allure.title("Check get user with invalid user_id")
    def test_get_microblog_with_invalid_micropost_id(self, user_api):
        r: Response = user_api.get_user_by_id(user_id=INVALID_ID)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 422, "Status code must be 422"
            assert (
                json_obj == RESPONSE_USER_ID_WITH_INVALID_UID
            ), f"json_obj must be equal {RESPONSE_USER_ID_WITH_INVALID_UID}"
