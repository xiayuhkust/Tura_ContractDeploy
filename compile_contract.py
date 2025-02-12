from solcx import compile_source, compile_files
import json
import os

def compile_contract():
    print("Compiling StrategyAgent contract...")
    
    contracts_dir = "backend/app/real_agent_system/contracts"
    
    # Get absolute paths
    strategy_path = os.path.join(os.getcwd(), contracts_dir, "StrategyAgent.sol")
    
    # Set up allow_paths for imports
    node_modules_path = os.path.join(os.getcwd(), contracts_dir, "node_modules")
    contracts_path = os.path.join(os.getcwd(), contracts_dir)
    
    # Compile the contract with allow_paths
    compiled_sol = compile_files(
        [strategy_path],
        output_values=['abi', 'bin'],
        solc_version='0.8.20',
        allow_paths=[node_modules_path, contracts_path],
        import_remappings=[
            f"@openzeppelin/contracts={os.path.join(node_modules_path, '@openzeppelin/contracts')}",
            f"./={contracts_path}"
        ]
    )

    # Get contract interface
    contract_id, contract_interface = compiled_sol.popitem()
    
    # Save the compiled contract
    output = {
        'abi': contract_interface['abi'],
        'bytecode': contract_interface['bin']
    }
    
    with open('backend/app/real_agent_system/contracts/StrategyAgent.compiled.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("Compilation complete! Saved to StrategyAgent.compiled.json")

if __name__ == '__main__':
    compile_contract()
