from web3 import Web3
from eth_account import Account
import json

def verify_deployment():
    print("Verifying contract deployment...")
    
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider("http://43.135.26.222:8000"))
    
    # Contract address from deployment
    contract_address = "0x00Bdaa6317e589b02414119434eED10220D4AF88"
    
    # Load contract ABI
    with open('build/contracts/AIAgentRegistryFactory.json', 'r') as f:
        contract_data = json.load(f)
        abi = contract_data['abi']
    
    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    # Verify contract state
    print("\nVerifying contract state:")
    admin = contract.functions.admin().call()
    min_stake = contract.functions.minimumStake().call()
    token = contract.functions.token().call()
    
    print(f"Admin address: {admin}")
    print(f"Minimum stake: {min_stake} wei")
    print(f"Token address: {token}")
    
    # Verify our account is admin
    private_key = "ad6fb1ceb0b9dc598641ac1cef545a7882b52f5a12d7204d6074762d96a8a474"
    account = Account.from_key(private_key)
    is_admin = (admin.lower() == account.address.lower())
    print(f"\nDeployer is admin: {is_admin}")

if __name__ == "__main__":
    verify_deployment()
