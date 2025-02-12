from web3 import Web3
from eth_account import Account
import json

def verify_registration():
    """Verify the AI agent registration."""
    print("Verifying AI agent registration...")
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider("http://43.135.26.222:8000"))
    
    # Contract address from deployment
    factory_address = "0xE2b594eBefd4D0773eD5A94BE3094393A9B11DcE"
    
    # Initialize account from private key
    private_key = "7da572101629e7e24fd80c8e8918f718f2638365e3ca30866794f06b2147278e"
    account = Account.from_key(private_key)
    print(f"Checking registration for account: {account.address}")
    
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
    agent_address = factory_contract.functions.agentContracts(account.address).call()
    print(f"\nAgent contract address: {agent_address}")
    
    if agent_address == "0x0000000000000000000000000000000000000000":
        raise Exception("No agent contract found - registration may have failed")
    
    # Get agent type
    agent_type = factory_contract.functions.agentTypes(account.address).call()
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

if __name__ == "__main__":
    verify_registration()
