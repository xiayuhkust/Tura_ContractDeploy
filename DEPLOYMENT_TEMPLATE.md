# Native Token Staking Deployment Record Template

## Environment Setup
1. Copy `.env.example` to `.env`
2. Configure environment variables:
   - `TURA_RPC_URL`: Your TURA chain RPC endpoint
   - `TURA_PRIVATE_KEY`: Deployer's private key
   - `TURA_CHAIN_ID`: Chain ID (default: 1337)

## Contract Deployment
```bash
# Install dependencies
poetry install

# Compile contracts
poetry run python compile_contracts.py

# Deploy factory contract
poetry run python deploy_template.py
```

## Contract Features
1. Native Token Support
   - Direct TURA token staking
   - No wrapping required
   - Payable functions for native token handling

2. Security Measures
   - ReentrancyGuard implementation
   - Proper stake validation
   - Secure withdrawal mechanism
   - Access controls for admin functions

3. Agent Management
   - Unique agent registration
   - Type tracking
   - Stake amount tracking
   - Event emission for transparency

## Deployment Checklist
- [ ] Environment variables configured
- [ ] Contracts compiled successfully
- [ ] Factory contract deployed
- [ ] Minimum stake amount set
- [ ] Test registration completed
- [ ] Stake amount verified
- [ ] Events verified

## Security Notes
- Keep private keys secure and never commit them
- Use environment variables for sensitive data
- Verify contract addresses before interaction
- Always test with small amounts first
