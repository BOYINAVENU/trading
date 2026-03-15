"""Simple RPC connection test"""
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_rpc_direct():
    """Test RPC with direct HTTP POST"""
    endpoints = [
        'https://rpc.ankr.com/polygon',
        'https://polygon-mainnet.g.alchemy.com/v2/demo',
        'https://polygon-mainnet.public.blastapi.io',
    ]
    
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    
    print("Testing RPC endpoints with direct HTTP POST...")
    print("="*70)
    
    for endpoint in endpoints:
        try:
            print(f"\nTesting: {endpoint}")
            response = requests.post(
                endpoint, 
                json=payload, 
                timeout=10, 
                verify=False  # Disable SSL verification
            )
            
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data:
                    # Convert hex block number to decimal
                    block_hex = data['result']
                    block_num = int(block_hex, 16)
                    print(f"  ✓ SUCCESS - Current block: {block_num}")
                else:
                    print(f"  ✗ Unexpected response: {data}")
            else:
                print(f"  ✗ HTTP error: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print(f"  ✗ Timeout after 10 seconds")
        except requests.exceptions.ConnectionError as e:
            print(f"  ✗ Connection error: {str(e)[:100]}")
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:100]}")
    
    print("\n" + "="*70)

def test_with_web3():
    """Test with Web3.py"""
    from web3 import Web3
    
    endpoints = [
        'https://rpc.ankr.com/polygon',
        'https://polygon-mainnet.g.alchemy.com/v2/demo',
    ]
    
    print("\nTesting RPC endpoints with Web3.py...")
    print("="*70)
    
    for endpoint in endpoints:
        try:
            print(f"\nTesting: {endpoint}")
            
            # Create session without SSL verification
            session = requests.Session()
            session.verify = False
            
            # Create Web3 instance
            w3 = Web3(Web3.HTTPProvider(
                endpoint,
                request_kwargs={'timeout': 10},
                session=session
            ))
            
            # Try to get block number
            block = w3.eth.block_number
            print(f"  ✓ SUCCESS - Current block: {block}")
            
            # Try to get chain ID
            chain_id = w3.eth.chain_id
            print(f"  Chain ID: {chain_id} (should be 137 for Polygon)")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:150]}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SIMPLE RPC CONNECTION TEST")
    print("="*70)
    
    # Test with direct requests first
    test_rpc_direct()
    
    # Then test with Web3.py
    test_with_web3()
    
    print("\nDONE!")
