# Tor-Scraper
A containerized scraping platform written in python. The platform extends a UI over the web, and allows scraping over TOR. 


## Project Structure
the project builds into a unique docker image which has a few moving parts:
1. scrapyd - a scrapy daemon. For more information, go to the [scrapy page](https://github.com/scrapy/scrapy) and the [scrapyd page](https://github.com/scrapy/scrapyd). 
2. scrapydweb - a web UI for scrapyd. For more information go to the [scrapydweb page](https://github.com/my8100/scrapydweb). 
3. privoxy - a proxy used to catch the requests and pack them into a SOCKS5 tunnel for easier TOR network integration. 
4. TOR stem - the TOR stem controller for the container. Used to access the TOR network, change circuits and bridges.

## Spiders
Spiders are used to access the remote website host. They utilize the scrapy package  to make requests to the website, and can parse the response. 

An example spider is given in the code. 

## Middleware
Middleware is the conponent that sits right after a request is bound to leave the machine and right before the response gets back to the spider. 

The middleware does network adjustments to the request. In this instance, the TorMiddleware is used to make the requests go through TOR. The TorMiddleware is automatically added to each spider. This feature can be disabled for individual spiders or altogether. 

### TorMiddleware
The TorMiddleware is used to pass requests to the TOR network over a SOCKS5 proxy. The behavior of the request can be changed. As of now, a circuit is changed only when a request fails with code 403. The bridge is configured on image build and can be changed in runtiume if needed via the TOR stem. 

## Pipelines
After a request returns, the parsed ItemAdapter is passed to the configured pipeline. An example DebugPipeline which logs the response is implemented and configured to the example spider. 
The pipeline can be used to make requests to your backend API, to save the formulized data in a DB or to do with the data whatever you want. 