from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

def transfer_tura():
    """Transfer TURA tokens to test address."""
    # Initialize Web3 with new RPC URL
    w3 = Web3(Web3.HTTPProvider("https://rpc-beta1.turablockchain.com"))
    
    # Set up accounts
    sender_private_key = "8f739492aa27c83ce43a575dd3f9fba6dad7342e9bfd10b593116fb26566ad13"
    sender_account = Account.from_key(sender_private_key)
    recipient = "0x08Bb6eA809A2d6c13D57166Fa3ede48C0ae9a70e"
    
    # Amount to transfer (3000 TURA)
    amount = w3.to_wei(3000, 'ether')
    
    print(f"Sender address: {sender_account.address}")
    print(f"Recipient address: {recipient}")
    print(f"Amount to transfer: {w3.from_wei(amount, 'ether')} TURA")
    
    # Check sender balance
    balance = w3.eth.get_balance(sender_account.address)
    print(f"Sender balance: {w3.from_wei(balance, 'ether')} TURA")
    
    if balance < amount:
        raise Exception(f"Insufficient balance. Need {w3.from_wei(amount, 'ether')} TURA but only have {w3.from_wei(balance, 'ether')} TURA")
    
    # Build transaction
    nonce = w3.eth.get_transaction_count(sender_account.address)
    transaction = {
        'nonce': nonce,
        'to': recipient,
        'value': amount,
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 1337  # TURA testnet chain ID
    }
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, sender_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Transaction hash: {tx_hash.hex()}")
    
    # Wait for transaction receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction status: {'Success' if receipt['status'] == 1 else 'Failed'}")
    
    # Verify final balances
    new_recipient_balance = w3.eth.get_balance(recipient)
    print(f"Recipient new balance: {w3.from_wei(new_recipient_balance, 'ether')} TURA")

if __name__ == "__main__":
    transfer_tura()
