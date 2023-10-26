import private_config
import requests


class AiDevsRestapiHelper:
    """Encapsulate details about calling API, authorization and others."""
    def __init__(self, task_name):
        """Get authorization token."""
        self.task_name = task_name
        js = {'apikey': private_config.API_KEY_SERVICE}
        response = requests.post(private_config.TOKEN_URL + task_name, json=js)
        assert response.status_code < 300, {'HTTP code': response.status_code, 'JSON': response.json()}
        self._authorization_token = response.json()['token']

    def __enter__(self):
        """Init the class to use with 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit function for with statement."""
        pass

    def get_task(self):
        """Get task details."""
        response = requests.get(private_config.TASK_URL + self._authorization_token)
        assert response.status_code < 300, {'HTTP code': response.status_code, 'JSON': response.json()}
        print(response.json())
        return response.json()

    def submit_answer(self, answer):
        """Submit answer."""
        js = {'answer': answer}
        response = requests.post(private_config.ANSWER_URL + self._authorization_token, json=js)
        assert response.status_code < 300, {'HTTP code': response.status_code, 'JSON': response.json()}
        print(response.json())
        return response.json()
