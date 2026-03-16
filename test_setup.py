"""Test script to verify bot setup and configuration"""
import sys
import os
from colorama import Fore, Style, init

init(autoreset=True)

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_warning(text):
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def test_python_version():
    """Test Python version"""
    print_header("Testing Python Version")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} (Required: 3.9+)")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} (Required: 3.9+)")
        return False

def test_dependencies():
    """Test if all dependencies are installed"""
    print_header("Testing Dependencies")
    
    required_packages = [
        'py_clob_client',
        'web3',
        'dotenv',
        'requests',
        'websockets',
        'matplotlib',
        'pandas',
        'aiohttp',
        'colorama',
        'tabulate'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} NOT installed")
            all_installed = False
            
    if not all_installed:
        print_warning("\nInstall missing packages with: pip install -r requirements.txt")
        
    return all_installed

def test_env_file():
    """Test if .env file exists and has required values"""
    print_header("Testing Environment Configuration")
    
    if not os.path.exists('.env'):
        print_error(".env file not found")
        print_warning("Copy .env.example to .env: cp .env.example .env")
        return False
        
    print_success(".env file exists")
    
    # Try to load config
    try:
        from config import Config
        
        # Check required settings
        if not Config.PRIVATE_KEY or Config.PRIVATE_KEY == 'your_ethereum_private_key_here':
            print_error("PRIVATE_KEY not set in .env")
            print_warning("Add your Ethereum private key to .env file")
            return False
        else:
            # Mask private key for display
            masked_key = Config.PRIVATE_KEY[:6] + '...' + Config.PRIVATE_KEY[-4:]
            print_success(f"PRIVATE_KEY configured ({masked_key})")
            
        print_success(f"Polygon RPC: {Config.POLYGON_RPC_URL}")
        print_success(f"Max position size: {Config.MAX_POSITION_SIZE_PCT}%")
        print_success(f"Min probability: {Config.MIN_PROBABILITY_THRESHOLD}%")
        print_success(f"Time threshold: {Config.TIME_TO_CLOSE_THRESHOLD_MINUTES} minutes")
        
        return True
        
    except Exception as e:
        print_error(f"Error loading config: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print_header("Testing Directory Structure")
    
    required_dirs = ['data', 'logs']
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print_success(f"Created {dir_name}/ directory")
        else:
            print_success(f"{dir_name}/ directory exists")
            
    return True

def test_wallet_connection():
    """Test connection to Ethereum wallet"""
    print_header("Testing Wallet Connection")
    
    try:
        from web3 import Web3
        from config import Config
        import urllib3
        
        # Disable SSL warnings for corporate networks
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Connect to Polygon RPC with SSL verification disabled for corporate networks
        session = __import__('requests').Session()
        session.verify = False  # Disable SSL verification for corporate proxy
        
        w3 = Web3(Web3.HTTPProvider(
            Config.POLYGON_RPC_URL,
            request_kwargs={'timeout': 60},
            session=session
        ))
        
        if not w3.is_connected():
            print_error(f"Cannot connect to Polygon RPC: {Config.POLYGON_RPC_URL}")
            return False
            
        print_success("Connected to Polygon network")
        
        # Get account from private key
        account = w3.eth.account.from_key(Config.PRIVATE_KEY)
        print_success(f"Wallet address: {account.address}")
        
        # Get balance
        balance = w3.eth.get_balance(account.address)
        matic_balance = w3.from_wei(balance, 'ether')
        print_success(f"MATIC balance: {matic_balance:.4f} MATIC")
        
        if matic_balance < 0.01:
            print_warning("Low MATIC balance - you need MATIC for gas fees")
            print_warning("Get MATIC from a faucet or exchange")
        
        # Try to get USDC balance (if USDC contract available)
        try:
            # Native USDC contract on Polygon (the one most exchanges use)
            usdc_address = '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359'
            usdc_abi = [{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]
            
            usdc_contract = w3.eth.contract(address=Web3.to_checksum_address(usdc_address), abi=usdc_abi)
            usdc_balance = usdc_contract.functions.balanceOf(account.address).call()
            usdc_decimals = usdc_contract.functions.decimals().call()
            usdc_balance = usdc_balance / (10 ** usdc_decimals)
            
            print_success(f"USDC balance: {usdc_balance:.2f} USDC")
            
            if usdc_balance < Config.MIN_BALANCE_USDC:
                print_warning(f"USDC balance below minimum ({Config.MIN_BALANCE_USDC} USDC)")
                print_warning("Fund your wallet with USDC on Polygon network")
            
        except Exception as e:
            print_warning(f"Could not fetch USDC balance: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Wallet connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print(f"{Fore.MAGENTA}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     POLYMARKET SNIPER BOT - SETUP VERIFICATION TEST      ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Environment Config", test_env_file),
        ("Directory Structure", test_directories),
        ("Wallet Connection", test_wallet_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Fore.CYAN}{'='*60}")
    if passed == total:
        print(f"{Fore.GREEN}All tests passed! ({passed}/{total})")
        print(f"{Fore.GREEN}✓ Bot is ready to run!")
        print(f"{Fore.CYAN}\nStart the bot with: {Fore.WHITE}python run.py")
    else:
        print(f"{Fore.YELLOW}Some tests failed ({passed}/{total})")
        print(f"{Fore.YELLOW}Please fix the issues above before running the bot")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
