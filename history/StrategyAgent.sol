// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./interfaces/IGenericAgent.sol";
import "./interfaces/IEdgeValidation.sol";

contract StrategyAgent is IGenericAgent {
    address public owner;
    address public multiSigAddr;
    address public edgeValidationAddr;
    uint256 public immutable FEE_PER_ANALYSIS; // Set during deployment
    IERC20 public turaToken;

    struct Order {
        string action;
        string symbol;
        uint256 amount;
        string orderType;
    }

    event StrategyAnalyzed(
        address indexed caller,
        bytes32 indexed edgeId,
        bool executed,
        uint256 timestamp
    );

    event OrderGenerated(
        address indexed caller,
        bytes32 indexed edgeId,
        string action,
        string symbol,
        uint256 amount,
        string orderType,
        uint256 timestamp
    );

    string public tradingSymbol;  // Trading symbol set during initialization
    string public tradingPair;    // Trading pair set during initialization
    uint256 public immutable CHAIN_ID; // Network chain ID

    event ContractInitialized(
        address indexed owner,
        address indexed multiSigAddr,
        address indexed turaToken
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Unauthorized");
        _;
    }

    function setMultiSigAddress(address _multiSigAddr) external onlyOwner {
        multiSigAddr = _multiSigAddr;
    }
    
    constructor(
        address _owner,
        address[] memory _multiSigAddrs,
        uint256 _feePerAnalysis,
        address _tokenAddress,
        string memory _tradingSymbol,
        string memory _tradingPair,
        uint256 _chainId,
        address _edgeValidationAddr
    ) {
        require(_owner != address(0), "Invalid configuration");
        require(_multiSigAddrs.length > 0, "Invalid configuration");
        require(_multiSigAddrs[0] != address(0), "Invalid configuration");
        require(_feePerAnalysis > 0, "Invalid configuration");
        require(_tokenAddress != address(0), "Invalid configuration");
        require(bytes(_tradingSymbol).length > 0, "Invalid configuration");
        require(bytes(_tradingPair).length > 0, "Invalid configuration");
        require(_chainId > 0, "Invalid configuration");
        require(_edgeValidationAddr != address(0), "Invalid EdgeValidation address");
        
        owner = _owner;
        multiSigAddr = _multiSigAddrs[0];
        FEE_PER_ANALYSIS = _feePerAnalysis;
        turaToken = IERC20(_tokenAddress);
        tradingSymbol = _tradingSymbol;
        tradingPair = _tradingPair;
        CHAIN_ID = _chainId;
        edgeValidationAddr = _edgeValidationAddr;

        // Emit initialization event
        emit ContractInitialized(owner, multiSigAddr, address(turaToken));
    }

    function analyzeMarketData(bytes32 edgeId) external payable returns (Order memory) {
        // Validate caller, input and edge validation contract
        require(msg.sender != address(0), "Unauthorized caller");
        require(edgeId != bytes32(0), "Invalid edge ID");
        require(edgeValidationAddr != address(0), "EdgeValidation not set");
        
        // Get validated data from EdgeValidation
        require(IEdgeValidation(edgeValidationAddr).isEdgeProcessed(edgeId), "Edge not processed");
        bytes memory validatedData = IEdgeValidation(edgeValidationAddr).getValidatedData(edgeId);
        require(validatedData.length > 0, "No validated data");
        
        // Decode market data from validated data
        uint256 marketData = abi.decode(validatedData, (uint256));
        
        // Validate contract state and payment
        require(owner != address(0), "Contract not initialized");
        require(multiSigAddr != address(0), "MultiSig not set");
        require(msg.value == FEE_PER_ANALYSIS, "Incorrect fee amount");
        
        // Transfer fee to multisig address
        (bool success, ) = payable(multiSigAddr).call{value: msg.value}("");
        require(success, "Transaction failed");
        
        // Emit fee transfer event
        emit FeeTransferred(msg.sender, multiSigAddr, msg.value);

        // Initialize order with default values
        Order memory order = Order({
            action: "hold",
            symbol: tradingSymbol,
            amount: 0,
            orderType: "NO_ACTION"
        });

        // Strategy implementation to be added during deployment
        // This ensures trading strategy remains private and secure
        // Each deployment should implement its own validateAndExecuteStrategy function
        bool shouldExecute = validateAndExecuteStrategy(marketData);
        
        // Execute order if strategy conditions are met
        if (shouldExecute) {
            order.action = "buy";
            order.amount = msg.value;
            order.orderType = string(abi.encodePacked(tradingPair));
        }
        
        emit StrategyAnalyzed(
            msg.sender,
            edgeId,
            shouldExecute,
            block.timestamp
        );

        // Emit order generated event if it's a buy order
        if (shouldExecute) {
            emit OrderGenerated(
                msg.sender,
                edgeId,
                order.action,
                order.symbol,
                order.amount,
                order.orderType,
                block.timestamp
            );
        }

        return order;
    }

    // Allow withdrawal of collected fees
    function withdrawFees(address payable to, uint256 amount) external onlyOwner {
        require(to != address(0), "Invalid recipient");
        require(amount > 0, "Invalid amount");
        require(
            address(this).balance >= amount,
            "Insufficient balance"
        );
        (bool success, ) = to.call{value: amount}("");
        require(success, "Fee transfer failed");
        emit FeesWithdrawn(msg.sender, to, amount);
    }
    
    // Events for fee tracking
    event FeesWithdrawn(address indexed owner, address indexed to, uint256 amount);
    event FeeReceived(address indexed from, uint256 amount);
    event FeeTransferred(address indexed from, address indexed to, uint256 amount);
    
    // Allow contract to receive native tokens
    receive() external payable {
        emit FeeReceived(msg.sender, msg.value);
    }

    // Implementation of the strategy to check market data last digit
    function validateAndExecuteStrategy(uint256 marketData) internal returns (bool) {
        require(marketData > 0, "Invalid market data");

        // Get the last digit of the market data
        uint256 lastDigit = marketData % 10;

        // Return true (execute trade) if last digit is odd
        return lastDigit % 2 == 1;
    }

    // Events for data reception
    event DataReceived(
        address indexed source,
        bytes32 indexed edgeId,
        uint256 marketData,
        bool success,
        uint256 timestamp
    );

    /**
     * @dev Implementation of IGenericAgent.receiveData
     * Receives and processes validated data from EdgeValidation
     */
    function receiveData(bytes32 edgeId, bytes calldata data) external override returns (bool) {
        // Validate caller is EdgeValidation contract
        require(msg.sender == edgeValidationAddr, "Unauthorized caller");
        require(edgeId != bytes32(0), "Invalid edge ID");
        require(data.length > 0, "Empty data");
        
        // Decode market data
        uint256 marketData = abi.decode(data, (uint256));
        require(marketData > 0, "Invalid market data");
        
        // Process the data through strategy
        bool result = validateAndExecuteStrategy(marketData);
        
        emit DataReceived(
            msg.sender,
            edgeId,
            marketData,
            result,
            block.timestamp
        );
        
        return result;
    }
}
