import asyncio
import datetime
import json
import math
from dataclasses import dataclass, field
from typing import Tuple

import aiohttp


@dataclass()
class StationStatisticSummary:
    avg_temperature: float = 0
    avg_temperatures_per_year: list = field(default_factory=lambda: [])
    max_temp_date_list: list = field(default_factory=lambda: [])
    total_days_with_precipitation: int = 0
    total_days_without_precipitation: int = 0
    total_days_with_snow: int = 0
    avg_wind_speed: float = 0


async def retrieve_station_statistic(
    statistic_summary: StationStatisticSummary,
    station_id: str,
    start_date: str,
    end_date: str,
) -> None:
    start_date = datetime.date.fromisoformat(start_date)
    end_date = datetime.date.fromisoformat(end_date)

    annual_statistic_tasks_list = []
    annual_statistic_list = []

    # api has a restriction one year for daily params
    for i in range(start_date.year, end_date.year + 1):
        if end_date.year == start_date.year:
            current_start_date = start_date
            current_end_date = end_date
        elif i == start_date.year:
            current_start_date = start_date
            current_end_date = end_date.replace(year=i, month=12, day=31)
        elif i == end_date.year:
            current_start_date = start_date.replace(year=i, month=1, day=1)
            current_end_date = end_date
        else:
            current_start_date = start_date.replace(year=i, month=1, day=1)
            current_end_date = end_date.replace(year=i, month=12, day=31)

        annual_statistic_summary = StationStatisticSummary()
        annual_statistic_list.append(annual_statistic_summary)
        annual_statistic_tasks_list.append(
            asyncio.create_task(
                get_annual_statistic(
                    annual_statistic_summary,
                    station_id,
                    current_start_date,
                    current_end_date,
                )
            )
        )

    await asyncio.gather(*annual_statistic_tasks_list)

    max_temp_date_list = []
    temperature_samples_cnt = 0
    for item in annual_statistic_list:
        if item.avg_temperature is not None:
            temperature_samples_cnt += 1
            statistic_summary.avg_temperature += item.avg_temperature
            statistic_summary.avg_temperatures_per_year.append(item.avg_temperature)
        if item.max_temp_date_list is not None:
            max_temp_date_list.extend(item.max_temp_date_list)
        if item.total_days_with_precipitation is not None:
            statistic_summary.total_days_with_precipitation += (
                item.total_days_with_precipitation
            )
        if item.total_days_without_precipitation is not None:
            statistic_summary.total_days_without_precipitation += (
                item.total_days_without_precipitation
            )
        if item.total_days_with_snow is not None:
            statistic_summary.total_days_with_snow += item.total_days_with_snow

    if temperature_samples_cnt:
        statistic_summary.avg_temperature /= temperature_samples_cnt

    if max_temp_date_list:
        max_temp_date_list.sort(key=lambda data: data["value"], reverse=True)
        statistic_summary.max_temp_date_list = max_temp_date_list[:3]


async def get_annual_statistic(
    annual_statistic_summary: StationStatisticSummary,
    station_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> None:
    temperature_task = asyncio.create_task(
        temperature_statistic_task(station_id, start_date, end_date)
    )
    await temperature_task
    (
        annual_statistic_summary.avg_temperature,
        annual_statistic_summary.max_temp_date_list,
    ) = temperature_task.result()

    precipitation_task = asyncio.create_task(
        precipitation_statistic_task(station_id, start_date, end_date)
    )
    await precipitation_task
    (
        annual_statistic_summary.total_days_with_precipitation,
        annual_statistic_summary.total_days_without_precipitation,
        annual_statistic_summary.total_days_with_snow,
    ) = precipitation_task.result()


async def precipitation_statistic_task(
    station_id: str, start_date: datetime.date, end_date: datetime.date
) -> Tuple[int, int, int]:
    # params for request
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    params = {
        "datasetid": "GHCND",
        "datatypeid": ["PRCP", "SNWD"],
        "stationid": station_id,
        "units": "metric",
        "startdate": start_date.isoformat(),
        "enddate": end_date.isoformat(),
        "limit": 1,
        "offset": 0,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            params=params,
            headers={"token": "ucyeHcqokRAJiVchQBAyvqGXGIbhOHjx"},
        ) as resp:
            if resp.status != 200:
                raise ConnectionError
            try:
                r_json = await resp.json()
                result_set = r_json["metadata"]["resultset"]
            except json.decoder.JSONDecodeError:
                return None, None, None
            except KeyError:
                return None, None, None

        limit = 1000
        last_page_num = math.ceil(result_set["count"] / limit)

        task_list = []
        for i in range(last_page_num):
            offset = i * limit
            task_list.append(
                asyncio.create_task(
                    retrieve_and_calc_precipitation_params(
                        session,
                        station_id,
                        ["PRCP", "SNWD"],
                        start_date.isoformat(),
                        end_date.isoformat(),
                        str(offset),
                        str(limit),
                    )
                )
            )
        await asyncio.gather(*task_list)

        total_days_with_precipitation = 0
        total_days_without_precipitation = 0
        total_days_with_snow = 0
        for task in task_list:
            tsk_result_with, tsk_result_without, tsk_result_snow = task.result()
            total_days_with_precipitation += tsk_result_with
            total_days_without_precipitation += tsk_result_without
            total_days_with_snow += tsk_result_snow

        return (
            total_days_with_precipitation,
            total_days_without_precipitation,
            total_days_with_snow,
        )


async def retrieve_and_calc_precipitation_params(
    session,
    station_id: str,
    datatypeid: list,
    start_date: str,
    end_date: str,
    offset: str,
    limit: str,
) -> Tuple[int, int, int]:
    # params for request
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    params = {
        "datasetid": "GHCND",
        "datatypeid": datatypeid,
        "units": "metric",
        "stationid": station_id,
        "startdate": start_date,
        "enddate": end_date,
        "limit": limit,
        "offset": offset,
    }

    async with session.get(
        url=url, params=params, headers={"token": "ucyeHcqokRAJiVchQBAyvqGXGIbhOHjx"}
    ) as resp:
        if resp.status != 200:
            raise ConnectionError
        try:
            r_json = await resp.json()
            data_json = r_json["results"]
        except json.decoder.JSONDecodeError:
            return None, None, None
        except KeyError:
            return None, None, None

        total_days_with_precipitation = 0
        total_days_without_precipitation = 0
        total_days_with_snow = 0

        for raw in data_json:
            if raw["datatype"] == "PRCP":
                if raw["value"] > 1.4:
                    total_days_with_precipitation += 1
                else:
                    total_days_without_precipitation += 1
            if (
                raw["datatype"] == "SNWD"
            ):  # this type of data appears when raw["value"] > 0
                total_days_with_snow += 1
    return (
        total_days_with_precipitation,
        total_days_without_precipitation,
        total_days_with_snow,
    )


async def temperature_statistic_task(
    station_id: str, start_date: datetime.date, end_date: datetime.date
) -> Tuple[float, list]:
    # params for request
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    params = {
        "datasetid": "GHCND",
        "datatypeid": "TAVG",
        "units": "metric",
        "stationid": station_id,
        "startdate": start_date.isoformat(),
        "enddate": end_date.isoformat(),
        "limit": 1,
        "offset": 0,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            params=params,
            headers={"token": "ucyeHcqokRAJiVchQBAyvqGXGIbhOHjx"},
        ) as resp:
            if resp.status != 200:
                raise ConnectionError
            try:
                r_json = await resp.json()
                result_set = r_json["metadata"]["resultset"]
            except json.decoder.JSONDecodeError:
                return None, None
            except KeyError:
                return None, None

        limit = 1000
        last_page_num = math.ceil(result_set["count"] / limit)

        retrieve_and_calc_temperature_task_list = []
        for i in range(last_page_num):
            offset = i * limit
            retrieve_and_calc_temperature_task_list.append(
                asyncio.create_task(
                    retrieve_and_calc_temperature_params(
                        session,
                        station_id,
                        "TAVG",
                        start_date.isoformat(),
                        end_date.isoformat(),
                        str(offset),
                        str(limit),
                    )
                )
            )
        await asyncio.gather(*retrieve_and_calc_temperature_task_list)

        avg_value = 0
        max_temp_raw_list = []
        for task in retrieve_and_calc_temperature_task_list:
            temperature, max_temp_raw = task.result()
            avg_value += temperature
            max_temp_raw_list.extend(max_temp_raw)
        avg_value /= last_page_num
        max_temp_raw_list.sort(key=lambda data: data["value"], reverse=True)
        return avg_value, max_temp_raw_list[:3]


async def retrieve_and_calc_temperature_params(
    session,
    station_id: str,
    datatypeid: str,
    start_date: str,
    end_date: str,
    offset: str,
    limit: str,
) -> Tuple[float, list]:
    # params for request
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    params = {
        "datasetid": "GHCND",
        "datatypeid": datatypeid,
        "units": "metric",
        "stationid": station_id,
        "startdate": start_date,
        "enddate": end_date,
        "limit": limit,
        "offset": offset,
    }

    async with session.get(
        url=url, params=params, headers={"token": "ucyeHcqokRAJiVchQBAyvqGXGIbhOHjx"}
    ) as resp:

        if resp.status != 200:
            raise ConnectionError
        try:
            r_json = await resp.json()
            data_json = r_json["results"]
            result_set = r_json["metadata"]["resultset"]
        except json.decoder.JSONDecodeError:
            return None, None
        except KeyError:
            return None, None

        data_json.sort(key=lambda data: data["value"], reverse=True)
        avg_value = sum(raw["value"] for raw in data_json) / result_set["count"]
        max_temp_rows = data_json[:3]

    return avg_value, max_temp_rows
