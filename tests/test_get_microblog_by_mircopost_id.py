import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateMicroblogBody
from data.response_models.microblog import Microblog
from user_data import INVALID_ID, RESPONSE_MICROPOST_ID_WITH_INVALID_UID


@allure.story("Microblog functionality")
class TestGetMicroblogByMicropostid:
    @pytest.mark.smoke
    @allure.title("Check get microblog by micropost_id positive")
    @pytest.mark.xfail(reason="order of microblog are not correct for get all microblogs")
    def test_get_microblog_by_micropost_id_ok(self, microblog_api):
        with allure.step("create microblog"):
            data = dataclasses.asdict(CreateMicroblogBody(owner=1))
            r: Response = microblog_api.post_microblog(body=data)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            with soft_assertions():
                assert isinstance(json_obj, dict), "json_obj must be dict"
                assert json_obj["title"] == data["title"], f"json_obj['title'] must be equal {data['title']}"
                assert json_obj["text"] == data["text"], f"json_obj['text'] must be equal {data['text']}"
                assert json_obj["owner"] == data["owner"], f"json_obj['owner'] must be equal {data['owner']}"
            micropost_id = json_obj["id"]

        with allure.step("get all microblogs"):
            r: Response = microblog_api.get_microblog()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            with soft_assertions():
                assert isinstance(json_obj, list), "json_obj must be list"
                assert json_obj_last["title"] == data["title"], f"json_obj['title'] must be equal {data['title']}"
                assert json_obj_last["text"] == data["text"], f"json_obj['text'] must be equal {data['text']}"
                assert json_obj_last["owner"] == data["owner"], f"json_obj['owner'] must be equal {data['owner']}"
                assert json_obj_last["id"] == micropost_id, f"json_obj['id'] must be equal {micropost_id}"

        with allure.step("get microblog by micropost_id"):
            r: Response = microblog_api.get_microblog_by_micropost_id(micropost_id=micropost_id)
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            Microblog(**json_obj)
            with soft_assertions():
                assert isinstance(json_obj, dict)
                assert json_obj["title"] == data["title"], f"json_obj['title'] must be equal {data['title']}"
                assert json_obj["text"] == data["text"], f"json_obj['text'] must be equal {data['text']}"
                assert json_obj["owner"] == data["owner"], f"json_obj['owner'] must be equal {data['owner']}"
                assert json_obj["id"] == micropost_id, f"json_obj['id'] must be equal {micropost_id}"

    @allure.title("Check get microblog by non-existent micropost_id ")
    @pytest.mark.parametrize(
        "non_existent_micropost_id",
        [
            0,
            -1,
            36893488147419103232,
        ],
        ids=["0", "-1", "36893488147419103232"],
    )
    def test_get_microblog_with_non_existenting_micropost_id(self, non_existent_micropost_id, microblog_api):
        r: Response = microblog_api.get_microblog_by_micropost_id(micropost_id=non_existent_micropost_id)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 200, "Status code must be 200"
            assert json_obj is None, "json_obj must be equal None"

    @allure.title("Check get microblog with invalid micropost_id ")
    def test_get_microblog_with_invalid_micropost_id(self, microblog_api):
        r: Response = microblog_api.get_microblog_by_micropost_id(micropost_id=INVALID_ID)
        assert r.status_code == 422, "Status code must be 422"
        json_obj = r.json()
        assert (
            json_obj == RESPONSE_MICROPOST_ID_WITH_INVALID_UID
        ), f"json_obj must be equal {RESPONSE_MICROPOST_ID_WITH_INVALID_UID}"
