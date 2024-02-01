import argparse
import asyncio
import os
from datetime import datetime
from tqdm.asyncio import tqdm

from libs.utils import log
from libs.provider import Provider


async def process_slot(
    provider: Provider, blocks_dir: str, slot: int, semaphore: asyncio.Semaphore
):
    async with semaphore:
        slot_file = blocks_dir + "/" + str(slot) + ".csv"
        block_addresses = {}

        # if already file exist, get from file
        if os.path.exists(slot_file):
            log("get addresses from block " + str(slot) + " from file")
            with open(slot_file) as f:
                for line in f:
                    address, apparition = line.strip().split(",")
                    if address not in block_addresses:
                        block_addresses[address] = int(apparition)
                    else:
                        block_addresses[address] += int(apparition)
        else:
            log("getting block " + str(slot) + " from API")
            object = {
                "encoding": "json",
                "transactionDetails": "accounts",
                "rewards": False,
                "maxSupportedTransactionVersion": 0,
            }
            try:
                data = await provider.request_solana("getBlock", slot, object)

                # get address from block
                for transaction in data["result"]["transactions"]:
                    for account in transaction["transaction"]["accountKeys"]:
                        address = account["pubkey"]
                        if address not in block_addresses:
                            block_addresses[address] = 1
                        else:
                            block_addresses[address] += 1

                # write block in file
                with open(slot_file, "w") as outfile:
                    for address in block_addresses:
                        outfile.write(
                            address + "," +
                            str(block_addresses[address]) + "\n"
                        )
            except Exception as e:
                code, _ = e.args
                if (
                    code == -32009
                ):  # Slot X was skipped, or missing in long-term storage
                    log("skip block " + str(slot))

                else:
                    raise e


async def get_lastest_slot(provider: Provider):
    # get last block
    response = await provider.request_solana(
        "getLatestBlockhash", {"commitment": "finalized"}
    )
    # Solana have approximately 2 blocks per second
    # TODO remove approximative
    last_slot = response["result"]["context"]["slot"]
    last_blockhash = response["result"]["value"]["blockhash"]
    log("last_slot: " + str(last_slot))
    log("last_blockhash: " + last_blockhash)

    return last_slot


async def get_first_slot(provider: Provider, start_date, is_slot, last_slot):
    date_now = datetime.timestamp(datetime.now())

    first_slot = start_date
    if not is_slot:
        # get first slot of start date, if start date is a UNIX timestamp
        # Solana have approximately 2 blocks per second
        # TODO remove approximative
        first_slot = last_slot - int((date_now - start_date) * 2)
        date_first_slot = await provider.get_slot_time(first_slot, True)
        while date_first_slot > start_date:
            # remove approximative 1 day
            first_slot -= 86400 * 2
            log("get new slot:", str(first_slot))
            date_first_slot = await provider.get_slot_time(first_slot, True)
        log(
            "block time for slot "
            + str(first_slot)
            + ": "
            + str(date_first_slot)
            + " -> "
            + datetime.fromtimestamp(date_first_slot).strftime("%Y-%m-%d %H:%M:%S")
        )

    return first_slot


async def main(
    start_date, is_slot, output_dir, provider_url: str, threads: int, block_step: int
):
    semaphore = asyncio.Semaphore(threads)

    async with Provider(provider_url) as provider:
        last_slot = await get_lastest_slot(provider)
        first_slot = await get_first_slot(provider, start_date, is_slot, last_slot)

        blocks_dir = output_dir + "/blocks"
        os.makedirs(blocks_dir, exist_ok=True)

        log("Organisation tasks queue...")
        tasks = [
            asyncio.create_task(process_slot(
                provider, blocks_dir, slot, semaphore))
            for slot in range(first_slot, last_slot, block_step)
        ]
        log("Tasks ready!")

        with tqdm(total=(last_slot - first_slot) / block_step, unit="block") as pbar:
            for coroutine in asyncio.as_completed(tasks):
                try:
                    await coroutine
                except Exception as e:
                    log("Got an exception:", e)
                finally:
                    pbar.update(1)

        log("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--start-date",
        "--slot",
        help="The start date in UNIX timestamp or the start slot",
        type=int,
        default=datetime.timestamp(datetime.now()) - 2592000,  # 30 days ago
    )
    parser.add_argument(
        "--is-slot",
        help="True is start-date is a slot, False if start-date is a UNIX timestamp",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-p",
        "--provider",
        help="The Solana provider",
        type=str,
        default="https://api.mainnet-beta.solana.com",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The output directory",
        type=str,
        default="output/" + str(int(datetime.timestamp(datetime.now()))),
    )
    parser.add_argument(
        "-t",
        "--threads",
        help="Count of threads",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--block-step",
        help="Step between each block",
        type=int,
        default=1,
    )
    args = parser.parse_args()

    log("Using " + str(args.threads) + " threads.")

    asyncio.run(
        main(
            args.start_date,
            args.is_slot,
            args.output,
            args.provider,
            args.threads,
            args.block_step,
        )
    )
