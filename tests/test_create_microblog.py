import dataclasses
from dataclasses import asdict

import allure
import pytest
import requests
from assertpy import soft_assertions
from requests import Response

from data.models import CreateMicroblogBody
from data.response_models.microblog import Microblog
from steps.mircoblog import MicroblogApiSteps


@allure.story("Microblog functionality")
class TestCreateMicroblog():
    @pytest.mark.smoke
    @allure.title("Check create microblog positive")
    def test_create_microblog_ok(self):
        data = asdict(CreateMicroblogBody(owner=1))
        api = MicroblogApiSteps()
        r: Response = api.post_microblog(body=data)
        assert r.status_code == 200
        json_obj = r.json()
        assert isinstance(json_obj, dict)
        Microblog(**json_obj)
        with soft_assertions():
            assert json_obj["title"] == data["title"]
            assert json_obj["text"] == data["text"]
            assert json_obj["owner"] == data["owner"]
            # добавить на текущую дату

    @pytest.mark.parametrize("missing_param", ["title", "text", "owner"])
    @allure.title("Check create microblog without mandatory fields")
    def test_create_microblog_without_mandatory_fields(self, missing_param):
        data = dataclasses.asdict(CreateMicroblogBody(owner=1))
        data.pop(missing_param)
        api = MicroblogApiSteps()
        r: Response = api.post_microblog(body=data)
        assert r.status_code == 422
        json_obj = r.json()
        with soft_assertions():
            assert isinstance(json_obj, dict)
            assert "detail" in json_obj
            assert json_obj["detail"][0]["loc"]==["body",missing_param]
            assert json_obj["detail"][0]["msg"] == "field required"
            assert json_obj["detail"][0]["type"] == "value_error.missing"

    @allure.title("Check create microblog with empty body")
    def test_create_microblog_with_empty_body(self):
        data = {}
        api = MicroblogApiSteps()
        r: Response = api.post_microblog(body=data)
        assert r.status_code == 422
        json_obj = r.json()
        assert isinstance(json_obj, dict)
        responce ={
    "detail": [
        {
            "loc": [
                "body",
                "title"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": [
                "body",
                "text"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": [
                "body",
                "owner"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
        assert json_obj == responce

