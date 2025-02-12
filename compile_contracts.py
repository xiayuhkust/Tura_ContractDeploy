from solcx import compile_standard
import json
import os

def compile_contracts():
    print("Compiling contracts...")
    
    # Read contract sources
    with open('contracts/AIAgent.sol', 'r') as f:
        agent_source = f.read()
    with open('contracts/AIAgentRegistryFactory.sol', 'r') as f:
        registry_source = f.read()
    with open('contracts/AIAgentNative.sol', 'r') as f:
        agent_native_source = f.read()
    with open('contracts/AIAgentRegistryFactoryNative.sol', 'r') as f:
        registry_native_source = f.read()
    
    # Create build directory if it doesn't exist
    os.makedirs('build/contracts', exist_ok=True)
    
    # Compile contracts
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "AIAgent.sol": {"content": agent_source},
            "AIAgentRegistryFactory.sol": {"content": registry_source},
            "AIAgentNative.sol": {"content": agent_native_source},
            "AIAgentRegistryFactoryNative.sol": {"content": registry_native_source}
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
    
    # Save contract data
    with open('build/contracts/AIAgentRegistryFactory.json', 'w') as f:
        json.dump(compiled_sol['contracts']['AIAgentRegistryFactory.sol']['AIAgentRegistryFactory'], f, indent=2)
    
    with open('build/contracts/AIAgent.json', 'w') as f:
        json.dump(compiled_sol['contracts']['AIAgent.sol']['AIAgent'], f, indent=2)
    
    with open('build/contracts/AIAgentNative.json', 'w') as f:
        json.dump(compiled_sol['contracts']['AIAgentNative.sol']['AIAgent'], f, indent=2)
    
    # Save AIAgentRegistryFactoryNative contract data
    contract_data = compiled_sol['contracts']['AIAgentRegistryFactoryNative.sol']['AIAgentRegistryFactoryNative']
    contract_data['bytecode'] = contract_data['evm']['bytecode']['object']
    with open('build/contracts/AIAgentRegistryFactoryNative.json', 'w') as f:
        json.dump(contract_data, f, indent=2)
    
    # Also save IERC20 ABI
    ierc20_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {"name": "_spender", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "approve",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        }
    ]
    with open('build/contracts/IERC20.json', 'w') as f:
        json.dump({"abi": ierc20_abi}, f, indent=2)
    
    print("Compilation complete! Contract artifacts saved in build/contracts/")

if __name__ == "__main__":
    compile_contracts()
