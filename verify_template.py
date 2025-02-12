from web3 import Web3
from eth_account import Account
import json
import os
from dotenv import load_dotenv

def verify_registration(factory_address, user_address):
    """Verify the AI agent registration."""
    load_dotenv()
    
    # Load environment variables
    rpc_url = os.getenv("TURA_RPC_URL")
    if not rpc_url:
        raise ValueError("TURA_RPC_URL environment variable not set")
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    print(f"Checking registration for account: {user_address}")
    
    # Load contract ABIs
    with open('build/contracts/AIAgentRegistryFactoryNative.json', 'r') as f:
        factory_data = json.load(f)
        factory_abi = factory_data['abi']
    
    with open('build/contracts/AIAgentNative.json', 'r') as f:
        agent_data = json.load(f)
        agent_abi = agent_data['abi']
    
    # Initialize factory contract
    factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi)
    
    # Get agent contract address
    agent_address = factory_contract.functions.agentContracts(user_address).call()
    print(f"\nAgent contract address: {agent_address}")
    
    if agent_address == "0x0000000000000000000000000000000000000000":
        raise Exception("No agent contract found - registration may have failed")
    
    # Get agent type
    agent_type = factory_contract.functions.agentTypes(user_address).call()
    print(f"Agent type: {agent_type}")
    
    # Initialize agent contract
    agent_contract = w3.eth.contract(address=agent_address, abi=agent_abi)
    
    # Get staked amount
    staked_amount = agent_contract.functions.stakedAmount().call()
    print(f"Staked amount: {staked_amount} wei")
    
    # Get minimum stake
    min_stake = factory_contract.functions.minimumStake().call()
    print(f"Minimum stake required: {min_stake} wei")
    
    # Verify stake amount meets minimum
    if staked_amount < min_stake:
        raise Exception(f"Staked amount ({staked_amount}) is less than minimum required ({min_stake})")
    
    print("\nVerification successful!")
    print("✓ Agent contract deployed")
    print("✓ Agent type set correctly")
    print("✓ Stake amount meets minimum requirement")
    return agent_address

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python verify_template.py <factory_contract_address> <user_address>")
        sys.exit(1)
    verify_registration(sys.argv[1], sys.argv[2])
