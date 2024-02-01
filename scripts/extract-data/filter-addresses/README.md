# Solana Address Validator

This Python script validates Solana addresses for executability using an RPC provider.

## Description

The script reads a list of Solana addresses from an input file and write only addresses owned by System Program to an output file.

## Prerequisites

- Python 3.x
- Ensure required Python libraries are installed by running:

```
pip install -r requirements.txt
```

## Usage

1. Install the required Python libraries:

  ```bash
  pip install -r requirements.txt
  ```

2. Run the script with the following command:

  ```bash
  python solana_address_validator.py -i <input_file_path> --rpc-provider <rpc_url> -t <threads_count>
  ```

  Replace:
  - `<input_file_path>`: Path to the input file containing Solana addresses.
  - `<rpc_url>`: Solana RPC provider URL. Default is set to `https://api.mainnet-beta.solana.com`.
  - `<threads_count>`: Count of threads to use for address validation. Default is set to `5`.

3. Example:

  ```bash
  python solana_address_validator.py -i input_addresses.txt --rpc-provider https://api.mainnet-beta.solana.com -t 10
  ```