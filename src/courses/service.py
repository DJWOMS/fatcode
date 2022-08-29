import os, requests


class Service:
    def request(self, file, course_name):
        headers = {'Authorization': f"Bearer {os.environ.get('FASTAPI_TOKEN')}"}
        request = requests.post(
            f'http://fast-test_api_1:8008/api/python/test/{course_name}/',
            headers=headers,
            files={
                'file': open(file, 'rb')
            }, timeout=120
        )
        self.status_code = request.status_code
        self.content = request.content
        return request
