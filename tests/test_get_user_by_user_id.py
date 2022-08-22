import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateUserBody
from data.response_models.user import User
from steps.user import UsersApiSteps
from user_data import INVALID_ID, RESPONCE_USER_ID_WITH_INVALID_UID


@allure.story("User functionality")
class TestGetUserByUserId:
    @pytest.mark.smoke
    @allure.title("Check get user by user_id positive")
    def test_get_user_by_user_id_ok(self):
        with allure.step("create user"):
            data = dataclasses.asdict(CreateUserBody())
            api = UsersApiSteps()
            r: Response = api.post_user(body=data)
            assert r.status_code == 200
            json_obj = r.json()
            user_id = json_obj["id"]
            with soft_assertions():
                assert isinstance(json_obj, dict)
                assert json_obj["name"] == data["name"]
                assert json_obj["email"] == data["email"]
                assert not json_obj["is_admin"]
                assert not json_obj["is_active"]
            user_id = json_obj["id"]
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
                assert json_obj_last["id"] == user_id

        with allure.step("get user by user id"):
            api = UsersApiSteps()
            r: Response = api.get_user_by_id(user_id=user_id)
            json_obj = r.json()
            User(**json_obj)
            with soft_assertions():
                assert isinstance(json_obj, dict)
                assert r.status_code == 200
                assert json_obj["name"] == data["name"]
                assert json_obj["email"] == data["email"]
                assert json_obj["id"] == user_id
                assert json_obj["is_admin"] is False
                assert json_obj["is_active"] is False
                assert json_obj["id"] == user_id

    @allure.title("Check get user by non-existent user_id")
    @pytest.mark.parametrize(
        "non_existent_user_id",
        [
            0,
            -1,
            36893488147419103232,
        ],
        ids=["0", "-1", "36893488147419103232"],
    )
    def test_get_user_with_non_existent_user_id(self, non_existent_user_id):
        api = UsersApiSteps()
        r: Response = api.get_user_by_id(user_id=non_existent_user_id)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 200
            assert json_obj is None

    @allure.title("Check get user with invalid user_id")
    def test_get_microblog_with_invalid_micropost_id(self):
        api = UsersApiSteps()
        r: Response = api.get_user_by_id(user_id=INVALID_ID)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 422
            assert json_obj == RESPONCE_USER_ID_WITH_INVALID_UID
