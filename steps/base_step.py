import json

import allure
from requests import Request, Response, session


class BaseApiSteps:
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
