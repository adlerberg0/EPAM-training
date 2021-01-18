import asyncio
import datetime
import json
import math
from dataclasses import dataclass, field

import aiohttp
import requests

# Create your views here.
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import DateRangeForm


def choose_country(request: HttpRequest, page: int = 1) -> HttpResponse:
    limit = 20
    offset = (page - 1) * limit
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations"
    params = {
        "locationcategoryid": "CNTRY",
        "sortfield": "name",
        "limit": limit,
        "offset": offset,
    }
    r = requests.get(
        url=url, params=params, headers={"token": "ucyeHcqokRAJiVchQBAyvqGXGIbhOHjx"}
    )

    try:
        r_json = r.json()
        country_list = r_json["results"]
        result_set = r_json["metadata"]["resultset"]
    except KeyError:
        raise Http404
    except json.decoder.JSONDecodeError:
        raise Http404

    last_page = False
    if result_set["offset"] + result_set["limit"] >= result_set["count"]:
        last_page = True
    last_page_num = math.ceil(result_set["count"] / result_set["limit"])

    context = {
        "country_list": country_list,
        "page": page,
        "first_page": True if page == 1 else False,
        "last_page": last_page,
        "last_page_num": last_page_num,
    }
    return render(request, "forecast_app/index.html", context=context)


def choose_city(request: HttpRequest, country_id: str, page: int = 1) -> HttpResponse:
    limit = 20
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"

    params = {
        "locationid": country_id,
        "sortfield": "name",
        "limit": limit,
        "offset": (page - 1) * limit,
    }
    r = requests.get(
        url=url, params=params, headers={"token": "ucyeHcqokRAJiVchQBAyvqGXGIbhOHjx"}
    )

    try:
        r_json = r.json()
        city_list = r.json()["results"]
        result_set = r_json["metadata"]["resultset"]
    except KeyError:
        raise Http404
    except json.decoder.JSONDecodeError:
        raise Http404

    last_page = False
    if result_set["offset"] + result_set["limit"] >= result_set["count"]:
        last_page = True
    last_page_num = math.ceil(result_set["count"] / result_set["limit"])

    context = {
        "country_id": country_id,
        "city_list": city_list,
        "page": page,
        "first_page": True if page == 1 else False,
        "last_page": last_page,
        "last_page_num": last_page_num,
    }

    return render(request, "forecast_app/cities.html", context=context)


def set_statistic_time_interval(request: HttpRequest, city_id: str) -> HttpResponse:

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = DateRangeForm(
            request.POST, years=list(range(2010, 2022))
        )  # TO DO: I should request year range
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            url = reverse("forecast_app:get_station_statistic", args=[city_id])
            url += f"?startdate={form.cleaned_data['min_date']}&enddate={form.cleaned_data['max_date']}"
            return HttpResponseRedirect(url)

        # if a GET (or any other method) we'll create a blank form
    else:

        form = DateRangeForm(years=list(range(2010, 2022)))

    return render(
        request, "forecast_app/station.html", {"form": form, "city_id": city_id}
    )


@dataclass()
class StationStatisticSummary:
    avg_temperature: float = 0
    avg_temperatures_per_year: list = field(default_factory=lambda: [])
    avg_wind_speed: float = 0


def get_station_statistic(request: HttpRequest, stationid: str) -> HttpResponse:
    startdate = request.GET.get("startdate", "")
    enddate = request.GET.get("enddate", "")
    statistic_summary = StationStatisticSummary()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        retrieve_station_statistic(statistic_summary, stationid, startdate, enddate)
    )
    print(statistic_summary)
    loop.close()

    return render(
        request,
        "forecast_app/station_statistic.html",
        {
            "avg_temperature": statistic_summary.avg_temperature,
            "avg_temperature_per_year": statistic_summary.avg_temperatures_per_year,
        },
    )


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
        if i == start_date.year:
            current_start_date = start_date.replace(year=i)
            current_end_date = end_date.replace(year=i, month=12, day=31)
        if i == end_date.year:
            current_start_date = start_date.replace(year=i, month=1, day=1)
            current_end_date = end_date.replace(year=i)
        else:
            current_start_date = start_date.replace(year=i, month=12, day=31)
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
    for item in annual_statistic_list:
        if item.avg_temperature is not None:
            statistic_summary.avg_temperature += item.avg_temperature
        statistic_summary.avg_temperatures_per_year.append(item.avg_temperature)
        if item.avg_wind_speed is not None:
            statistic_summary.avg_wind_speed += item.avg_wind_speed
    statistic_summary.avg_temperature /= len(annual_statistic_list)
    statistic_summary.avg_wind_speed /= len(annual_statistic_list)


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
    annual_statistic_summary.avg_temperature = temperature_task.result()


#    wind_task = asyncio.create_task(
#            wind_statistic_task(station_id, start_date, end_date)
#    )
#    await wind_task
#    annual_statistic_summary.avg_wind_speed = wind_task.result()

#    precipitation_task = asyncio.create_task(
#        get_annual_statistic(precipitation_statistic_task, station_id, current_start_date, current_end_date)
#    )


async def wind_statistic_task(
    station_id: str, start_date: datetime.date, end_date: datetime.date
) -> float:
    # params for request
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    params = {
        "datasetid": "GHCND",
        "datatypeid": "WSFI",
        "stationid": station_id,
        "startdate": start_date.isoformat(),
        "enddate": end_date.isoformat(),
        "limit": 10,
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
                return None  # TO DO: what to do here?
            except KeyError:
                return None  # TO DO: what to do here?

        limit = 1000
        last_page_num = math.ceil(result_set["count"] / limit)

        task_list = []
        for i in range(last_page_num):
            offset = i * limit
            task_list.append(
                asyncio.create_task(
                    retrieve_and_calc_temperature_params(
                        session,
                        station_id,
                        "WSFI",
                        start_date.isoformat(),
                        end_date.isoformat(),
                        str(offset),
                        str(limit),
                    )
                )
            )
        await asyncio.gather(*task_list)
        avg_value = 0
        for task in task_list:
            avg_value += task.result()
        avg_value /= last_page_num
        return avg_value


async def temperature_statistic_task(
    station_id: str, start_date: datetime.date, end_date: datetime.date
) -> float:

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
                return None  # TO DO: what to do here?
            except KeyError:
                return None  # TO DO: what to do here?

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
        for task in retrieve_and_calc_temperature_task_list:
            avg_value += task.result()
        avg_value /= last_page_num
        return avg_value


async def retrieve_and_calc_temperature_params(
    session,
    station_id: str,
    datatypeid: str,
    start_date: str,
    end_date: str,
    offset: str,
    limit: str,
) -> float:
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
    avg_value = 0
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
            return None  # TO DO: what to do here?
        except KeyError:
            return None  # TO DO: what to do here?
        for raw in data_json:
            avg_value += raw["value"]
        avg_value /= result_set["count"]
    return avg_value
