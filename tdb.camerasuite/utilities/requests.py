import aiohttp
import ujson


async def get_json(url) -> dict:
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.get(url) as response:
            return await response.json()


async def put_json(url, json) -> dict:
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.put(url, json=json) as response:
            return await response.json()
