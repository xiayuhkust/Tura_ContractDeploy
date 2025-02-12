from web3 import Web3
from eth_account import Account
import json

def deploy_native_factory():
    """Deploy AIAgentRegistryFactoryNative contract."""
    print("Deploying AIAgentRegistryFactoryNative contract...")
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider("http://43.135.26.222:8000"))
    
    # Initialize account with private key from environment
    private_key = "7da572101629e7e24fd80c8e8918f718f2638365e3ca30866794f06b2147278e"
    account = Account.from_key(private_key)
    print(f"Deploying from account: {account.address}")
    
    # Load contract data
    with open('build/contracts/AIAgentRegistryFactoryNative.json', 'r') as f:
        contract_data = json.load(f)
    
    # Deploy contract
    contract = w3.eth.contract(abi=contract_data['abi'], bytecode=contract_data['bytecode'])
    
    # Set minimum stake to 1 TURA
    min_stake = w3.to_wei(1, 'ether')
    
    print("\nDeployment parameters:")
    print(f"Minimum stake: {min_stake} wei")
    
    transaction = contract.constructor(min_stake).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 3000000,
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
    deploy_native_factory()
