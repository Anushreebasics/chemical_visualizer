import os
import requests

API_BASE_URL = os.environ.get('CEV_API_BASE_URL', 'http://localhost:8000/api')


class APIClient:
    """Client for API communication."""

    def __init__(self, token=None):
        self.token = token
        self.headers = {'Content-Type': 'application/json'}
        if token:
            self.headers['Authorization'] = f'Token {token}'

    def register(self, username, email, password, first_name='', last_name=''):
        return requests.post(
            f'{API_BASE_URL}/auth/register/',
            json={
                'username': username,
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
            },
            headers=self.headers,
        )

    def login(self, username, password):
        return requests.post(
            f'{API_BASE_URL}/auth/login/',
            json={'username': username, 'password': password},
            headers=self.headers,
        )

    def logout(self):
        return requests.post(f'{API_BASE_URL}/auth/logout/', headers=self.headers)

    def upload_csv(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return requests.post(
                f'{API_BASE_URL}/upload-csv/',
                files=files,
                headers={'Authorization': f'Token {self.token}'},
            )

    def get_summary(self):
        return requests.get(f'{API_BASE_URL}/summary/', headers=self.headers)

    def get_history(self):
        return requests.get(f'{API_BASE_URL}/history/', headers=self.headers)

    def generate_pdf(self, upload_id=None):
        data = {'upload_id': upload_id} if upload_id else {}
        return requests.post(
            f'{API_BASE_URL}/generate-pdf/',
            json=data,
            headers=self.headers,
        )
