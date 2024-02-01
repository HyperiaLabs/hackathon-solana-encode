import argparse
import asyncio
from datetime import datetime
import os
from tqdm import tqdm

from get_all_txs import get_all_txs
from libs.provider import RPCProvider, SolanaFMProvider
from libs.utils import log, Color, logError
import traceback


async def task(
    address,
    outputDir,
    rpc_provider: RPCProvider,
    fm_provider: SolanaFMProvider,
    sem: asyncio.Semaphore,
):
    async with sem:
        await get_all_txs(address, outputDir, rpc_provider, fm_provider)


async def get_all_txs_multi(
    listFile, outputDir, rpc_url: str, fm_url: str, workers: int
):
    os.makedirs(outputDir, exist_ok=True)

    async with RPCProvider(rpc_url) as rpc_provider:
        async with SolanaFMProvider(fm_url) as fm_provider:
            log("Using", workers, "workers")
            sem = asyncio.Semaphore(workers)

            log("Reading list " + listFile)
            tasks = []
            with open(listFile) as file:
                for line in tqdm(file):
                    address = line.strip()
                    tasks.append(
                        asyncio.create_task(
                            task(
                                address,
                                outputDir + "/" + address,
                                rpc_provider,
                                fm_provider,
                                sem,
                            )
                        )
                    )
            log("Tasks ready!", color=Color.GREEN)

            with tqdm(
                total=len(tasks),
                desc="Addresses",
                unit=" address",
                ncols=80,
                smoothing=0,
            ) as pbar:
                for future in asyncio.as_completed(tasks):
                    try:
                        await future
                    except Exception as e:
                        logError("Got an exception:", e, "\n", traceback.format_exc())

                    pbar.update(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--list",
        help="The list of wallet addresses to start the search from",
        type=str,
        default="input/wallets.txt",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The output directory",
        type=str,
        default="output/" + str(int(datetime.timestamp(datetime.now()))),
    )
    parser.add_argument(
        "--rpc-provider",
        help="A Solana RPC provider",
        type=str,
        default="https://api.mainnet-beta.solana.com",
    )
    parser.add_argument(
        "--fm-provider",
        help="The SolanaFM provider",
        type=str,
        default="https://api.solana.fm",
    )
    parser.add_argument(
        "-w",
        "--workers",
        help="Concurrency workers",
        type=int,
        default=1,
    )
    args = parser.parse_args()

    asyncio.run(
        get_all_txs_multi(
            args.list, args.output, args.rpc_provider, args.fm_provider, args.workers
        )
    )
