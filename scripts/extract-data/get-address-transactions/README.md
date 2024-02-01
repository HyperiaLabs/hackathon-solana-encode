# Get all transactions of one or more specific address for Solana blockchain

This repository is used to get all transactions of one or more specific address for Solana blockchain.  
It contains two scripts:
- `get_all_txs.py`: get all transactions of one address
- `get_all_txs_multi.py`: get all transactions of multiple addresses

## Installation
1. Clone this repository
2. Install requirements
```bash
pip3 install -r requirements.txt
```

## Usage
### Get all transactions of one address
Run script
```bash
python3 get_all_txs.py -a ADDRESS_HERE
```

You can use these options:

- `-h` or `--help` for show help message
- `-a` or `--address` for address
- `-o` or `--output` for output directory
- `-p` or `--provider` for provider url

### Get all transactions of multiple addresses
Run script
```bash
python3 get_all_txs_multi.py -l LIST_FILE_HERE
```

You can use these options:

- `-h` or `--help` for show help message
- `-l` or `--list` for list file
- `-o` or `--output` for output directory
- `-p` or `--provider` for provider url