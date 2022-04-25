import json
import os
from dotenv import load_dotenv
from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os

# from dotenv import load_dotenv

load_dotenv()

# Open the solidity code file and copy all of its content into simpple_storage_file variable
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# print(simple_storage_file)

# We add these two lines that we forgot from the video!
print("Installing Solidity Compiler...")
# Install/Prepare a compiler to compile the solidity code
install_solc("0.6.0")

# Solidity source code is compiled and the compiled code it stored into a JSON format with all the compiled code material
# like abi, OPCodes, bytecode and metadata
print("Compiling Solidity Code...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

# print(compiled_sol)

# stored the solidity compiled code into a new external JSON file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# from the JSON external file, fetch separate part of the compiled output
# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# print("Print Bytecode")
# print(bytecode)
# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# print("Print ABI")
# print(abi)

# # w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# # chain_id = 4

# For connecting to ganache
print("Connecting to the Ganache Blockchain...")
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337

my_address = "0xf3d57502E4F62e90c2e19183C46a3070E1cf461E"
private_key = os.getenv("PRIVATE_KEY")
# print(private_key)

# Create the contract in Python as ControlObject (this is not yet deployed on the blockchain)
print("Creating contract object...")
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print("Creating a transation...")
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Contract as bundled in a transaction and transaction is now signed by us...")
# Send it!
print("Sending Transaction to the blockchain")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
# w3 -> already connected to the blockchain, we fetch all the details about the contract into simple_storage
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print("Latest state of the contract is fetched...")
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
# to actually change the state of a variable on the blockchain, we need to create, sign and send it as a transaction
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
# Waits for the transaction specified by transaction_hash to be included in a block, then returns its transaction receipt.
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
print(simple_storage.functions.retrieve().call())
