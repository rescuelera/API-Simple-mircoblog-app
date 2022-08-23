import json

import allure
from requests import Request, Response, session

from settings import API_HOST


class MicroblogApiSteps:
    _microblog_endpoint = "/microblog/"
    _microblog_by_micropost_id_endpoint = "/microblog/{micropost_id}"

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
