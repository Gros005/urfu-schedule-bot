from src.api_client import UrfuAPIClient

def test_client_initialization():
    client = UrfuAPIClient()
    assert client.base_url == "https://urfu.ru/api/v2"

def test_client_custom_base_url():
    client = UrfuAPIClient(base_url="https://urfu.ru/ru/students/study/schedule/")
    assert client.base_url == "https://urfu.ru/ru/students/study/schedule/"


def test_earch_groups():
    client = UrfuAPIClient()
    data = client.search_groups(name = 'МЕН-333009')
    assert type(data) == int