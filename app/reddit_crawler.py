"""
Reddit Crawler for OSINT Framework
Crawls public Reddit data using PRAW (Reddit API)
"""

import praw
import os
from typing import Dict, List, Optional
from datetime import datetime
import logging
from app.entity_extractor import EntityExtractor
from app.database import store_crawled_data, store_entities

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedditCrawler:
    """Crawls Reddit for public user data using PRAW"""

    def __init__(self):
        """Initialize Reddit API connection using environment variables"""
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "OSINTFramework/1.0")

        if not all([self.client_id, self.client_secret]):
            raise ValueError(
                "Reddit API credentials not found. "
                "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables."
            )

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent
        )
        logger.info("Reddit API initialized")

    def get_user_data(self, username: str) -> Optional[Dict]:
        """
        Fetch public data for a Reddit user
        Returns dict with profile info, recent posts/comments
        """
        try:
            # Reddit API will raise exception if user doesn't exist/suspended
            user = self.reddit.redditor(username)

            # Test if user exists by trying to access an attribute
            _ = user.id

            # Get basic profile info
            profile_data = {
                'username': user.name,
                'id': user.id,
                'created_utc': user.created_utc,
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'is_employee': user.is_employee,
                'is_mod': user.is_mod,
                'has_verified_email': user.has_verified_email,
            }

            # Get recent posts (limit to 25 for reasonable demo)
            posts = []
            try:
                for submission in user.submissions.new(limit=25):
                    posts.append({
                        'id': submission.id,
                        'title': submission.title,
                        'selftext': submission.selftext,
                        'url': submission.url,
                        'subreddit': str(submission.subreddit),
                        'created_utc': submission.created_utc,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'permalink': submission.permalink
                    })
            except Exception as e:
                logger.warning(f"Could not fetch posts for {username}: {e}")

            # Get recent comments (limit to 25 for reasonable demo)
            comments = []
            try:
                for comment in user.comments.new(limit=25):
                    comments.append({
                        'id': comment.id,
                        'body': comment.body,
                        'subreddit': str(comment.subreddit),
                        'created_utc': comment.created_utc,
                        'score': comment.score,
                        'parent_id': comment.parent_id,
                        'permalink': comment.permalink
                    })
            except Exception as e:
                logger.warning(f"Could not fetch comments for {username}: {e}")

            return {
                'platform': 'reddit',
                'username': username,
                'profile': profile_data,
                'posts': posts,
                'comments': comments,
                'crawled_at': datetime.utcnow().isoformat(),
                'total_posts': len(posts),
                'total_comments': len(comments)
            }

        except Exception as e:
            logger.error(f"Error crawling user {username}: {e}")
            return None

    def extract_and_store_data(
        self,
        username: str,
        investigation_id: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Crawl a Reddit user, extract entities, and store everything
        Returns dict with counts of what was stored
        """
        logger.info(f"Starting crawl for u/{username}")

        # Crawl the user data
        raw_data = self.get_user_data(username)
        if not raw_data:
            logger.warning(f"No data returned for user {username}")
            return {"crawled": 0, "entities_stored": 0}

        # Store raw crawled data
        crawled_data_id = store_crawled_data(
            platform="reddit",
            source_identifier=username,
            raw_data=raw_data,
            investigation_id=investigation_id
        )
        logger.info(f"Stored crawled data with ID: {crawled_data_id}")

        # Extract entities from posts and comments
        extractor = EntityExtractor()
        all_posts = raw_data.get('posts', [])
        all_comments = raw_data.get('comments', [])

        # Combine posts and comments for entity extraction
        combined_text = ""

        for post in all_posts:
            combined_text += " " + post.get('title', '')
            combined_text += " " + post.get('selftext', '')

        for comment in all_comments:
            combined_text += " " + comment.get('body', '')

        # Extract entities
        entities_data = extractor.extract_entities(combined_text)

        # Also add the Reddit username itself as a username entity
        if username:
            if 'usernames' not in entities_data:
                entities_data['usernames'] = []
            entities_data['usernames'].append(username.lower())

        # Normalize URLs
        if 'urls' in entities_data:
            entities_data['urls'] = list(set([
                extractor.normalize_url(url) for url in entities_data['urls']
            ]))

        # Store entities
        entities_stored = store_entities(
            entities=entities_data,
            source_platform="reddit",
            source_identifier=username,
            crawled_data_id=crawled_data_id,
            investigation_id=investigation_id
        )

        logger.info(f"Stored {entities_stored} new entities for u/{username}")

        return {
            "crawled": 1,
            "entities_stored": entities_stored,
            "posts_crawled": len(all_posts),
            "comments_crawled": len(all_comments)
        }

    def get_user_mentions(self, username: str, limit: int = 100) -> List[str]:
        """
        Get recent mentions of a username in comments (basic implementation)
        Note: This is limited due to Reddit API restrictions
        """
        mentions = []
        try:
            # Search for comments containing the username
            # This is a simplified approach - in practice you'd want to use Reddit search
            # or monitor specific subreddits
            for comment in self.reddit.subreddit("all").comments(limit=limit):
                if f"u/{username}" in comment.body.lower() or f"/u/{username}" in comment.body.lower():
                    mentions.append(comment.author.name if comment.author else "[deleted]")
        except Exception as e:
            logger.warning(f"Could not search for mentions of {username}: {e}")

        return list(set(mentions))  # Remove duplicates


def demo_crawler():
    """Demo function to show crawler capabilities (requires credentials)"""
    print("🤖 Reddit Crawler Demo")
    print("=" * 30)
    print("NOTE: This demo requires Reddit API credentials")
    print("Set these environment variables:")
    print("  REDDIT_CLIENT_ID=your_client_id")
    print("  REDDIT_CLIENT_SECRET=your_client_secret")
    print("  REDDIT_USER_AGENT=OSINTFramework/1.0 by your_username")
    print()
    print("To get credentials:")
    print("1. Go to https://www.reddit.com/prefs/apps")
    print("2. Create a 'script' type app")
    print("3. Note the client ID and secret")
    print()

    # Show what the crawler would do
    print("🎯 What the crawler will do:")
    print("  • Fetch user profile info (karma, verification status, etc.)")
    print("  • Get recent posts (title, text, URL, subreddit, score)")
    print("  • Get recent comments (text, subreddit, score, parent)")
    print("  • Extract entities: usernames, emails, URLs, phones, hashtags, crypto")
    print("  • Store raw data and extracted entities in SQLite")
    print("  • Track provenance and timestamps")
    print()
    print("💡 For mid-term demo:")
    print("  • Crawl 2-3 easy targets (e.g., 'spez', 'kemitche')")
    print("  • Show extracted entities in your presentation")
    print("  • Demonstrate database stats and entity search")
    print("  • Explain how this enables cross-platform correlation")


if __name__ == "__main__":
    demo_crawler()