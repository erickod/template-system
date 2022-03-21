from dynaconf import Dynaconf
from fastapi.testclient import TestClient
from template_system.api.app import app_factory

settings = Dynaconf(settings_file=["settings.toml"], environments=True)
client = TestClient(app_factory())
ENDPOINT = f"/{settings.API_VERSION}/templating/"


def test_templating_endpoint_returns_status_400_when_no_template_vars_is_sent():
    response = client.post(ENDPOINT)
    assert response.status_code == 400
