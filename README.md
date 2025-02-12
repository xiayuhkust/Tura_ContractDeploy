使用方法：

# 1. 编译合约
poetry run python compile_contracts.py

# 2. 部署工厂合约
poetry run python deploy_template.py
# 部署后会输出合约地址

# 3. 注册代理
poetry run python register_template.py <工厂合约地址>

# 4. 验证注册
poetry run python verify_template.py <工厂合约地址> <您的地址>
