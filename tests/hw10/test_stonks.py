import os
from pathlib import Path
from typing import Any

import pandas as pd
from aiohttp import web
from bs4 import BeautifulSoup

from hw10.stonks import CompanyInfo  # noqa
from hw10.stonks import get_dollar_course_value  # noqa;
from hw10.stonks import parse_company_page_info  # noqa;
from hw10.stonks import parse_information_from_one_page  # noqa;
from hw10.stonks import retrieve_main_page_company_info  # noqa;
from hw10.stonks import write_result_to_json  # noqa

verified_company_list = [
    CompanyInfo(
        name="YUM! Brands",
        code="",
        P_E=0,
        price=0,
        url="/stocks/yum-stock",
        year_growth=-2.35,
        max_income=0,
    ),
    CompanyInfo(
        name="Zimmer Biomet",
        code="",
        P_E=0,
        price=0,
        url="/stocks/zbh-stock",
        year_growth=-13.0,
        max_income=0,
    ),
    CompanyInfo(
        name="Zions Bancorporation",
        code="",
        P_E=0,
        price=0,
        url="/stocks/zion-stock",
        year_growth=-12.8,
        max_income=0,
    ),
    CompanyInfo(
        name="Zoeti a",
        code="",
        P_E=0,
        price=0,
        url="/stocks/zts-stock",
        year_growth=12.42,
        max_income=0,
    ),
]


async def test_retrieve_main_page_company_info():
    with open("mainpage_company_info.html") as fi:
        raw = fi.read()
    soup = BeautifulSoup(raw, "lxml")
    company = CompanyInfo()
    retrieve_main_page_company_info(company, soup)
    assert company == CompanyInfo(
        name="YUM! Brands", url="/stocks/yum-stock", year_growth=-1.33
    )


async def test_parse_company_page_info(aiohttp_raw_server: Any, aiohttp_client):
    with open("test_parse_company_page_info.html") as fi:
        soup = BeautifulSoup(fi, "lxml")

    async def async_response(request):
        return web.Response(text=str(soup))

    company = CompanyInfo(name="YUM! Brands", url="", year_growth=-1.33)
    base_url = "/"
    dollar_course = 75.4571

    app = await aiohttp_raw_server(async_response)
    client = await aiohttp_client(app)

    await parse_company_page_info(company, client, base_url, dollar_course)

    assert company == CompanyInfo(
        name="YUM! Brands",
        code="YUM",
        P_E=28.75,
        price=8058.063709,
        url="",
        year_growth=-1.33,
        max_income=1.0045487627365357,
    )


async def test_get_dollar_course_value():
    with open("test_get_dollar_course_value.xml") as fi:
        assert await get_dollar_course_value(fi.read()) == 30.9436


async def test_parse_information_from_one_page(aiohttp_raw_server, aiohttp_client):
    with open("test_parse_information_from_one_page.html") as fi:
        soup = BeautifulSoup(fi, "lxml")

    async def async_response(request):
        return web.Response(text=str(soup))

    app = await aiohttp_raw_server(async_response)
    client = await aiohttp_client(app)

    base_url = "/"
    addition = ""
    page_param = {"p": 11}
    dollar_course = 75.4571
    company_list = []
    task_list = []
    await parse_information_from_one_page(
        client, base_url, addition, company_list, task_list, dollar_course, page_param
    )
    assert company_list == verified_company_list


def test_write_results_to_json(event_loop, tmp_path):
    os.chdir(tmp_path)
    company_list = [
        CompanyInfo(
            name="YUM! Brands",
            code="YUM",
            P_E=28.75,
            price=8058.063709,
            url="/stocks/yum-stock",
            year_growth=-1.33,
            max_income=1.0045487627365357,
        ),
        CompanyInfo(
            name="Zimmer Biomet",
            code="ZBH",
            P_E=19.1,
            price=11241.598757999998,
            url="/stocks/zbh-stock",
            year_growth=-14.0,
            max_income=1.1793734032540002,
        ),
        CompanyInfo(
            name="Zions Bancorporation",
            code="ZION",
            P_E=12.38,
            price=3283.1384209999997,
            url="/stocks/zion-stock",
            year_growth=-12.8,
            max_income=1.2251908396946567,
        ),
        CompanyInfo(
            name="Zoeti a",
            code="ZTS",
            P_E=36.49,
            price=12061.817434999999,
            url="/stocks/zts-stock",
            year_growth=12.42,
            max_income=0.9567627494456762,
        ),
    ]

    test_dir = Path(__file__).parent
    event_loop.run_until_complete(write_result_to_json(company_list))
    pd.testing.assert_frame_equal(
        pd.read_json("company_by_price.json", orient="records"),
        pd.read_json(test_dir / "verified_company_by_price.json", orient="records"),
    )
    pd.testing.assert_frame_equal(
        pd.read_json("company_by_year_growth.json", orient="records"),
        pd.read_json(
            test_dir / "verified_company_by_year_growth.json", orient="records"
        ),
    )
    pd.testing.assert_frame_equal(
        pd.read_json("company_by_max_income.json", orient="records"),
        pd.read_json(
            test_dir / "verified_company_by_max_income.json", orient="records"
        ),
    )
    pd.testing.assert_frame_equal(
        pd.read_json("company_by_min_p_e.json", orient="records"),
        pd.read_json(test_dir / "verified_company_by_min_p_e.json", orient="records"),
    )
