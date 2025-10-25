from random import choice

from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from stem.util.log import get_logger

# Constants
PRIVOXY_URL = 'http://127.0.0.1:8118'

def _get_user_agent():
    """Get a random user agent string"""
    ua = UserAgent(fallback='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36')
    return choice([ua.chrome, ua.firefox, ua.safari, ua.google])  # noqa: S311

def _set_new_ip(spider):
    """Request a new Tor circuit and verify IP change"""
    logger = get_logger()
    logger.propagate = False

    with Controller.from_port(port=9051) as controller: # type: ignore

        # Authenticate with the controller
        controller.authenticate(password=spider.settings.get('TOR_CONTROL_PASSWORD'))

        # Close existing circuits
        for circ in controller.get_circuits():
            controller.close_circuit(circ.id)

        # Send NEWNYM signal to switch identity
        controller.signal(Signal.NEWNYM) # type: ignore

    return True

class TorProxyMiddleware:
    def process_request(self, request, spider):
        """Process each request through the proxy"""
        if spider.name in ['Yad2SaleSpider', 'GovTrends']:
            # Skip processing for GovDeals spider
            return

        # Use Privoxy as HTTP proxy
        request.meta['proxy'] = PRIVOXY_URL
        request.headers['User-Agent'] = _get_user_agent()

    def process_response(self, request, response, spider):
        """Handle 403 responses by rotating proxy and retrying"""
        if spider.name in ['Yad2SaleSpider', 'GovTrends']:
            # Skip processing for GovDeals spider
            return response

        if response.status == 403:

            spider.logger.warning(f"403 Forbidden on {request.url}. Rotating proxy and retrying...")

            _set_new_ip(spider)  # Rotate proxy

            # Retry the same request with a new proxy
            retry_request = request.copy()

            retry_request.meta['proxy'] = PRIVOXY_URL
            retry_request.headers['User-Agent'] = _get_user_agent()
            return retry_request

        if response.status == 502:
            retry_request = request.copy()

            retry_request.meta['proxy'] = PRIVOXY_URL
            retry_request.headers['User-Agent'] = _get_user_agent()
            return retry_request

        return response
