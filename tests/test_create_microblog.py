import dataclasses
from dataclasses import asdict

import allure
import pytest
from assertpy import soft_assertions
from requests import Response

from data.models import CreateMicroblogBody
from data.response_models.microblog import Microblog


@allure.story("Microblog functionality")
class TestCreateMicroblog:
    @pytest.mark.smoke
    @allure.title("Check create microblog positive")
    def test_create_microblog_ok(self, microblog_api):
        data = asdict(CreateMicroblogBody(owner=1))
        r: Response = microblog_api.post_microblog(body=data)
        assert r.status_code == 200, "Status code must be 200"
        json_obj = r.json()
        assert isinstance(json_obj, dict), "json_obj must be dict"
        Microblog(**json_obj)
        with soft_assertions():
            assert json_obj["title"] == data["title"], f"json_obj['title'] must be equal {data['title']}"
            assert json_obj["text"] == data["text"], f"json_obj['text'] must be equal {data['text']}"
            assert json_obj["owner"] == data["owner"], f"json_obj['owner'] must be equal {data['owner']}"

    @pytest.mark.parametrize("missing_param", ["title", "text", "owner"])
    @allure.title("Check create microblog without mandatory fields")
    def test_create_microblog_without_mandatory_fields(self, missing_param, microblog_api):
        data = dataclasses.asdict(CreateMicroblogBody(owner=1))
        data.pop(missing_param)
        r: Response = microblog_api.post_microblog(body=data)
        assert r.status_code == 422, "Status code must be 422"
        json_obj = r.json()
        with soft_assertions():
            assert isinstance(json_obj, dict), "json_obj must be dict"
            assert "detail" in json_obj
            assert json_obj["detail"][0]["loc"] == [
                "body",
                missing_param,
            ], f"json_obj['detail'][0]['loc'] must be equal 'body', {missing_param}"
            assert (
                json_obj["detail"][0]["msg"] == "field required"
            ), "json_obj['detail'][0]['msg'] must be equal 'field required'"
            assert (
                json_obj["detail"][0]["type"] == "value_error.missing"
            ), "json_obj['detail'][0]['type'] must be equal 'value_error.missing'"

    @allure.title("Check create microblog with empty body")
    def test_create_microblog_with_empty_body(self, microblog_api):
        r: Response = microblog_api.post_microblog(body={})
        assert r.status_code == 422, "Status code must be 422"
        json_obj = r.json()
        assert isinstance(json_obj, dict), "json_obj must be dict"
        response = {
            "detail": [
                {"loc": ["body", "title"], "msg": "field required", "type": "value_error.missing"},
                {"loc": ["body", "text"], "msg": "field required", "type": "value_error.missing"},
                {"loc": ["body", "owner"], "msg": "field required", "type": "value_error.missing"},
            ]
        }
        assert json_obj == response, f"json_obj must be equal {response}"
