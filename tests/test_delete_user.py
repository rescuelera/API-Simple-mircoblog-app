import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateUserBody
from user_data import INVALID_ID, RESPONSE_USER_ID_WITH_INVALID_UID


@allure.story("User functionality")
class TestDeleteUser:
    @pytest.mark.smoke
    @allure.title("Delete user positive")
    @pytest.mark.xfail(reason="order of users are not correct for get all users")
    def test_delete_user_ok(self, user_api):
        with allure.step("create user"):
            data = dataclasses.asdict(CreateUserBody())
            r: Response = user_api.post_user(body=data)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            with soft_assertions():
                assert isinstance(json_obj, dict), "json_obj must be equal dict"
                assert json_obj["name"] == data["name"], f"json_obj_last['name'] must be equal {data['name']}"
                assert json_obj["email"] == data["email"], f"json_obj_last['email'] must be equal {data['email']}"
                assert not json_obj["is_admin"], "json_obj_last['is_admin'] must be equal False"
                assert not json_obj["is_active"], "json_obj_last['is_active'] must be equal False"
            user_id = json_obj["id"]
        with allure.step("get all users and check the last one"):
            r: Response = user_api.get_user()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            with soft_assertions():
                assert isinstance(json_obj, list), "json_obj must be equal list"
                assert json_obj_last["name"] == data["name"], f"json_obj_last['name'] must be equal {data['name']}"
                assert json_obj_last["email"] == data["email"], f"json_obj_last['email'] must be equal {data['email']}"
                assert json_obj_last["is_admin"] is False, "json_obj_last['is_admin'] must be equal False"
                assert json_obj_last["is_active"] is False, "json_obj_last['is_active'] must be equal False"
                assert json_obj_last["id"] == user_id, f"json_obj_last['id'] must be equal {user_id}"

        with allure.step("delete user"):
            r: Response = user_api.delete_user(user_id=user_id)
            assert r.status_code == 200, "Status code must be 200"

        with allure.step("get all user and check that the deleted user not displayed"):
            r: Response = user_api.get_user()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            assert json_obj_last["id"] != user_id, f"json_obj_last['id'] must be not equal {user_id}"

        with allure.step("get user by user_id and check that is not displayed"):
            r: Response = user_api.get_user_by_id(user_id=user_id)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            with soft_assertions():
                assert r.status_code == 200, "Status code must be 200"
                assert json_obj is None, "json_obj must be equal None"

    @allure.title("Check delete user by non-existent user_id ")
    @pytest.mark.parametrize(
        "not_existing_user_id",
        [
            0,
            -1,
            36893488147419103232,
        ],
        ids=["0", "-1", "36893488147419103232"],
    )
    @pytest.mark.xfail(reason="500 error")
    def test_delete_user_with_non_existent_user_id(self, not_existing_user_id, user_api):
        r: Response = user_api.delete_user(user_id=not_existing_user_id)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 200, "Status code must be 200"
            assert json_obj is None, "json_obj must be equal None"

    @allure.title("Check delete user with invalid user_id ")
    def test_delete_user_with_invalid_user_id(self, user_api):
        r: Response = user_api.delete_user(user_id=INVALID_ID)
        assert r.status_code == 422, "Status code must be 422"
        json_obj = r.json()
        assert (
            json_obj == RESPONSE_USER_ID_WITH_INVALID_UID
        ), f"json_obj must be equal {RESPONSE_USER_ID_WITH_INVALID_UID}"
