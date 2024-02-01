import argparse
import shutil
import os
import asyncio
from tqdm import tqdm
from libs.log import Color, log, logError
from libs.provider import RPCProvider


async def main(input_file: str, rpc_url: str, workers: int):
    sem = asyncio.Semaphore(workers)

    async with RPCProvider(rpc_url) as rpc_provider:
        tasks = create_tasks(input_file, rpc_provider, sem)

        output_file = input_file + ".output"
        await execute_tasks(tasks, output_file)

    print("Done")


def create_tasks(input_file: str, rpc_provider: RPCProvider, sem: asyncio.Semaphore):
    tasks = []
    log("Reading list " + input_file)
    with open(input_file) as file:
        for line in tqdm(file):
            address = line.strip()
            tasks.append(asyncio.create_task(task_wrapper(address, rpc_provider, sem)))
    log("Tasks ready!", color=Color.GREEN)
    return tasks


async def task_wrapper(
    address: str, provider: RPCProvider, sem: asyncio.Semaphore
) -> (str, bool):
    async with sem:
        return (address, await provider.is_smart_contract(address))


async def execute_tasks(tasks, output_file):
    with open(output_file, "w") as output:
        with tqdm(
            total=len(tasks),
            desc="Addresses",
            unit=" address",
            ncols=80,
            smoothing=0,
        ) as pbar:
            for is_smart_contract in asyncio.as_completed(tasks):
                try:
                    (address, sc) = await is_smart_contract

                    if sc is True:
                        log(address, "is a smart contract", color=Color.YELLOW)
                    else:
                        log(address, "is a user", color=Color.GREEN)
                        output.write(address + "\n")

                except Exception as e:
                    logError("Got an exception:", e)

                pbar.update(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="The input file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--rpc-provider",
        help="A Solana RPC provider",
        type=str,
        default="https://api.mainnet-beta.solana.com",
    )
    parser.add_argument(
        "-t",
        "--threads",
        help="Count of threads",
        type=int,
        default=5,
    )
    args = parser.parse_args()

    asyncio.run(main(args.input, args.rpc_provider, args.threads))
