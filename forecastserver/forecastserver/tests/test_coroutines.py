import asyncio
import datetime
from typing import Tuple
from unittest import mock

import aiohttp
from aioresponses import aioresponses
from django.test import TestCase
from forecast_app.api_requests import (
    StationStatisticSummary,
    get_annual_statistic,
    precipitation_statistic_task,
    retrieve_and_calc_precipitation_params,
    retrieve_and_calc_temperature_params,
    retrieve_station_statistic,
    temperature_statistic_task,
)


async def mocked_retrieve_and_calc_temperature_params(
    session,
    station_id: str,
    datatypeid: str,
    start_date: str,
    end_date: str,
    offset: str,
    limit: str,
) -> Tuple[float, list]:
    return -7.666666666666667, [
        {
            "date": "2010-01-02T00:00:00",
            "datatype": "TAVG",
            "station": "GHCND:BOM00026941",
            "attributes": "H,,S,",
            "value": -5.6,
        },
        {
            "date": "2010-01-01T00:00:00",
            "datatype": "TAVG",
            "station": "GHCND:BOM00026941",
            "attributes": "H,,S,",
            "value": -5.9,
        },
        {
            "date": "2010-01-03T00:00:00",
            "datatype": "TAVG",
            "station": "GHCND:BOM00026941",
            "attributes": "H,,S,",
            "value": -11.5,
        },
    ]


async def mocked_retrieve_and_calc_precipitation_params(
    session,
    station_id: str,
    datatypeid: str,
    start_date: str,
    end_date: str,
    offset: str,
    limit: str,
) -> Tuple[int, int, int]:
    return 2, 0, 2


async def mocked_temperature_statistic_task(
    station_id: str, start_date: datetime.date, end_date: datetime.date
) -> Tuple[float, list]:
    return -7.666666666666667, [
        {
            "date": "2010-01-02T00:00:00",
            "datatype": "TAVG",
            "station": "GHCND:BOM00026941",
            "attributes": "H,,S,",
            "value": -5.6,
        },
        {
            "date": "2010-01-01T00:00:00",
            "datatype": "TAVG",
            "station": "GHCND:BOM00026941",
            "attributes": "H,,S,",
            "value": -5.9,
        },
        {
            "date": "2010-01-03T00:00:00",
            "datatype": "TAVG",
            "station": "GHCND:BOM00026941",
            "attributes": "H,,S,",
            "value": -11.5,
        },
    ]


async def mocked_precipitation_statistic_task(
    station_id: str, start_date: datetime.date, end_date: datetime.date
) -> Tuple[int, int, int]:
    return 2, 0, 2


async def mocked_get_annual_statistic(
    annual_statistic_summary: StationStatisticSummary,
    station_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
):
    return StationStatisticSummary(
        avg_temperature=-7.666666666666667,
        avg_temperatures_per_year=[],
        max_temp_date_list=[
            {
                "date": "2010-01-02T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.6,
            },
            {
                "date": "2010-01-01T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.9,
            },
            {
                "date": "2010-01-03T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -11.5,
            },
        ],
        total_days_with_precipitation=2,
        total_days_without_precipitation=0,
        total_days_with_snow=2,
        avg_wind_speed=0,
    )


async def mocked_get_station_statistic(
    annual_statistic_summary: StationStatisticSummary,
    station_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
):
    return StationStatisticSummary(
        avg_temperature=-7.666666666666667,
        avg_temperatures_per_year=[],
        max_temp_date_list=[
            {
                "date": "2010-01-02T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.6,
            },
            {
                "date": "2010-01-01T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.9,
            },
            {
                "date": "2010-01-03T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -11.5,
            },
        ],
        total_days_with_precipitation=2,
        total_days_without_precipitation=0,
        total_days_with_snow=2,
        avg_wind_speed=0,
    )


class MyAppTestCase(TestCase):
    @aioresponses()
    def test_retrieve_and_calc_temperature_params(self, mocked):
        loop = asyncio.get_event_loop()
        text = {
            "metadata": {"resultset": {"offset": 1, "count": 3, "limit": 1000}},
            "results": [
                {
                    "date": "2010-01-01T00:00:00",
                    "datatype": "TAVG",
                    "station": "GHCND:BOM00026941",
                    "attributes": "H,,S,",
                    "value": -5.9,
                },
                {
                    "date": "2010-01-02T00:00:00",
                    "datatype": "TAVG",
                    "station": "GHCND:BOM00026941",
                    "attributes": "H,,S,",
                    "value": -5.6,
                },
                {
                    "date": "2010-01-03T00:00:00",
                    "datatype": "TAVG",
                    "station": "GHCND:BOM00026941",
                    "attributes": "H,,S,",
                    "value": -11.5,
                },
            ],
        }
        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&enddate=2010-01-03&limit=1&offset=1000&startdate=2010-01-01&stationid=GHCND%253ABOM00026941&units=metric"
        mocked.get(url, status=200, payload=text)
        session = aiohttp.ClientSession()
        result = loop.run_until_complete(
            retrieve_and_calc_temperature_params(
                session,
                "GHCND:BOM00026941",
                "TAVG",
                "2010-01-01",
                "2010-01-03",
                "1000",
                "1",
            )
        )

        expected_result = -7.666666666666667, [
            {
                "date": "2010-01-02T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.6,
            },
            {
                "date": "2010-01-01T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.9,
            },
            {
                "date": "2010-01-03T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -11.5,
            },
        ]

        self.assertEqual(result, expected_result)

    @aioresponses()
    @mock.patch(
        "forecast_app.api_requests.retrieve_and_calc_temperature_params",
        side_effect=mocked_retrieve_and_calc_temperature_params,
    )
    def test_temperature_statistic_task(self, mocked, *args):
        loop = asyncio.get_event_loop()
        text = {
            "metadata": {"resultset": {"offset": 1, "count": 3, "limit": 1}},
            "results": [
                {
                    "date": "2010-01-01T00:00:00",
                    "datatype": "TAVG",
                    "station": "GHCND:BOM00026941",
                    "attributes": "H,,S,",
                    "value": -5.9,
                }
            ],
        }

        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&enddate=2010-01-03&limit=1&offset=0&startdate=2010-01-01&stationid=GHCND%253ABOM00026941&units=metric"
        mocked.get(url, status=200, payload=text)
        result = loop.run_until_complete(
            temperature_statistic_task(
                "GHCND:BOM00026941",
                datetime.date.fromisoformat("2010-01-01"),
                datetime.date.fromisoformat("2010-01-03"),
            )
        )

        expected_result = -7.666666666666667, [
            {
                "date": "2010-01-02T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.6,
            },
            {
                "date": "2010-01-01T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -5.9,
            },
            {
                "date": "2010-01-03T00:00:00",
                "datatype": "TAVG",
                "station": "GHCND:BOM00026941",
                "attributes": "H,,S,",
                "value": -11.5,
            },
        ]

        self.assertEqual(result, expected_result)

    @aioresponses()
    def test_retrieve_and_calc_precipitation_params(self, mocked):
        loop = asyncio.get_event_loop()
        text = {
            "metadata": {"resultset": {"offset": 1, "count": 4, "limit": 1000}},
            "results": [
                {
                    "date": "2021-01-03T00:00:00",
                    "datatype": "PRCP",
                    "station": "GHCND:BOM00026850",
                    "attributes": "B,,S,",
                    "value": 3.8,
                },
                {
                    "date": "2021-01-03T00:00:00",
                    "datatype": "SNWD",
                    "station": "GHCND:BOM00026850",
                    "attributes": ",,S,",
                    "value": 30.0,
                },
                {
                    "date": "2021-01-04T00:00:00",
                    "datatype": "PRCP",
                    "station": "GHCND:BOM00026850",
                    "attributes": "B,,S,",
                    "value": 2.3,
                },
                {
                    "date": "2021-01-04T00:00:00",
                    "datatype": "SNWD",
                    "station": "GHCND:BOM00026850",
                    "attributes": ",,S,",
                    "value": 41.0,
                },
            ],
        }
        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=PRCP&datatypeid=SNWD&enddate=2010-01-04&limit=0&offset=1000&startdate=2010-01-03&stationid=GHCND%253ABOM00026850&units=metric"
        mocked.get(url, status=200, payload=text)
        session = aiohttp.ClientSession()
        result = loop.run_until_complete(
            retrieve_and_calc_precipitation_params(
                session,
                "GHCND:BOM00026850",
                ["PRCP", "SNWD"],
                "2010-01-03",
                "2010-01-04",
                "1000",
                "0",
            )
        )

        expected_result = 2, 0, 2

        self.assertEqual(result, expected_result)

    @aioresponses()
    @mock.patch(
        "forecast_app.api_requests.retrieve_and_calc_precipitation_params",
        side_effect=mocked_retrieve_and_calc_precipitation_params,
    )
    def test_precipitation_statistic_task(self, mocked, *args):
        loop = asyncio.get_event_loop()
        text = {
            "metadata": {"resultset": {"offset": 1, "count": 4, "limit": 1}},
            "results": [
                {
                    "date": "2021-01-03T00:00:00",
                    "datatype": "PRCP",
                    "station": "GHCND:BOM00026850",
                    "attributes": "B,,S,",
                    "value": 3.8,
                }
            ],
        }

        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=PRCP&datatypeid=SNWD&enddate=2010-01-04&limit=1&offset=0&startdate=2010-01-03&stationid=GHCND%253ABOM00026850&units=metric"
        mocked.get(url, status=200, payload=text)
        result = loop.run_until_complete(
            precipitation_statistic_task(
                "GHCND:BOM00026850",
                datetime.date.fromisoformat("2010-01-03"),
                datetime.date.fromisoformat("2010-01-04"),
            )
        )

        expected_result = 2, 0, 2

        self.assertEqual(result, expected_result)

    @mock.patch(
        "forecast_app.api_requests.temperature_statistic_task",
        side_effect=mocked_temperature_statistic_task,
    )
    @mock.patch(
        "forecast_app.api_requests.precipitation_statistic_task",
        side_effect=mocked_precipitation_statistic_task,
    )
    def test_get_annual_statistic(self, *args):
        loop = asyncio.get_event_loop()
        statistic_summary = StationStatisticSummary()
        loop.run_until_complete(
            get_annual_statistic(
                statistic_summary,
                "GHCND:BOM00026850",
                datetime.date.fromisoformat("2010-01-03"),
                datetime.date.fromisoformat("2010-01-04"),
            )
        )

        expected_value = StationStatisticSummary(
            avg_temperature=-7.666666666666667,
            avg_temperatures_per_year=[],
            max_temp_date_list=[
                {
                    "date": "2010-01-02T00:00:00",
                    "datatype": "TAVG",
                    "station": "GHCND:BOM00026941",
                    "attributes": "H,,S,",
                    "value": -5.6,
                },
                {
                    "date": "2010-01-01T00:00:00",
                    "datatype": "TAVG",
                    "station": "GHCND:BOM00026941",
                    "attributes": "H,,S,",
                    "value": -5.9,
                },
                {
                    "date": "2010-01-03T00:00:00",
                    "datatype": "TAVG",
                    "station": "GHCND:BOM00026941",
                    "attributes": "H,,S,",
                    "value": -11.5,
                },
            ],
            total_days_with_precipitation=2,
            total_days_without_precipitation=0,
            total_days_with_snow=2,
            avg_wind_speed=0,
        )

        self.assertEqual(statistic_summary, expected_value)

        @mock.patch(
            "forecast_app.api_requests.get_annual_statistic",
            side_effect=mocked_get_annual_statistic,
        )
        def test_retrieve_station_statistic(self, mocked, *args):
            loop = asyncio.get_event_loop()
            statistic_summary = StationStatisticSummary()
            loop.run_until_complete(
                retrieve_station_statistic(
                    statistic_summary,
                    "GHCND:BOM00026850",
                    datetime.date.fromisoformat("2010-01-03"),
                    datetime.date.fromisoformat("2010-01-04"),
                )
            )

            expected_value = StationStatisticSummary(
                avg_temperature=-7.666666666666667,
                avg_temperatures_per_year=[],
                max_temp_date_list=[
                    {
                        "date": "2010-01-02T00:00:00",
                        "datatype": "TAVG",
                        "station": "GHCND:BOM00026941",
                        "attributes": "H,,S,",
                        "value": -5.6,
                    },
                    {
                        "date": "2010-01-01T00:00:00",
                        "datatype": "TAVG",
                        "station": "GHCND:BOM00026941",
                        "attributes": "H,,S,",
                        "value": -5.9,
                    },
                    {
                        "date": "2010-01-03T00:00:00",
                        "datatype": "TAVG",
                        "station": "GHCND:BOM00026941",
                        "attributes": "H,,S,",
                        "value": -11.5,
                    },
                ],
                total_days_with_precipitation=2,
                total_days_without_precipitation=0,
                total_days_with_snow=2,
                avg_wind_speed=0,
            )

            self.assertEqual(statistic_summary, expected_value)
