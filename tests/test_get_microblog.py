import dataclasses

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateMicroblogBody
from data.response_models.microblog import Microblog


@allure.story("Microblog functionality")
class TestGetMicroblog:
    @pytest.mark.smoke
    @allure.title("Check get microblog positive")
    def test_get_microblog_ok(self, microblog_api):
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
            id = json_obj["id"]

        with allure.step("get microblog"):
            r: Response = microblog_api.get_microblog()
            assert r.status_code == 200, "Status code must be 200"
            json_obj = r.json()
            json_obj_last = json_obj[-1]
            Microblog(**json_obj_last)

            with soft_assertions():
                assert isinstance(json_obj, list), "json_obj must be list"
                assert json_obj_last["title"] == data["title"], f"json_obj['title'] must be equal {data['title']}"
                assert json_obj_last["text"] == data["text"], f"json_obj['text'] must be equal {data['text']}"
                assert json_obj_last["owner"] == data["owner"], f"json_obj['owner'] must be equal {data['owner']}"
                assert json_obj_last["id"] == id
