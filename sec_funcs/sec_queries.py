from sec_api import QueryApi

import aiohttp


async def async_get_request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url,
                               headers={'token': "30d52e6e37ff6b4f07bcb15a3c62fcd4aa8be5b8bb5e142f4dcb79410934e4d5",
                                        'type': 'html'}) as response:
            if response.status == 200:
                return await response.read()


async def download_file(url: str):
    file_content = await async_get_request(url)
    if file_content is not None:
        return file_content
    return None
    # input_file = InputFile(file_content)
    # await bot.send_document(chat_id, input_file)


class sec:
    queryApi = QueryApi(api_key="30d52e6e37ff6b4f07bcb15a3c62fcd4aa8be5b8bb5e142f4dcb79410934e4d5")


def get_report_url(Ticket: str, date: str, type: str):
    query = {
        "query": {"query_string": {
            "query": f"ticker:{Ticket} AND filedAt:" + '{' + f"{date}-01-01 TO {date}-12-31" + "}" + f" AND formType:\"{type}\""
        }},
        "from": "0",
        "size": "10",
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    filings = sec.queryApi.get_filings(query)
    for item in filings['filings'][0]['documentFormatFiles']:
        if item['description'] == type:
            return item['documentUrl']
