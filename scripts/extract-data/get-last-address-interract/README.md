# Get last address have interacted with Solana blockchain
This script will get last address have interacted with Solana blockchain and save to file.  
Caution: This script will get all blocks from start date to now, so it will take a long time to run.

## Installation
1. Clone this repository
2. Install requirements
```bash
pip3 install -r requirements.txt
```

## Usage
Run the script
```bash
python3 main.py
```

You can use these options:

- `-h` or `--help` for show help message

## Information
Due to long time of execution of the script, you can stop the script and run it again.
For get a final file without finish the main script you can use `combine_csv.py` script.
```bash
python3 combine_csv.py
```

You can use these options:

- `-h` or `--help` for show help message
- `-i` or `--input` for set input directory
- `-o` or `--output` for set output directory