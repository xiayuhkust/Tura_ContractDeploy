from web3 import Web3
from eth_account import Account
import json
from solcx import compile_standard
import os

def compile_and_deploy():
    print("Compiling and deploying contracts...")
    
    # Read contract sources
    with open('contracts/AIAgent.sol', 'r') as f:
        agent_source = f.read()
    with open('contracts/AIAgentRegistryFactory.sol', 'r') as f:
        registry_source = f.read()
    
    # Compile contracts
    print("Compiling contracts...")
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "AIAgent.sol": {"content": agent_source},
            "AIAgentRegistryFactory.sol": {"content": registry_source}
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            },
            "optimizer": {
                "enabled": True,
                "runs": 200
            }
        }
    }, solc_version="0.8.20")
    
    # Get contract data
    registry_contract = compiled_sol['contracts']['AIAgentRegistryFactory.sol']['AIAgentRegistryFactory']
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider("http://43.135.26.222:8000"))
    
    # Initialize account
    private_key = "ad6fb1ceb0b9dc598641ac1cef545a7882b52f5a12d7204d6074762d96a8a474"
    account = Account.from_key(private_key)
    print(f"Deploying from account: {account.address}")
    
    # Deploy contract
    contract = w3.eth.contract(
        abi=registry_contract['abi'],
        bytecode=registry_contract['evm']['bytecode']['object']
    )
    
    # Deploy parameters
    token_address = "0x0000000000000000000000000000000000000000"
    min_stake = w3.to_wei(1, 'ether')
    
    print("\nDeployment parameters:")
    print(f"Token address: {token_address}")
    print(f"Minimum stake: {min_stake} wei")
    
    transaction = contract.constructor(
        token_address,
        min_stake
    ).build_transaction({
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
    compile_and_deploy()
