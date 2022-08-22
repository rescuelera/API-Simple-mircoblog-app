import allure
import requests
from requests import Response, get

from settings import API_HOST


class UsersApiSteps:
    _user_endpoint = "/user/"
    _user_by_id_endpoint = "/user/{user_id}"

    @allure.step(f" GET{_user_endpoint}")
    def get_user(self) ->Response:
        r: Response = get(f"{API_HOST}{self._user_endpoint}")
        return r

    @allure.step(f" POST{_user_endpoint}")
    def post_user(self, body: dict) ->Response:
        r: Response = requests.post(f"{API_HOST}{self._user_endpoint}", json=body)
        return r

    @allure.step(f" GET{_user_by_id_endpoint}")
    def get_user_by_id(self, user_id: int) -> Response:
        r: Response = requests.get(f"{API_HOST}{self._user_by_id_endpoint.format(user_id=user_id)}")
        return r

    @allure.step(f" DELETE{_user_by_id_endpoint}")
    def delete_user(self, user_id: int) -> Response:
        pass