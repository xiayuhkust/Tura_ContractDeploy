// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./AIAgent.sol";

contract AIAgentRegistryFactory is ReentrancyGuard {
    IERC20 public token;
    address public admin;
    uint256 public minimumStake;

    mapping(address => address) public agentContracts;
    mapping(address => string) public agentTypes;

    enum RegistrationType { AI_AGENT, WORKFLOW, MODEL, DATA_PROVIDER }

    event AgentContractDeployed(address indexed agent, address agentContractAddress, string agentType);

    constructor(address tokenAddress, uint256 minStake) {
        token = IERC20(tokenAddress);
        admin = msg.sender;
        minimumStake = minStake;
    }

    function registerAgent(uint256 stakeAmount, RegistrationType regType) external nonReentrant {
        require(agentContracts[msg.sender] == address(0), "Agent already registered");
        require(stakeAmount >= minimumStake, "Stake amount below minimum");
        require(token.transferFrom(msg.sender, address(this), stakeAmount), "Stake transfer failed");

        address newAgent;
        if (regType == RegistrationType.AI_AGENT) {
            AIAgent aiAgent = new AIAgent(msg.sender, address(token), stakeAmount);
            newAgent = address(aiAgent);
        }

        agentContracts[msg.sender] = newAgent;
        agentTypes[msg.sender] = _getAgentTypeString(regType);

        require(token.transfer(newAgent, stakeAmount), "Stake forwarding failed");

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
