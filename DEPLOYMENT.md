# 智能合约部署指南

本指南详细说明如何部署新的智能合约到Tura链上。

## 环境准备

1. 确保安装了必要的Python包：
```bash
poetry install
poetry add web3 py-solc-x python-dotenv
```

2. 安装Solidity编译器：
```bash
poetry run python install_solc.py
```

## 部署流程

### 1. 将合约文件放入contracts目录

- 将主合约文件（如 `YourContract.sol`）放入 `contracts/` 目录
- 如果合约依赖其他合约（如OpenZeppelin），确保所有依赖都已正确安装
- 确保合约的Solidity版本与配置匹配（当前使用0.8.20）

示例：
```bash
cp YourContract.sol contracts/
```

### 2. 编译合约

使用 `deploy_direct.py` 脚本编译和部署合约。该脚本会：
- 自动编译所有相关合约
- 处理合约之间的依赖关系
- 生成ABI和字节码

### 3. 部署合约

运行部署脚本：
```bash
poetry run python deploy_direct.py
```

部署脚本会：
- 连接到Tura链（http://43.135.26.222:8000）
- 使用提供的私钥签署交易
- 部署合约并等待确认
- 输出合约地址和交易哈希

### 4. 验证部署结果

使用 `verify_deployment.py` 脚本验证部署：
```bash
poetry run python verify_deployment.py
```

验证内容包括：
- 确认合约已成功部署
- 验证合约状态（管理员地址、最小质押额等）
- 确认部署账户权限

## 示例：AIAgentRegistryFactory合约

最新部署结果：
- 合约地址：0x00Bdaa6317e589b02414119434eED10220D4AF88
- 管理员地址：0x08Bb6eA809A2d6c13D57166Fa3ede48C0ae9a70e
- 最小质押额：1 TURA (1000000000000000000 wei)

## 注意事项

- 部署前确保有足够的TURA代币支付gas费
- 保管好私钥，不要泄露
- 建议先在测试网络测试后再部署到主网
- 记录每次部署的合约地址和参数
