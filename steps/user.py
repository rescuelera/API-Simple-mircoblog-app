import allure
from requests import Request, Response

from settings import API_HOST
from steps.base_step import BaseApiSteps


class UsersApiSteps(BaseApiSteps):
    _user_endpoint = "/user/"
    _user_by_id_endpoint = "/user/{user_id}"

    @allure.step(f" GET{_user_endpoint}")
    def get_user(self) -> Response:
        req = Request("GET", f"{API_HOST}{self._user_endpoint}")
        return self.send_request(req)

    @allure.step(f" POST{_user_endpoint}")
    def post_user(self, body: dict) -> Response:
        req = Request("POST", f"{API_HOST}{self._user_endpoint}", json=body)
        return self.send_request(req)

    @allure.step(f" GET{_user_by_id_endpoint}")
    def get_user_by_id(self, user_id: int) -> Response:
        req = Request("GET", f"{API_HOST}{self._user_by_id_endpoint.format(user_id=user_id)}")
        return self.send_request(req)

    @allure.step(f" DELETE{_user_by_id_endpoint}")
    def delete_user(self, user_id: int) -> Response:
        req = Request("DELETE", f"{API_HOST}{self._user_by_id_endpoint.format(user_id=user_id)}")
        return self.send_request(req)
