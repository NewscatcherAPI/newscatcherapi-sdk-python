from requests.auth import AuthBase


class NewsCatcherApiAuth(AuthBase):
    # Provided by NewsCatcher: https://docs.newscatcherapi.com/api-docs/authentication
    def __init__(self, x_api_key):
        self.x_api_key = x_api_key

    def __call__(self, request):
        request.headers.update(get_auth_headers(self.x_api_key))
        return request


def get_auth_headers(x_api_key):
    return {"Content-Type": "Application/JSON", "x-api-key": x_api_key}
