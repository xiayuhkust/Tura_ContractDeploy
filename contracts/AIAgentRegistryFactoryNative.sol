// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./AIAgentNative.sol";

contract AIAgentRegistryFactoryNative is ReentrancyGuard {
    address public admin;
    uint256 public minimumStake;

    mapping(address => address) public agentContracts;
    mapping(address => string) public agentTypes;

    enum RegistrationType { AI_AGENT, WORKFLOW, MODEL, DATA_PROVIDER }

    event AgentContractDeployed(address indexed agent, address agentContractAddress, string agentType);

    constructor(uint256 minStake) {
        admin = msg.sender;
        minimumStake = minStake;
    }

    function registerAgent(RegistrationType regType) external payable nonReentrant {
        require(agentContracts[msg.sender] == address(0), "Agent already registered");
        require(msg.value >= minimumStake, "Stake amount below minimum");

        address newAgent;
        if (regType == RegistrationType.AI_AGENT) {
            AIAgent aiAgent = new AIAgent{value: msg.value}(msg.sender);
            newAgent = address(aiAgent);
        }

        agentContracts[msg.sender] = newAgent;
        agentTypes[msg.sender] = _getAgentTypeString(regType);

        emit AgentContractDeployed(msg.sender, newAgent, _getAgentTypeString(regType));
    }

    function setMinimumStake(uint256 newMinStake) external {
        require(msg.sender == admin, "Only admin can set the minimum stake");
        minimumStake = newMinStake;
    }

    function _getAgentTypeString(RegistrationType regType) internal pure returns (string memory) {
        if (regType == RegistrationType.AI_AGENT) {
            return "AI Agent";
        } else if (regType == RegistrationType.WORKFLOW) {
            return "Workflow";
        } else if (regType == RegistrationType.MODEL) {
            return "Model";
        } else if (regType == RegistrationType.DATA_PROVIDER) {
            return "DataProvider";
        }
        return "Unknown";
    }
}
