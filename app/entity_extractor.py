"""
Entity Extraction Module for OSINT Framework
Extracts and normalizes cyber-relevant entities from text
"""

import re
from typing import Dict, List
from datetime import datetime


class EntityExtractor:
    """Extracts entities using regex patterns"""

    @staticmethod
    def extract_entities(text: str) -> Dict[str, List[str]]:
        """
        Extract entities using regex patterns
        Returns dict of entity types to lists of values
        """
        if not text or not isinstance(text, str):
            return {
                'usernames': [],
                'emails': [],
                'urls': [],
                'phone_numbers': [],
                'hashtags': [],
                'crypto_addresses': []
            }

        entities = {
            'usernames': [],
            'emails': [],
            'urls': [],
            'phone_numbers': [],
            'hashtags': [],
            'crypto_addresses': []
        }

        # Username/handle patterns (alphanumeric + underscore, 3-30 chars)
        # Common words that aren't usernames
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can',
            'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
            'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who',
            'boy', 'did', 'man', 'men', 'put', 'too', 'use', 'reddit', 'comment',
            'post', 'submit', 'text', 'link', 'url', 'http', 'www', 'com', 'org',
            'net', 'info', 'edu', 'gov', 'mil', 'int', 'jobs', ' Mob', 'web',
            'api', 'data', 'file', 'image', 'video', 'photo', 'blog', 'forum'
        }

        username_pattern = r'\b[A-Za-z0-9_]{3,30}\b'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+[^\s<>"{}|\\^`\[\]]'
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        hashtag_pattern = r'#([A-Za-z0-9_]+)'
        btc_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
        eth_pattern = r'\b0x[a-fA-F0-9]{40}\b'

        # Extract entities
        usernames = re.findall(username_pattern, text)
        emails = re.findall(email_pattern, text)
        urls = re.findall(url_pattern, text)
        phones = re.findall(phone_pattern, text)
        hashtags = re.findall(hashtag_pattern, text)
        crypto_btc = re.findall(btc_pattern, text)
        crypto_eth = re.findall(eth_pattern, text)

        # Filter and normalize usernames
        filtered_usernames = []
        for username in usernames:
            username_lower = username.lower()
            if (username_lower not in common_words and
                not username.isdigit() and
                len(username) >= 3):
                filtered_usernames.append(EntityExtractor.normalize_username(username))

        entities['usernames'] = list(set(filtered_usernames))
        entities['emails'] = list(set(emails))
        entities['urls'] = list(set([EntityExtractor.normalize_url(url) for url in urls]))
        entities['phone_numbers'] = list(set(phones))
        entities['hashtags'] = list(set(hashtags))
        entities['crypto_addresses'] = list(set(crypto_btc + crypto_eth))

        return entities

    @staticmethod
    def normalize_username(username: str) -> str:
        """Normalize username for comparison"""
        return username.lower().strip()

    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL for comparison"""
        # Remove trailing slash, convert to lowercase, remove tracking params
        url = url.lower().rstrip('/')
        # Remove common tracking parameters
        if '?' in url:
            base_url = url.split('?')[0]
            # Only keep if base_url looks like a real domain
            if len(base_url) > len(url) * 0.5:  # Don't strip too much
                url = base_url
        return url

    @staticmethod
    def extract_from_reddit_posts(posts_data: List[Dict]) -> Dict[str, List[str]]:
        """
        Extract entities specifically from Reddit posts/comments
        """
        combined_text = ""

        for post in posts_data:
            # Add title and selftext
            combined_text += " " + post.get('title', '')
            combined_text += " " + post.get('selftext', '')

        # Also extract from comments if available
        # This would be called with comments data separately

        return EntityExtractor.extract_entities(combined_text)


def demo_extraction():
    """Demo function to show entity extraction capabilities"""
    sample_text = """
    Check out this cool project by @spez on Reddit!
    Visit https://github.com/osint-framework for more info.
    Contact us at contact@osint-framework.com or call +1-555-123-4567.
    Follow #OSINT and #CyberSecurity trends.
    Bitcoin donations accepted: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
    Ethereum wallet: 0x742d35Cc6634C0532925a3b8D4C0532950532950
    """

    extractor = EntityExtractor()
    entities = extractor.extract_entities(sample_text)

    print("🔍 Entity Extraction Demo")
    print("=" * 40)
    for entity_type, values in entities.items():
        if values:
            print(f"{entity_type.upper()}: {', '.join(values[:5])}")
            if len(values) > 5:
                print(f"  ... and {len(values) - 5} more")

    return entities


if __name__ == "__main__":
    demo_extraction()