from source.Business.IRequestAgent import *

from requests import *
from json import loads


class RequestAgent(IRequestAgent):
    def read_json(self, url: str) -> Tuple[int, Dict[str, Any]]:
        result = get(url)
        return result.status_code, loads(result.text)

    def read_json_file(
            self,
            url: str,
            token: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        result = None

        if token:
            headers = {'Accept': 'application/json',
                       'Content-Type': 'application_json',
                       'Authorization': f'Bearer {token}'}

            result = get(url, headers=headers)
        else:
            result = get(url)
        return result.status_code, result.json()

    def read_file(self, url: str) -> Tuple[int, bytes]:
        result = get(url)
        return result.status_code, result.content

    def post_and_read_json(
            self,
            url: str,
            headers: Optional[Dict] = None,
            data: Optional[Dict] = None) \
            -> Tuple[int, Dict]:
        result = post(url,
                 headers=headers,
                 data=data)
        return result.status_code, result.json()
