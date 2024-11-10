# script with help from ChatGPT
# for TryHackMe room Hack Back https://tryhackme.com/r/room/hackback
# work with python 3.10
from web3 import Web3

# Initialize connection
rpc_url = "http://geth:8545"
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if connected
assert w3.is_connected(), "Failed to connect to RPC!"
# Player details
player_address = "0x28a0340F7EEb8045224eA237c4dEf072aeA65fc7"
private_key = "0x55a284bcc207ba63c9d3ddd4837fa2657b0dafde3d91c173cb9a51671b4ebce4"

# Contract details
contract_address = "0xf22cB0Ca047e88AC996c17683Cee290518093574"
contract_abi = [
    {
        "inputs": [{"internalType": "string", "name": "data", "type": "string"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "out", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isSolved",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Decode the target string
target = "ZI^ZI^U_MJI"
key = 44
decoded_data = ''.join(chr(ord(char) ^ key) for char in target)
print(f"Decoded input: {decoded_data}")

# Initialize the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Prepare the transaction to call `transfer`
nonce = w3.eth.get_transaction_count(player_address)
transaction = contract.functions.transfer(decoded_data, 1000).build_transaction({
    'chainId': 31337,
    'gas': 2000000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'nonce': nonce
})

# Sign the transaction
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Transaction receipt: {tx_receipt}")

# Check if the challenge is solved
is_solved = contract.functions.isSolved().call()
print(f"Challenge Solved: {is_solved}")
