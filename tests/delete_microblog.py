import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateMicroblogBody
from steps.mircoblog import MicroblogApiSteps
from user_data import INVALID_ID, RESPONSE_MICROPOST_ID_WITH_INVALID_UID


@allure.story("Microblog functionality")
class TestDeleteMicroblog:
    @pytest.mark.smoke
    @allure.title("Delete microblog positive")
    def test_delete_microblog_ok(self):
        with allure.step("create microblog"):
            data = dataclasses.asdict(CreateMicroblogBody(owner=1))
            api = MicroblogApiSteps()
            r: Response = api.post_microblog(body=data)
            assert r.status_code == 200
            json_obj = r.json()
            with soft_assertions():
                assert isinstance(json_obj, dict)
                assert json_obj["title"] == data["title"]
                assert json_obj["text"] == data["text"]
                assert json_obj["owner"] == data["owner"]
            micropost_id = json_obj["id"]
            # добавить на текущую дату

        with allure.step("get microblog"):
            api = MicroblogApiSteps()
            r: Response = api.get_microblog()
            assert r.status_code == 200
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            with soft_assertions():
                assert isinstance(json_obj, list)
                assert json_obj_last["title"] == data["title"]
                assert json_obj_last["text"] == data["text"]
                assert json_obj_last["owner"] == data["owner"]
                assert json_obj_last["id"] == micropost_id
                # добавить на текущую дату

        with allure.step("delete microblog"):
            api = MicroblogApiSteps()
            r: Response = api.delete_microblog(micropost_id=micropost_id)
            assert r.status_code == 200

        with allure.step("get all microblogs and check that the deleted microblog is not displyed"):
            api = MicroblogApiSteps()
            r: Response = api.get_microblog()
            assert r.status_code == 200
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            assert json_obj_last["id"] != micropost_id

        with allure.step("get microblog by micropost_id and check that is not displayed"):
            api = MicroblogApiSteps()
            r: Response = api.get_microblog_by_micropost_id(micropost_id=micropost_id)
            assert r.status_code == 200
            json_obj = r.json()
            with soft_assertions():
                assert r.status_code == 200
                assert json_obj is None

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
    @pytest.mark.xfail(reason="500 error")
    def test_delete_microblog_with_non_existent_micropost_id(self, non_existent_micropost_id):
        api = MicroblogApiSteps()
        r: Response = api.delete_microblog(micropost_id=non_existent_micropost_id)
        json_obj = r.json()
        with soft_assertions():
            assert r.status_code == 200
            assert json_obj is None

    @allure.title("Check delete microblog with invalid micropost_id ")
    def test_delete_microblog_with_invalid_micropost_id(self):
        api = MicroblogApiSteps()
        r: Response = api.delete_microblog(micropost_id=INVALID_ID)
        assert r.status_code == 422
        json_obj = r.json()
        assert json_obj == RESPONSE_MICROPOST_ID_WITH_INVALID_UID
