"""Network connectivity diagnostic tool"""
import requests
import socket
from web3 import Web3
import urllib3

# Disable SSL warnings for corporate networks
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_basic_internet():
    """Test basic internet connectivity"""
    print("Testing basic internet connectivity...")
    try:
        response = requests.get('https://www.google.com', timeout=5, verify=False)
        print(f"✓ Internet works (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"✗ Internet connection failed: {e}")
        return False

def test_rpc_endpoints():
    """Test multiple RPC endpoints"""
    print("\nTesting Polygon RPC endpoints...")
    
    endpoints = [
        'https://rpc.ankr.com/polygon',
        'https://polygon-mainnet.g.alchemy.com/v2/demo',
        'https://polygon-mainnet.public.blastapi.io',
        'https://polygon.llamarpc.com',
        'https://rpc-mainnet.maticvigil.com',
        'https://polygon-rpc.com',
    ]
    
    working = []
    for endpoint in endpoints:
        try:
            # Create session without SSL verification for corporate networks
            session = requests.Session()
            session.verify = False
            
            w3 = Web3(Web3.HTTPProvider(
                endpoint,
                request_kwargs={'timeout': 10},
                session=session
            ))
            
            # Try to get block number to test connection
            try:
                block = w3.eth.block_number
                print(f"✓ {endpoint} - WORKS (Block: {block})")
                working.append(endpoint)
            except Exception as conn_err:
                print(f"✗ {endpoint} - Connection test failed: {str(conn_err)[:80]}")
                
        except Exception as e:
            print(f"✗ {endpoint} - Setup error: {str(e)[:80]}")
    
    return working

def test_dns():
    """Test DNS resolution"""
    print("\nTesting DNS resolution...")
    
    domains = [
        'rpc.ankr.com',
        'polygon-rpc.com',
        'polygon-mainnet.g.alchemy.com'
    ]
    
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            print(f"✓ {domain} → {ip}")
        except Exception as e:
            print(f"✗ {domain} - DNS failed: {e}")

def test_https_post():
    """Test HTTPS POST to RPC"""
    print("\nTesting HTTPS POST to RPC...")
    
    endpoints = [
        'https://rpc.ankr.com/polygon',
        'https://polygon-mainnet.g.alchemy.com/v2/demo',
    ]
    
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    
    for endpoint in endpoints:
        try:
            response = requests.post(endpoint, json=payload, timeout=10, verify=False)
            print(f"✓ {endpoint}")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.json()}")
            return True
        except Exception as e:
            print(f"✗ {endpoint} - Error: {str(e)[:80]}")
    
    return False

def test_proxy():
    """Check if proxy is needed"""
    print("\nChecking proxy configuration...")
    import os
    
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    
    if http_proxy or https_proxy:
        print(f"HTTP_PROXY: {http_proxy or 'Not set'}")
        print(f"HTTPS_PROXY: {https_proxy or 'Not set'}")
    else:
        print("No proxy environment variables set")
        print("If your network requires a proxy, you may need to set these")

def main():
    print("="*70)
    print("NETWORK DIAGNOSTIC TOOL")
    print("="*70)
    print()
    
    # Run tests
    internet_ok = test_basic_internet()
    test_dns()
    test_proxy()
    
    if internet_ok:
        working = test_rpc_endpoints()
        test_https_post()
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        if working:
            print(f"\n✓ Found {len(working)} working RPC endpoint(s):")
            for endpoint in working:
                print(f"  - {endpoint}")
            print("\nRECOMMENDATION:")
            print(f"Update .env file:")
            print(f"POLYGON_RPC_URL={working[0]}")
        else:
            print("\n✗ No working RPC endpoints found")
            print("\nPOSSIBLE CAUSES:")
            print("1. Corporate firewall blocking blockchain RPC endpoints")
            print("2. Need to configure proxy settings")
            print("3. VPN required for external access")
            print("\nRECOMMENDED ACTIONS:")
            print("1. Contact IT to allow blockchain RPC access")
            print("2. Try running from home/mobile hotspot")
            print("3. Use VPN that allows blockchain access")
            print("4. Deploy bot on external VPS instead")
    else:
        print("\n✗ Basic internet connectivity failed")
        print("Check your network connection")

if __name__ == "__main__":
    main()
