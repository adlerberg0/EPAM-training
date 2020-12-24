import asyncio
import re
from dataclasses import dataclass, fields
from datetime import datetime
from typing import Optional

import aiohttp
import bs4
import pandas as pd
from bs4 import BeautifulSoup

stonks_url = "https://markets.businessinsider.com"


@dataclass()
class CompanyInfo:
    name: str = ""
    code: str = ""
    P_E: float = 0
    price: float = 0
    url: str = ""
    year_growth: float = 0
    max_income: float = 0


def retrieve_main_page_company_info(company: CompanyInfo, raw_data: bs4.Tag) -> None:
    company.url = str(raw_data.findChild("a")["href"])
    company.name = str(raw_data.findChild("a")["title"])
    company.year_growth = float(
        raw_data.findChildren("span")[8].string.replace(",", "")
    )


async def parse_company_page_info(
    company: CompanyInfo,
    session: aiohttp.ClientSession,
    base_url: str,
    dollar_course: float,
) -> None:
    async with session.get(base_url + company.url) as resp:
        if resp.status != 200:
            raise ConnectionError
        soup = BeautifulSoup(await resp.text(), "lxml")
        # get company price in ruble
        price_tag = soup.find("span", class_="price-section__current-value")
        if price_tag:
            company.price = float(price_tag.string.replace(",", "")) * dollar_course
        # get company code
        code_tag = soup.find("span", class_="price-section__category")
        if code_tag:
            company.code = code_tag.findChild("span").string.strip(", ")
        # get for P/E Ratio

        p_e_tag = soup.find(
            "div", string="P/E Ratio"
        )  # doesn't work with both class and string params :(
        if p_e_tag:
            company.P_E = float(next(p_e_tag.parent.strings).replace(",", ""))

        # get low/high 52weeks         TO DO: how to optimize code below?
        pattern = re.compile(r"low52weeksDisplay: '(.*?)',")
        var = soup.find("script", string=pattern)
        if var:
            match = pattern.search(str(var))
            if match:
                low52weeks = float(match.group(1).replace(",", ""))
        pattern = re.compile(r"high52weeksDisplay: '(.*?)',")
        var = soup.find("script", string=pattern)
        if var:
            match = pattern.search(str(var))
            if match:
                high52weeks = float(match.group(1).replace(",", ""))
        company.max_income = (high52weeks - low52weeks) / low52weeks


async def get_dollar_course_value(markup: str) -> float:
    soup = BeautifulSoup(markup, "lxml")
    return float(soup.find("valute", id="R01235").value.string.replace(",", "."))


async def parse_information_from_one_page(
    session,
    base_url: str,
    addition: str,
    company_list: list,
    task_list: list,
    dollar_course: float,
    page_param: dict,
) -> Optional[int]:
    async with session.get(base_url + addition, params=page_param) as resp:
        if resp.status != 200:
            raise ConnectionError

        soup = BeautifulSoup(await resp.text(), "lxml")
        # we have 11th page which is not listed in the finando_paging class
        # so we'll traverse through pages until we won't find the table container index-list-container
        if not soup.find(id="index-list-container"):
            return -1
        table = soup.find("table", class_="table table-small")
        table_header = table.findChild()

        for raw in table_header.find_next_siblings():
            company = CompanyInfo()
            company_list.append(company)
            retrieve_main_page_company_info(company, raw)
            task_list.append(
                asyncio.create_task(
                    parse_company_page_info(company, session, base_url, dollar_course)
                )
            )


async def write_result_to_json(company_list: list) -> None:
    field_names = [field.name for field in fields(CompanyInfo)]
    df = pd.DataFrame(company_list, columns=field_names)
    df.sort_values(by=["price"], ascending=False)[0:10].to_json(
        "company_by_price.json", orient="records"
    )
    df.sort_values(by=["year_growth"], ascending=False)[0:10].to_json(
        "company_by_year_growth.json", orient="records"
    )
    df.sort_values(by=["max_income"], ascending=False)[0:10].to_json(
        "company_by_max_income.json", orient="records"
    )
    df.sort_values(by=["P_E"])[0:10].to_json(
        "company_by_min_p_e.json", orient="records"
    )


async def main_task(base_url: str, addition: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("http://www.cbr.ru/scripts/XML_daily.asp") as resp:
            if resp.status != 200:
                raise ConnectionError
            dollar_course = await get_dollar_course_value(
                await resp.text(),
            )
        # we start from first page
        page_param = {"p": 1}
        task_list = []
        company_list = []
        while True:
            res = await parse_information_from_one_page(
                session,
                base_url,
                addition,
                company_list,
                task_list,
                dollar_course,
                page_param,
            )
            # traverse through pages until func return -1
            if res == -1:
                break
            page_param["p"] += 1

        await asyncio.gather(*task_list)
        await write_result_to_json(company_list)


if __name__ == "__main__":
    start = datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_task(stonks_url, "/index/components/s&p_500"))
    print(datetime.now() - start)
