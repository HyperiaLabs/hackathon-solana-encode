import json
import aiohttp
from ratelimit import sleep_and_retry, limits
from libs.log import logWarning, log, Color
import asyncio


class RPCProvider:
    def __init__(
        self,
        provider: str,
    ):
        self._provider = provider

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=None, sock_connect=None, sock_read=None)
        )
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    @sleep_and_retry
    @limits(calls=1, period=0.032)  # 30 req/s
    async def request_solana(self, function, *args):
        url = self._provider

        payload = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": function, "params": args}
        )
        headers = {"Content-Type": "application/json"}

        attempt = 0
        retries = 10
        while attempt < retries:
            response = await self._session.post(url, headers=headers, data=payload)
            # log(url, color=Color.GRAY)

            if response.status == 200:
                response = await response.json()

                if "error" in response:
                    raise Exception(
                        response["error"]["code"], response["error"]["message"]
                    )

                return response
            elif response.status == 429:  # Too Many Requests
                logWarning(f"Got 429 error. Retrying ({attempt + 1}/{retries})...")
                await asyncio.sleep(1)  # Wait for some time before retrying
                attempt += 1
            else:
                response.raise_for_status()

    async def is_smart_contract(self, address: str) -> bool:
        res = await self.request_solana(
            "getAccountInfo", address, {"encoding": "base64"}
        )

        if res["result"]["value"] is None:
            raise Exception("The account value is null. What does it mean ?")

        SYSTEM_PROGRAM = "11111111111111111111111111111111"
        return res["result"]["value"]["owner"] != SYSTEM_PROGRAM
