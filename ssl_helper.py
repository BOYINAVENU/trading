"""SSL/TLS helper for corporate networks with SSL-intercepting proxies"""
import ssl
import urllib3
from config import Config

def setup_ssl_context():
    """
    Setup SSL context for corporate networks
    Disables SSL verification if configured
    """
    if Config.DISABLE_SSL_VERIFICATION:
        # Disable SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print("⚠️  SSL verification disabled for corporate network compatibility")
        return False
    return True

def get_requests_session():
    """
    Get requests session with appropriate SSL settings
    """
    import requests
    session = requests.Session()
    
    if Config.DISABLE_SSL_VERIFICATION:
        session.verify = False
        # Disable SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    return session

def get_aiohttp_connector():
    """
    Get aiohttp connector with appropriate SSL settings
    """
    import aiohttp
    
    if Config.DISABLE_SSL_VERIFICATION:
        return aiohttp.TCPConnector(ssl=False)
    return None
