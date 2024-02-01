# Bon, c'est un peu le bordel ici
# On utilise deux APIs qui sont différents, donc on doit faire une classe Provider pour chacun d'entre eux...

import asyncio
import json
import aiohttp
from ratelimit import sleep_and_retry, limits
from libs.utils import has_duplicates, logWarning, log, Color, chunkify


class BaseProvider:
    def __init__(
        self,
        baseUrl: str,
    ):
        self._baseUrl = baseUrl

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=None, sock_connect=None, sock_read=None)
        )
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def post_wrapper(self, url, headers, payload) -> any:
        attempt = 0
        retries = 10

        while attempt < retries:
            log(
                url,
                color=Color.GRAY,
            )
            response = await self._session.post(url, headers=headers, data=payload)

            if response.status == 200:
                response = await response.json()

                if "error" in response:
                    raise Exception(
                        response["error"]["code"], response["error"]["message"]
                    )

                return response
            elif response.status == 429 or response.status == 104:  # Retry error
                attempt += 1
                logWarning(
                    f"Got {response.status} error. Retrying ({attempt}/{retries})..."
                )
                await asyncio.sleep(1)  # Wait for some time before retrying
            else:
                response.raise_for_status()

        raise Exception("Max attemps reached. Aborting requests.")


class RPCProvider(BaseProvider):
    @sleep_and_retry
    @limits(calls=1, period=1 / 5)
    async def request(self, function, *args):
        payload = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": function, "params": args}
        )
        headers = {"Content-Type": "application/json"}

        return await self.post_wrapper(self._baseUrl, headers, payload)

    async def get_signatures(self, address, max_signatures_count=10000):
        LIMIT = 1_000
        signatures = []
        lastestSignature = None

        while True:
            res = await self.request(
                "getSignaturesForAddress",
                address,
                {"before": lastestSignature, "limit": LIMIT},
            )

            for s in res["result"]:
                signatures.append(s["signature"])

            lastestSignature = signatures[-1]

            if len(signatures) > max_signatures_count:
                logWarning(
                    "Aborting",
                    str(address),
                    "because it has more than",
                    str(max_signatures_count),
                    "transactions.",
                )
                return None

            if len(res["result"]) < LIMIT:
                if has_duplicates(signatures):
                    logWarning("Duplicate while getting signatures for " + str(address))

                return signatures


class SolanaFMProvider(BaseProvider):
    @sleep_and_retry
    @limits(calls=5, period=1)  # 5 req/s
    async def request(self, suffix, payload):
        url = self._baseUrl + suffix

        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}

        return await self.post_wrapper(url, headers, payload)

    async def get_transactions(self, signatures):
        transactions = []
        signatures_chunk = chunkify(signatures, 50)

        for chunk in signatures_chunk:
            res = await self.request("/v0/transfers", {"transactionHashes": chunk})
            transactions.extend(res["result"])

        return transactions
