import allure
from requests import Request, Response

from settings import API_HOST
from steps.base_step import BaseApiSteps


class MicroblogApiSteps(BaseApiSteps):
    _microblog_endpoint = "/microblog/"
    _microblog_by_micropost_id_endpoint = "/microblog/{micropost_id}"

    @allure.step(f" GET{_microblog_endpoint}")
    def get_microblog(self) -> Response:
        req = Request("GET", f"{API_HOST}{self._microblog_endpoint}")
        return self.send_request(req)

    @allure.step(f" POST{_microblog_endpoint}")
    def post_microblog(self, body: dict) -> Response:
        req = Request("POST", f"{API_HOST}{self._microblog_endpoint}", json=body)
        return self.send_request(req)

    @allure.step(f" GET{_microblog_by_micropost_id_endpoint}")
    def get_microblog_by_micropost_id(self, micropost_id: int) -> Response:
        req = Request("GET", f"{API_HOST}{self._microblog_by_micropost_id_endpoint.format(micropost_id=micropost_id)}")
        return self.send_request(req)

    @allure.step(f" DELETE{_microblog_by_micropost_id_endpoint}")
    def delete_microblog(self, micropost_id: int) -> Response:
        req = Request(
            "DELETE", f"{API_HOST}{self._microblog_by_micropost_id_endpoint.format(micropost_id=micropost_id)}"
        )
        return self.send_request(req)
