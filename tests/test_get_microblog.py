import dataclasses

import allure
import pytest
import requests
from assertpy import soft_assertions
from requests import Response

from data.models import CreateMicroblogBody
from data.response_models.microblog import Microblog
from steps.mircoblog import MicroblogApiSteps


@allure.story("Microblog functionality")
class TestGetMicroblog():
    @pytest.mark.smoke
    @allure.title("Check get microblog positive")
    def test_get_microblog_ok(self):
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
            id = json_obj["id"]
            # добавить на текущую дату

        with allure.step("get microblog"):
            api = MicroblogApiSteps()
            r: Response = api.get_microblog()
            assert r.status_code == 200
            json_obj = r.json()
            json_obj_last = json_obj[- 1]
            Microblog(**json_obj_last)

            with soft_assertions():
                assert isinstance(json_obj, list)
                assert json_obj_last["title"] == data["title"]
                assert json_obj_last["text"] == data["text"]
                assert json_obj_last["owner"] == data["owner"]
                assert json_obj_last["id"] == id
            # добавить на текущую дату

