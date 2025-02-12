// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract AIAgent is ReentrancyGuard {
    IERC20 public token;
    address public owner;
    uint256 public stakedAmount;

    constructor(address _owner, address _token, uint256 _stakeAmount) {
        owner = _owner;
        token = IERC20(_token);
        stakedAmount = _stakeAmount;
    }

    function withdraw() external nonReentrant {
        require(msg.sender == owner, "Only owner can withdraw");
        uint256 balance = token.balanceOf(address(this));
        require(token.transfer(owner, balance), "Transfer failed");
        stakedAmount = 0;
    }
}
