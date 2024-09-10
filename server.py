import json

from flask import Flask, jsonify, request, Response
import aiohttp
import asyncio

app = Flask(__name__)


async def send_request(session, *args, **kwargs):
    async with session.request(*args, **kwargs) as response:
        return {
            "status_code": response.status,
            "payload": await response.text()
        }


async def gather_responses(count, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, *args, **kwargs) for _ in range(count)]
        return await asyncio.gather(*tasks)


@app.route('/spam/<path:count>/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
async def proxy_request(count, url):
    print(url)
    # Извлекаем заголовки запроса
    headers = {key: value for key, value in request.headers if key != 'Host'}

    responses = await gather_responses(
        int(count),
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        params=request.args,
        cookies=request.cookies
    )

    # Возвращаем ответ от целевого сервера
    return Response(
        json.dumps(responses),
        status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
