import json
import aiohttp
from ratelimit import sleep_and_retry, limits
from libs.utils import log, Color


class Provider:
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
    @limits(calls=5, period=1)  # 5 req/s
    async def request_solana(self, function, *args):
        url = self._provider

        payload = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": function, "params": args}
        )
        headers = {"Content-Type": "application/json"}

        response = await self._session.post(url, headers=headers, data=payload)
        log(url, color=Color.GRAY)

        response.raise_for_status()
        response = await response.json()
        if "error" in response:
            raise Exception(response["error"]["code"], response["error"]["message"])

        return response

    # get UNIX time for a slot (a block)
    async def get_slot_time(self, slot, skip_error=False):
        try:
            response = await self.request_solana("getBlockTime", slot)
        except Exception as e:
            if skip_error:
                date = None
                while date is None:
                    # remove aproximative 5 minutes
                    slot -= 300 * 2
                    response = {"result": None}
                    try:
                        response = await self.request_solana("getBlockTime", slot)
                    except Exception:
                        pass
                    date = response["result"]
                return date
            else:
                raise e

        return response["result"]
