import pytest
from unittest.mock import patch

from app.enduhub_fetcher import EnduhubFetcher
from app.enduhub_result_sender import EnduhubResultSender
from app.birth_year import BirthYear


def test_enduhub_fetcher_object_init():
    """EnduhubFetcher  initalization test"""
    endu = EnduhubFetcher("Michal Mojek", 1980)
    assert isinstance(endu, EnduhubFetcher)


def test_enduhub_fetcher_string():
    """Test String representatation of EnduhubFetcher object"""
    endu = EnduhubFetcher("Michal Mojek", 1980)
    assert str(endu) == "Michal Mojek, 1980"


@patch("app.enduhub_fetcher.EnduhubFetcher.download_page")
def test_enduhub_fetcher_number_of_pages_without_pagination_div(
    mock_downloaded_page, html_with_results
):
    """Tests the extraction of the number of pages to download"""
    mock_downloaded_page.return_value = ""
    endu = EnduhubFetcher("Paweł Wójcik", 1976)
    assert endu.number_of_pages == 0
    endu.prepare_web_links()
    assert endu.number_of_pages == 1


@patch("app.enduhub_fetcher.EnduhubFetcher.download_page")
def test_enduhub_fetcher_number_of_pages_founder(
    mock_downloaded_page, html_with_results
):
    """Tests the extraction of the number of pages to download"""
    mock_downloaded_page.return_value = html_with_results
    endu = EnduhubFetcher("Paweł Wójcik", 1976)
    assert endu.number_of_pages == 0
    endu.prepare_web_links()
    assert len(endu.pages_content) == 1
    assert endu.number_of_pages == 7


@patch("app.enduhub_fetcher.EnduhubFetcher.download_page")
def test_enduhub_fetcher_fetch_results(
    mock_downloaded_page, html_with_results
):
    """Tests the extraction of race_results"""
    mock_downloaded_page.return_value = html_with_results
    endu = EnduhubFetcher("Paweł Wójcik", 1976)
    endu.prepare_web_links()
    results = endu.fetch_results()
    first_results_on_list = results[0]
    assert first_results_on_list["race_date"] == "2019-04-28"
    assert first_results_on_list["race_type"] == "Bieganie"


def test_endhub_result_sender_init(dict_results):
    enduhub = EnduhubResultSender(dict_results)
    assert isinstance(enduhub, EnduhubResultSender)


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if "get_or_create" in args[0]:
        return MockResponse({"id": "1"}, 200)

    if "race_results" in args[0]:
        return MockResponse({"id": "1"}, 200)


@patch(
    "app.enduhub_result_sender.requests.post", side_effect=mocked_requests_post
)
def test_endhub_result_sender_send_data(mocker, dict_results):
    enduhub = EnduhubResultSender(dict_results)
    res = enduhub.send_data()
    assert res.status_code == 200


def test_birth_year_init():
    birth = BirthYear(1980)
    assert str(birth) == "1980"
    assert birth.year == 1980


def test_birth_year_init_short():
    birth = BirthYear(80)
    assert str(birth) == "1980"
    assert birth.year == 1980


def test_birth_year_non_numerical():
    with pytest.raises(ValueError):
        BirthYear("asd")

