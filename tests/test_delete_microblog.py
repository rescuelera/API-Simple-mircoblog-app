import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateMicroblogBody
from user_data import INVALID_ID, RESPONSE_MICROPOST_ID_WITH_INVALID_UID


@allure.story("Microblog functionality")
class TestDeleteMicroblog:
    @pytest.mark.smoke
    @allure.title("Delete microblog positive")
    def test_delete_microblog_ok(self, microblog_api):
        with allure.step("create microblog"):
            data = dataclasses.asdict(CreateMicroblogBody(owner=1))
            r: Response = microblog_api.post_microblog(body=data)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            with soft_assertions():
                assert isinstance(json_obj, dict), "json_objmust be dict"
                assert json_obj["title"] == data["title"], "json_obj['title'] must be equal {data['title']}"
                assert json_obj["text"] == data["text"], "json_obj['text'] must be equal {data['text']}"
                assert json_obj["owner"] == data["owner"], "json_obj['owner'] must be equal {data['owner']}"
            micropost_id = json_obj["id"]

        with allure.step("get microblog"):
            r: Response = microblog_api.get_microblog()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            with soft_assertions():
                assert isinstance(json_obj, list)
                assert json_obj_last["title"] == data["title"], f"json_obj['title'] must be equal {data['title']}"
                assert json_obj_last["text"] == data["text"], f"json_obj['text'] must be equal {data['text']}"
                assert json_obj_last["owner"] == data["owner"], f"json_obj['owner'] must be equal {data['owner']}"
                assert json_obj_last["id"] == micropost_id, f"json_obj['id'] must be equal {data['id']}"

        with allure.step("delete microblog"):
            r: Response = microblog_api.delete_microblog(micropost_id=micropost_id)
            assert r.status_code == 200, "Status code must be 200"

        with allure.step("get all microblogs and check that the deleted microblog is not displyed"):
            r: Response = microblog_api.get_microblog()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            assert json_obj_last["id"] != micropost_id, f"json_obj_last['id'] must be not equal {micropost_id}"

        with allure.step("get microblog by micropost_id and check that is not displayed"):
            r: Response = microblog_api.get_microblog_by_micropost_id(micropost_id=micropost_id)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            with soft_assertions():
                assert r.status_code == 200, "Status code must be 200"
                assert json_obj is None, "json_obj code must be None"

    @allure.title("Check get microblog by non-existenting micropost_id ")
    @pytest.mark.parametrize(
        "non_existent_micropost_id",
        [
            0,
            -1,
            36893488147419103232,
        ],
        ids=["0", "-1", "36893488147419103232"],
    )
    @pytest.mark.xfail(reason="500 error")
    def test_delete_microblog_with_non_existent_micropost_id(self, non_existent_micropost_id, microblog_api):
        r: Response = microblog_api.delete_microblog(micropost_id=non_existent_micropost_id)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 200, "Status code must be 200"
            assert json_obj is None, "json_obj must be equal None"

    @allure.title("Check delete microblog with invalid micropost_id ")
    def test_delete_microblog_with_invalid_micropost_id(self, microblog_api):
        r: Response = microblog_api.delete_microblog(micropost_id=INVALID_ID)
        assert r.status_code == 422, "Status code must be 422"
        json_obj = r.json()
        assert (
            json_obj == RESPONSE_MICROPOST_ID_WITH_INVALID_UID
        ), f"json_obj must be equal {RESPONSE_MICROPOST_ID_WITH_INVALID_UID}"
