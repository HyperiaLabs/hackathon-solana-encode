import json
import os
from libs.provider import RPCProvider, SolanaFMProvider
from libs.utils import log, Color
import argparse
import asyncio
from datetime import datetime


async def main(address, outputDir, rpc_base_url: str, fm_base_url: str):
    async with RPCProvider(rpc_base_url) as rpc_provider:
        async with SolanaFMProvider(fm_base_url) as fm_provider:
            await get_all_txs(address, outputDir, rpc_provider, fm_provider)


async def get_all_txs(
    address,
    output_dir,
    rpc_provider: RPCProvider,
    fm_provider: SolanaFMProvider,
):
    signatures = await rpc_provider.get_signatures(address)

    if signatures is None:
        return

    os.makedirs(output_dir, exist_ok=True)

    signatures = remove_already_requested_signatures(signatures, output_dir)

    if len(signatures) > 0:
        transactions = await fm_provider.get_transactions(signatures)

        # writing transactions to file
        for transaction in transactions:
            path = output_dir + "/" + transaction["transactionHash"] + ".json"

            if os.path.exists(path):
                continue

            with open(path, "w") as file:
                json.dump(transaction, file, indent=2)

    log("Address " + address + " processed.", color=Color.GREEN)


def remove_already_requested_signatures(signatures, output_dir):
    fichiers_output = os.listdir(output_dir)
    signatures = [
        element
        for element in signatures
        if not any(fichier in element for fichier in fichiers_output)
    ]

    return signatures


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        help="The wallet address to start the search from",
        type=str,
        required=True,
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
    args = parser.parse_args()

    asyncio.run(main(args.address, args.output, args.rpc_provider, args.fm_provider))
