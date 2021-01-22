import asyncio
import json
import math

import requests

# Create your views here.
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .api_requests import StationStatisticSummary, retrieve_station_statistic
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
        "datatypeid": ["TAVG"],  # ["TAVG", "SNWD", "PRCP"],
        "sortfield": "name",
        "startdate": "2010-01-01",
        "enddate": "2022-01-01",
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
    loop.close()

    return render(
        request,
        "forecast_app/station_statistic.html",
        {
            "avg_temperature": statistic_summary.avg_temperature,
            "avg_temperature_per_year": statistic_summary.avg_temperatures_per_year,
            "max_temp_date_list": statistic_summary.max_temp_date_list,
            "precipitation_info": (
                statistic_summary.total_days_with_precipitation,
                statistic_summary.total_days_without_precipitation,
                statistic_summary.total_days_with_snow,
            ),
        },
    )
