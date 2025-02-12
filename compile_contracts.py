from solcx import compile_standard
import json
import os

def compile_contracts():
    print("Compiling contracts...")
    
    # Read contract sources
    with open('contracts/AIAgentNative.sol', 'r') as f:
        agent_source = f.read()
    with open('contracts/AIAgentRegistryFactoryNative.sol', 'r') as f:
        registry_source = f.read()
    
    # Create build directory if it doesn't exist
    os.makedirs('build/contracts', exist_ok=True)
    
    # Compile contracts
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "AIAgentNative.sol": {"content": agent_source},
            "AIAgentRegistryFactoryNative.sol": {"content": registry_source}
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
    with open('build/contracts/AIAgentRegistryFactoryNative.json', 'w') as f:
        contract_data = compiled_sol['contracts']['AIAgentRegistryFactoryNative.sol']['AIAgentRegistryFactoryNative']
        contract_data['bytecode'] = contract_data['evm']['bytecode']['object']
        json.dump(contract_data, f, indent=2)
    
    with open('build/contracts/AIAgentNative.json', 'w') as f:
        contract_data = compiled_sol['contracts']['AIAgentNative.sol']['AIAgent']
        contract_data['bytecode'] = contract_data['evm']['bytecode']['object']
        json.dump(contract_data, f, indent=2)
    
    print("Compilation complete! Contract artifacts saved in build/contracts/")

if __name__ == "__main__":
    compile_contracts()
