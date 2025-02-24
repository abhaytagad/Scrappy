import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from hindi_scraper.items import HindiScraperItem
import hashlib
from urllib.parse import urlparse, parse_qs, urlunparse
from w3lib.url import canonicalize_url
import langdetect


class HindiSpider(CrawlSpider):
    name = 'hindi_spider'
    
   

    allowed_domains  = [
    "aajtak.in",
    "amarujala.com",
    "bhaskar.com",
    "ndtv.in",
    "hindustantimes.com",
    "jagran.com",
    "navbharattimes.indiatimes.com",
    "zeenews.india.com",
    "abplive.com",
    "livehindustan.com",
    "prabhatkhabar.com",
    "patrika.com",
    "news18.com",
    
    "punjabkesari.in",
    "thewirehindi.com",
    "deshbandhu.co.in",
    "indiatoday.in",
    "satyahindi.com",
    "udayavani.com",
    
    "hindi.oneindia.com",
    "newsstate.com",
    "newsnationtv.com",
    "gaonconnection.com",
    "hindi.firstpost.com",
    "business-standard.com",
    "bbc.com",
    "voanews.com",
    "sputniknews.com",
    "theprint.in",
    "dw.com",
    "cnn.com",
    "swarajyamag.com",
    "outlookhindi.com"
]
    deny_domains = [
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "youtube.com",
    "linkedin.com",
    "pinterest.com",
    "tumblr.com",
    "reddit.com",
    "amazon.com",
    "flipkart.com",
    "ebay.com",
    "aliexpress.com",
    "ad.com",
    "ads.com",
    "doubleclick.net",
    "googleadservices.com",
    "adobe.com",
    "microsoft.com",
    "apple.com",
    "wikipedia.org",  # Exclude non-Hindi Wikipedia
    "github.com",
    "stackoverflow.com",
    "quora.com",
    "medium.com",
    "blogspot.com",
    "wordpress.com",
    "weebly.com",
    "wix.com",
    "godaddy.com",
    "cloudflare.com",
    "akamai.com",
    "cdn.com",
    "jsdelivr.net",
    "jquery.com",
    "bootstrap.com",
    "angularjs.org",
    "reactjs.org",
    "vuejs.org",
    "npmjs.com",
    "yarnpkg.com",
    "docker.com",
    "kubernetes.io",
    "aws.amazon.com",
    "azure.microsoft.com",
    "cloud.google.com",
    "oracle.com",
    "ibm.com",
    "salesforce.com",
    "zoho.com",
    "crm.com",
    "hubspot.com",
    "mailchimp.com",
    "paypal.com",
    "stripe.com",
    "squareup.com",
    "visa.com",
    "mastercard.com",
    "americanexpress.com",
    "discover.com",
    "bankofamerica.com",
    "wellsfargo.com",
    "chase.com",
    "citi.com",
    "capitalone.com",
    "schwab.com",
    "fidelity.com",
    "vanguard.com",
    "etrade.com",
    "robinhood.com",
    "coinbase.com",
    "binance.com",
    "kraken.com",
    "bitfinex.com",
    "gemini.com",
    "blockchain.com",
    "bitcoin.org",
    "ethereum.org",
    "ripple.com",
    "litecoin.org",
    "tether.to",
    "usdt.com",
    "usdc.com",
    "dai.com",
    "uniswap.org",
    "sushiswap.org",
    "pancakeswap.finance",
    "opensea.io",
    "rarible.com",
    "nft.com",
    "cryptopunks.com",
    "axieinfinity.com",
    "sandbox.game",
    "decentraland.org",
    "roblox.com",
    "minecraft.net",
    "fortnite.com",
    "epicgames.com",
    "steampowered.com",
    "origin.com",
    "uplay.com",
    "gog.com",
    "itch.io",
    "twitch.tv",
    "mixer.com",
    "dlive.tv",
    "trovo.live",
    "vimeo.com",
    "dailymotion.com",
    "vevo.com",
    "soundcloud.com",
    "spotify.com",
    "pandora.com",
    "iheart.com",
    "tidal.com",
    "deezer.com",
    "napster.com",
    "last.fm",
    "bandcamp.com",
    "reverbnation.com",
    "audiomack.com",
    "8tracks.com",
    "mixcloud.com",
    "jiosaavn.com",
    "gaana.com",
    "wynk.in",
    "hungama.com",
    "saavn.com",
    "spotify.com",
    "apple.com/music",
    "google.com/music",
    "youtube.com/music",
    "amazon.com/music",
    "pandora.com",
    "iheart.com",
    "tidal.com",
    "deezer.com",
    "napster.com",
    "last.fm",
    "bandcamp.com",
    "reverbnation.com",
    "audiomack.com",
    "8tracks.com",
    "mixcloud.com",
    "jiosaavn.com",
    "gaana.com",
    "wynk.in",
    "hungama.com",
    "saavn.com"
]

    start_urls = [
    "https://www.aajtak.in/",
    "https://www.amarujala.com/",
    "https://www.bhaskar.com/",
    "https://khabar.ndtv.com/",
    "https://www.hindustantimes.com/hindi/",
    "https://www.jagran.com/",
    "https://navbharattimes.indiatimes.com/",
    "https://zeenews.india.com/hindi",
    "https://www.abplive.com/",
    "https://www.livehindustan.com/",
    "https://www.prabhatkhabar.com/",
    "https://www.patrika.com/",
    "https://hindi.news18.com/",
   
    "https://www.punjabkesari.in/",
    "https://thewirehindi.com/",
    "https://www.deshbandhu.co.in/",
    "https://www.indiatoday.in/",
    "https://www.satyahindi.com/",
    "https://www.udayavani.com/hindi",
    "https://hindi.oneindia.com/",
    "https://www.newsstate.com/",
    "https://www.newsnationtv.com/",
    "https://www.gaonconnection.com/",
    "https://hindi.firstpost.com/",
    "https://www.business-standard.com/hindi/",
    "https://www.bbc.com/hindi",
    "https://www.voanews.com/hindi",
    "https://www.sputniknews.com/hindi/",
    "https://theprint.in/hindi",
    "https://www.dw.com/hi/",
    "https://www.cnn.com/hindi/",
    "https://www.swarajyamag.com/hindi",
    "https://www.outlookhindi.com/"
]


    # Set to track seen URLs and content hashes
    seen_urls = set()
    seen_content_hashes = set()

    # Define rules for crawling, following links, and parsing items
    rules = (
        Rule(LinkExtractor(allow=(),deny_domains=deny_domains ), callback='parse_item', follow=True, process_links='filter_links'),
    )

    def filter_links(self, links):
        """Filter out already seen URLs by canonicalizing them."""
        filtered_links = []
        for link in links:
            canonical_url = canonicalize_url(link.url)  # Better canonicalization
            if canonical_url not in self.seen_urls:
                self.seen_urls.add(canonical_url)
                filtered_links.append(link)
        return filtered_links

    def parse_item(self, response):
        """Extract Hindi text from the response and avoid duplicate content."""
        
        # Extract text from multiple HTML tags
        text_elements = response.css('p::text, div::text, span::text').getall()

        # Filter Hindi text using is_hindi_text method
        hindi_text_filtered = [text for text in text_elements if self.is_hindi_text(text)]

        # Combine the filtered Hindi text into a single string for content hashing
        combined_text = ''.join(hindi_text_filtered)
        content_hash = hashlib.md5(combined_text.encode('utf-8')).hexdigest()

        # Check if content is unique and if any Hindi text exists
        if content_hash not in self.seen_content_hashes and hindi_text_filtered:
            self.seen_content_hashes.add(content_hash)

            # Prepare the item to store the scraped data
            item = HindiScraperItem()
            item['url'] = response.url
            item['hindi_text'] = hindi_text_filtered
          
            yield  item

        else:
            self.logger.info(f"Duplicate content or no Hindi text found on: {response.url}")

    def is_hindi_text(self, text):
        """Check if the text contains common Hindi words and avoid Marathi."""
        if not text or not isinstance(text, str):  # Check if the text is valid
            return False
        # Common Hindi words (expand as needed)
        hindi_keywords = ['है', 'के', 'से', 'और', 'यह', 'पर', 'भी', 'जो', 'कर', 'रहा', 'भारत', 'विकास', 'समस्या']

        # Common Marathi words to exclude (expand as needed)
        marathi_keywords = ['आहे', 'मध्ये', 'साठी', 'तो', 'ती', 'होत', 'आणि', 'त्याचा', 'झाला', 'पण']
        # lang = detect(text)
            
        # Ensure text contains Hindi keywords and not Marathi keywords
        contains_hindi = any(word in text for word in hindi_keywords)
        contains_marathi = any(word in text for word in marathi_keywords)

        try:
            x = langdetect.detect(text)  # Just pass the text directly, no keyword argument
            return ((contains_hindi or (not contains_marathi)) and self.contains_devanagari(text)) and x == 'hi'
        except langdetect.lang_detect_exception.LangDetectException as e:
            return ((contains_hindi or (not contains_marathi)) and self.contains_devanagari(text))
    

    def contains_devanagari(self, text):
        """Check if the text contains Devanagari characters (common to Hindi and Marathi)."""
        return any('\u0900' <= char <= '\u097F' for char in text)
