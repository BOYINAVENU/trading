"""Check config.json RPC connection"""
from web3 import Web3
import json

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

rpc_url = config['network']['rpc_url']

print("=" * 60)
print("CHECKING CONFIG.JSON RPC CONNECTION")
print("=" * 60)
print(f"\nRPC URL: {rpc_url}")

# Test connection
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
    block = w3.eth.block_number
    print(f"\n[OK] Connected successfully!")
    print(f"Current block: {block}")
    print(f"\nYour config.json RPC is WORKING!")
else:
    print(f"\n[ERROR] Cannot connect!")
    print(f"\nYour config.json RPC is NOT WORKING!")
    print(f"\nCheck your config.json and make sure rpc_url is correct")
