import json

import allure
from requests import Request, Response, session

from settings import API_HOST


class UsersApiSteps:
    _user_endpoint = "/user/"
    _user_by_id_endpoint = "/user/{user_id}"

    def send_request(self, req: Request) -> Response:
        with allure.step(f"Request {req.method}: {req.url}"):
            allure.attach(json.dumps(req.headers, indent=4), "headers")

        prepared_req = session().prepare_request(req)
        r: Response = session().send(prepared_req)
        with allure.step(f"Response: {r.status_code}"):
            allure.attach(json.dumps(dict(r.headers), indent=4), "headers")
            if r.content:
                if r.json():
                    allure.attach(json.dumps(r.json(), indent=4), "body")
        return r

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
