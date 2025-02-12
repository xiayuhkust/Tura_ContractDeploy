from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv

def register_agent(factory_address):
    """Register user as an AI agent using native TURA tokens."""
    load_dotenv()
    
    # Load environment variables
    rpc_url = os.getenv("TURA_RPC_URL")
    private_key = os.getenv("TURA_PRIVATE_KEY")
    
    if not rpc_url or not private_key:
        raise ValueError("Required environment variables not set. Check .env.example")
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    account = Account.from_key(private_key)
    print(f"Using account: {account.address}")
    
    # Load contract ABI
    with open('build/contracts/AIAgentRegistryFactoryNative.json', 'r') as f:
        factory_data = json.load(f)
        factory_abi = factory_data['abi']
    
    # Initialize contract
    factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi)
    
    # Get minimum stake amount
    min_stake = factory_contract.functions.minimumStake().call()
    print(f"Minimum stake required: {min_stake} wei")
    
    # Check balance
    balance = w3.eth.get_balance(account.address)
    print(f"Account balance: {balance} wei")
    
    if balance < min_stake:
        raise Exception(f"Insufficient balance. Need {min_stake} wei but only have {balance} wei")
    
    # Register as AI agent with native token value
    register_tx = factory_contract.functions.registerAgent(
        0  # RegistrationType.AI_AGENT
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 500000,  # Increased gas limit for contract deployment
        'gasPrice': w3.eth.gas_price,
        'value': min_stake  # Send native TURA token
    })
    
    # Sign and send registration transaction
    signed_register = w3.eth.account.sign_transaction(register_tx, private_key)
    register_hash = w3.eth.send_raw_transaction(signed_register.raw_transaction)
    print(f"Registration transaction hash: {register_hash.hex()}")
    
    # Wait for transaction receipt
    receipt = w3.eth.wait_for_transaction_receipt(register_hash)
    
    print("\nRegistration complete!")
    print(f"Transaction status: {'Success' if receipt['status'] == 1 else 'Failed'}")
    print(f"Gas used: {receipt['gasUsed']}")
    
    if receipt['status'] == 0:
        print("\nTransaction failed. Details:")
        print(receipt)
        raise Exception("Registration transaction failed")
    
    # Verify registration
    agent_contract = factory_contract.functions.agentContracts(account.address).call()
    print(f"\nVerification:")
    print(f"Agent contract deployed at: {agent_contract}")
    return agent_contract

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python register_template.py <factory_contract_address>")
        sys.exit(1)
    register_agent(sys.argv[1])
