import argparse
import asyncio
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def process_file(file_path, data, pbar: tqdm):
    with open(file_path) as f:
        for line in f:
            address, apparition = line.strip().split(",")
            if address not in data:
                data[address] = int(apparition)
            else:
                data[address] += int(apparition)

    pbar.update(1)


async def combine_csv(input_dir, output_dir, max_workers: int):
    data = {}
    input_files = [file for file in os.listdir(input_dir) if file.endswith(".csv")]

    with tqdm(total=len(input_files), unit="file") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for file in input_files:
                file_path = os.path.join(input_dir, file)
                future = loop.run_in_executor(
                    executor, process_file, file_path, data, pbar
                )
                futures.append(future)

            await asyncio.gather(*futures)

    # order data
    data = {
        k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)
    }

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "addresses.csv"), "w") as outfile:
        for address in data:
            outfile.write(address + "," + str(data[address]) + "\n")

    with open(os.path.join(output_dir, "addresses.txt"), "w") as outfile:
        for address in data:
            outfile.write(address + "\n")

    print("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="The input directory", type=str, required=True
    )
    parser.add_argument(
        "-o", "--output", help="The output directory", type=str, required=True
    )
    parser.add_argument(
        "-w",
        "--workers",
        help="Numbers of workers",
        type=int,
        default=os.cpu_count() or 1,
    )
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(combine_csv(args.input, args.output, args.workers))
