import allure
import requests
from requests import Response, get

from settings import API_HOST


class MicroblogApiSteps:
    _microblog_endpoint = "/microblog/"
    _microblog_by_micropost_id_endpoint = "/microblog/{micropost_id}"

    @allure.step(f" GET{_microblog_endpoint}")
    def get_microblog(self) -> Response:
        r: Response = get(f"{API_HOST}{self._microblog_endpoint}")
        return r

    @allure.step(f" POST{_microblog_endpoint}")
    def post_microblog(self, body: dict) -> Response:
        r: Response = requests.post(f"{API_HOST}{self._microblog_endpoint}", json=body)
        return r

    @allure.step(f" GET{_microblog_by_micropost_id_endpoint}")
    def get_microblog_by_micropost_id(self, micropost_id: int) -> Response:
        r: Response = requests.get(
            f"{API_HOST}{self._microblog_by_micropost_id_endpoint.format(micropost_id=micropost_id)}"
        )
        return r

    @allure.step(f" DELETE{_microblog_by_micropost_id_endpoint}")
    def delete_microblog(self, micropost_id: int) -> Response:
        pass
