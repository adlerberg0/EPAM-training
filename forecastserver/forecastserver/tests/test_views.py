from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from requests import Response
from selenium.webdriver.firefox.webdriver import WebDriver

from .response_test_context_data import context_cities_dict, context_countries_dict


def mocked_countries_view_requests_get(*args, **kwargs):
    response = Response()
    with open("forecastserver/tests/response_countries.json", "r") as fi:
        response._content = fi.read().encode()
    response.status_code = 200

    return response


def mocked_city_view_requests_get(*args, **kwargs):
    response = Response()
    with open("forecastserver/tests/response_cities.json", "r") as fi:
        response._content = fi.read().encode()
    response.status_code = 200

    return response


class IndexViewTest(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_start_button_click(self):
        self.selenium.get("%s%s" % (self.live_server_url, ""))
        self.selenium.find_element_by_id("start").click()
        self.assertIn(reverse("forecast_app:country"), self.selenium.current_url)


class CountriesViewTest(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @mock.patch("requests.get", side_effect=mocked_countries_view_requests_get)
    def test_view_url_exists_at_desired_location(self, *args):
        response = self.client.get("/forecast/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.get", side_effect=mocked_countries_view_requests_get)
    def test_view_url_accessible_by_name(self, *args):
        response = self.client.get(reverse("forecast_app:country"))
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.get", side_effect=mocked_countries_view_requests_get)
    def test_view_uses_correct_template(self, *args):
        response = self.client.get(reverse("forecast_app:country"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forecast_app/index.html")

    @mock.patch("requests.get", side_effect=mocked_countries_view_requests_get)
    def test_processing_result_of_requesting_countries_from_api(self, *args):
        response = self.client.get(reverse("forecast_app:country"))

        self.assertEqual(
            response.context["country_list"], context_countries_dict["country_list"]
        )

    @mock.patch("requests.get", side_effect=mocked_countries_view_requests_get)
    def test_pagination_buttons(self, *args):
        self.selenium.get(
            "%s%s" % (self.live_server_url, reverse("forecast_app:country"))
        )

        self.selenium.find_element_by_id("go_ahead").click()
        self.assertIn(
            reverse("forecast_app:country", args=[2]), self.selenium.current_url
        )

        self.selenium.find_element_by_id("go_back").click()
        self.assertIn(
            reverse("forecast_app:country", args=[1]), self.selenium.current_url
        )

    @mock.patch("requests.get", side_effect=mocked_countries_view_requests_get)
    def test_redirection_to_cities_page(self, *args):
        self.selenium.get(
            "%s%s" % (self.live_server_url, reverse("forecast_app:country"))
        )

        self.selenium.find_element_by_xpath(
            "//div[@class='list-group justify-content-center']/a"
        ).click()
        self.assertIn(
            reverse("forecast_app:city", args=["FIPS:AF"]), self.selenium.current_url
        )


class CitiesViewTest(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @mock.patch("requests.get", side_effect=mocked_city_view_requests_get)
    def test_view_url_exists_at_desired_location(self, *args):
        response = self.client.get("/forecast/city/FIPS:BO")
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.get", side_effect=mocked_city_view_requests_get)
    def test_view_url_accessible_by_name(self, *args):
        response = self.client.get(reverse("forecast_app:city", args=["FIPS:BO"]))
        self.assertEqual(response.status_code, 200)

    @mock.patch("requests.get", side_effect=mocked_city_view_requests_get)
    def test_view_uses_correct_template(self, *args):
        response = self.client.get(reverse("forecast_app:city", args=["FIPS:BO"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forecast_app/cities.html")

    @mock.patch("requests.get", side_effect=mocked_city_view_requests_get)
    def test_processing_result_of_requesting_countries_from_api(self, *args):
        response = self.client.get(reverse("forecast_app:city", args=["FIPS:BO"]))

        self.assertEqual(
            response.context["city_list"], context_cities_dict["city_list"]
        )
        self.assertEqual(
            response.context["country_id"], context_cities_dict["country_id"]
        )
        self.assertEqual(response.context["page"], context_cities_dict["page"])
        self.assertEqual(
            response.context["first_page"], context_cities_dict["first_page"]
        )
        self.assertEqual(
            response.context["last_page_num"], context_cities_dict["last_page_num"]
        )

    @mock.patch("requests.get", side_effect=mocked_city_view_requests_get)
    def test_pagination_buttons(self, *args):
        self.selenium.get(
            "%s%s"
            % (self.live_server_url, reverse("forecast_app:city", args=["FIPS:BO"]))
        )

        self.selenium.find_element_by_id("go_ahead").click()
        self.assertIn(
            reverse("forecast_app:city", args=["FIPS:BO", 2]), self.selenium.current_url
        )

        self.selenium.find_element_by_id("go_back").click()
        self.assertIn(
            reverse("forecast_app:city", args=["FIPS:BO", 1]), self.selenium.current_url
        )

    @mock.patch("requests.get", side_effect=mocked_city_view_requests_get)
    def test_redirection_to_set_time_interval_page(self, *args):
        self.selenium.get(
            "%s%s"
            % (self.live_server_url, reverse("forecast_app:city", args=["FIPS:BO"]))
        )

        self.selenium.find_element_by_xpath(
            "//div[@class='list-group justify-content-center']/a"
        ).click()
        self.assertIn(
            reverse(
                "forecast_app:set_statistic_time_interval", args=["GHCND:BOM00026941"]
            ),
            self.selenium.current_url,
        )  # TO DO: why 'forecast_app:city'?? should be statistic_time_interval/


class SetStatisticTimeIntervalViewTest(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(
            "/forecast/statistic_time_interval/GHCND:BOM00026941"
        )
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse(
                "forecast_app:set_statistic_time_interval", args=["GHCND:BOM00026941"]
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse(
                "forecast_app:set_statistic_time_interval", args=["GHCND:BOM00026941"]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forecast_app/station.html")

    def test_redirection_to_set_time_interval_page(self):
        response = self.client.post(
            reverse(
                "forecast_app:set_statistic_time_interval", args=["GHCND:BOM00026941"]
            ),
            {
                "min_date_month": "1",
                "min_date_day": "1",
                "min_date_year": "2010",
                "max_date_month": "1",
                "max_date_day": "1",
                "max_date_year": "2010",
            },
        )

        self.assertRedirects(
            response,
            reverse("forecast_app:get_station_statistic", args=["GHCND:BOM00026941"])
            + "?startdate=2010-01-01&enddate=2010-01-01",
        )
