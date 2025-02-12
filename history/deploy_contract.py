from web3 import Web3
from eth_account import Account
import json
import os

def deploy_strategy_agent():
    """Deploy StrategyAgent contract."""
    print("Deploying StrategyAgent contract...")
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider("http://43.135.26.222:8000"))
    
    # Load contract data
    contract_path = os.path.join(os.path.dirname(__file__), "StrategyAgent.compiled.json")
    with open(contract_path, "r") as f:
        contract_data = json.load(f)
    
    # Initialize account with private key from environment
    private_key = os.getenv("TURA_PRIVATE_KEY")
    if not private_key:
        raise ValueError("TURA_PRIVATE_KEY environment variable not set")
    account = Account.from_key(private_key)
    print(f"Deploying from account: {account.address}")
    
    # Deploy contract
    contract = w3.eth.contract(abi=contract_data['abi'], bytecode=contract_data['bytecode'])
    
    # Deploy with owner, multisig addresses array, and native token address
    owner_address = "0x009f54E5CcbEFCdCa0dd85ddc85171A76B5c1ef1"
    multisig_addresses = ["0x009f54E5CcbEFCdCa0dd85ddc85171A76B5c1ef1", "0x08Bb6eA809A2d6c13D57166Fa3ede48C0ae9a70e"]
    native_token = "0x0000000000000000000000000000000000000000"
    
    print("\nDeployment parameters:")
    print(f"Owner: {owner_address}")
    print(f"Multisig addresses: {multisig_addresses}")
    print(f"Native token: {native_token}")
    
    transaction = contract.constructor(
        owner_address,
        multisig_addresses,
        native_token
    ).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 3000000,  # Increased gas limit for complex constructor
        "gasPrice": w3.eth.gas_price
    })
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"\nTransaction hash: {tx_hash.hex()}")
    print("Waiting for transaction receipt...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    contract_address = tx_receipt['contractAddress']
    print(f"Contract deployed at: {contract_address}")
    return contract_address

if __name__ == "__main__":
    deploy_strategy_agent()
