import os
import requests
import json
from rest_framework import serializers


class Service:
    def request(self, file, course_name):
        headers = {'Authorization': f"Bearer {os.environ.get('FASTAPI_TOKEN')}"}
        try:
            request = requests.post(
                f'http://fast-test_api_1:8008/api/python/test/{course_name}/',
                headers=headers,
                files={
                    'file': open(file, 'rb')
                }, timeout=120
            )
            self.status_code = request.status_code
            self.content = json.loads(request.content)
        except requests.exceptions.ConnectionError:
            raise serializers.ValidationError('server not response')
        return request
