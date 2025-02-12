// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract AIAgent is ReentrancyGuard {
    address public owner;
    uint256 public stakedAmount;

    constructor(address _owner) payable {
        owner = _owner;
        stakedAmount = msg.value;
    }

    function withdraw() external nonReentrant {
        require(msg.sender == owner, "Only owner can withdraw");
        uint256 balance = address(this).balance;
        (bool success, ) = owner.call{value: balance}("");
        require(success, "Transfer failed");
        stakedAmount = 0;
    }

    // Allow contract to receive native tokens
    receive() external payable {}
}
