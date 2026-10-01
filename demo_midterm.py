"""
Mid-Term Demo Script for OSINT Framework
Demonstrates Reddit crawler + entity extraction capabilities
"""

import os
import sys
import json
from datetime import datetime

# Add the app directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.reddit_crawler import RedditCrawler, demo_crawler
from app.entity_extractor import EntityExtractor, demo_extraction
from app.database import (
    create_tables, get_connection, store_crawled_data,
    store_entities, get_investigation_stats, search_entities
)
from app.database import DATABASE_PATH


def setup_environment():
    """Check if environment is set up for demo"""
    print("🔧 ENVIRONMENT SETUP CHECK")
    print("=" * 40)

    # Check for .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file found")
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
    else:
        print("⚠️  .env file not found")
        print("   Copy .env.example to .env and add your Reddit API credentials")
        print("   Get credentials at: https://www.reddit.com/prefs/apps")

    # Check database
    if os.path.exists(DATABASE_PATH):
        print(f"✅ Database found: {DATABASE_PATH}")
    else:
        print(f"📝 Database will be created: {DATABASE_PATH}")

    print()


def demo_entity_extraction():
    """Demonstrate entity extraction capabilities"""
    print("🎯 ENTITY EXTRACTION DEMO")
    print("=" * 40)

    extractor = EntityExtractor()

    # Sample text that would come from social media
    sample_texts = [
        """
        Just had a great conversation with @elonmusk about the future of AI!
        Check out our latest paper at https://arxiv.org/abs/2301.01234
        Contact us at research@ai-lab.edu or +1-800-555-0199
        Follow #AI #MachineLearning #DeepLearning
        ETH donations: 0x742d35Cc6634C0532925a3b8D4C0532950532950
        BTC wallet: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
        """,
        """
        Sorry to see you go @spez. Thanks for building Reddit!
        Visit our new platform at https://newsocial.com
        Email feedback to: feedback@newsocial.com
        Phone support: +1-555-RED-DIT1
        Join the discussion: #RedditFeedback #SocialMedia
        """
    ]

    for i, text in enumerate(sample_texts, 1):
        print(f"\n📝 Sample Text {i}:")
        print("-" * 20)
        print(text.strip()[:100] + ("..." if len(text.strip()) > 100 else ""))

        entities = extractor.extract_entities(text)

        print("🔍 Extracted Entities:")
        for entity_type, values in entities.items():
            if values:
                print(f"  {entity_type.upper():<15}: {', '.join(values[:3])}")
                if len(values) > 3:
                    print(f"  {'':<15}    ... and {len(values) - 3} more")

    print("\n" + "=" * 40)


def demo_database_operations():
    """Demonstrate database storage and retrieval"""
    print("💾 DATABASE OPERATIONS DEMO")
    print("=" * 40)

    # Ensure tables exist
    create_tables()
    print("✅ Database tables ready")

    # Create a sample investigation
    connection = get_connection()
    cursor = connection.execute(
        """
        INSERT OR IGNORE INTO investigations (query, sources, status, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            "OSINT Framework Mid-Term Demo",
            '["reddit"]',
            "active",
            datetime.utcnow().isoformat()
        )
    )
    connection.commit()

    # Get the investigation ID
    investigation_id = cursor.lastrowid if cursor.rowcount > 0 else 1
    connection.close()

    print(f"📋 Using investigation ID: {investigation_id}")

    # Store sample crawled data (simulating what Reddit crawler would produce)
    sample_reddit_data = {
        "platform": "reddit",
        "username": "spez",
        "profile": {
            "username": "spez",
            "id": "t2_xy1",
            "created_utc": 1234567890,
            "comment_karma": 1000000,
            "link_karma": 500000,
            "is_employee": True,
            "is_mod": False,
            "has_verified_email": True
        },
        "posts": [
            {
                "id": "t3_abc1",
                "title": "Introducing Reddit's new API features",
                "selftext": "We're excited to announce improved API access for developers. Check out https://redditblog.com/api-update",
                "url": "https://reddit.com/r/announcements/comments/abc1",
                "subreddit": "announcements",
                "created_utc": 1234567890,
                "score": 5000,
                "num_comments": 120
            }
        ],
        "comments": [
            {
                "id": "t1_def2",
                "body": "This is amazing! Contact us at api@reddit.com for more info. Also check out our Bitcoin wallet: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                "subreddit": "announcements",
                "created_utc": 1234567891,
                "score": 250
            }
        ],
        "crawled_at": datetime.utcnow().isoformat()
    }

    # Store the crawled data
    crawled_data_id = store_crawled_data(
        platform="reddit",
        source_identifier="spez",
        raw_data=sample_reddit_data,
        investigation_id=investigation_id
    )
    print(f"✅ Stored crawled data (ID: {crawled_data_id})")

    # Extract and store entities (simulating what entity extractor would do)
    from app.entity_extractor import EntityExtractor
    extractor = EntityExtractor()

    # Extract from posts and comments
    combined_text = ""
    for post in sample_reddit_data['posts']:
        combined_text += " " + post.get('title', '')
        combined_text += " " + post.get('selftext', '')

    for comment in sample_reddit_data['comments']:
        combined_text += " " + comment.get('body', '')

    entities_data = extractor.extract_entities(combined_text)
    entities_data['usernames'].append('spez')  # Add the username itself

    # Store entities
    entities_stored = store_entities(
        entities=entities_data,
        source_platform="reddit",
        source_identifier="spez",
        crawled_data_id=crawled_data_id,
        investigation_id=investigation_id
    )
    print(f"✅ Stored {entities_stored} entities")

    # Show database stats
    stats = get_investigation_stats(investigation_id)
    print(f"\n📊 Investigation Stats:")
    print(f"  Total crawled records: {stats['total_crawled']}")
    print(f"  Total unique entities: {stats['total_unique_entities']}")
    print(f"  Entities by type: {json.dumps(stats['entities_by_type'], indent=2)}")

    # Demonstrate entity search
    print(f"\n🔍 Entity Search Examples:")
    search_terms = ["spez", "api@reddit.com", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"]
    for term in search_terms:
        results = search_entities(term, investigation_id)
        if results:
            print(f"  Found '{term}': {len(results)} match(es)")
            for result in results[:2]:  # Show first 2 results
                print(f"    - {result['entity_type']}: {result['entity_value']} "
                      f"(from {result['source_platform']})")
        else:
            print(f"  No matches found for '{term}'")

    connection.close()
    print("\n" + "=" * 40)


def show_midterm_presentation_tips():
    """Show tips for what to present in mid-term evaluation"""
    print("🎓 MID-TERM PRESENTATION TIPS")
    print("=" * 40)
    print("🎯 WHAT TO SHOW:")
    print("  1. Working Reddit crawler code (show reddit_crawler.py)")
    print("  2. Entity extraction working (demo with sample text)")
    print("  3. Database storage of crawled data and entities")
    print("  4. Ability to search and retrieve stored entities")
    print("  5. Clear explanation of how this enables cross-platform correlation")
    print()
    print("📝 SAMPLE DEMO FLOW:")
    print("  1. Show environment setup (.env file explanation)")
    print("  2. Run entity extraction on sample social media text")
    print("  3. Show extracted entities (usernames, emails, URLs, etc.)")
    print("  4. Demonstrate database storage")
    print("  5. Show investigation stats")
    print("  6. Demonstrate entity search capabilities")
    print("  7. Explain next steps: adding more platforms, correlation engine")
    print()
    print("💬 TALKING POINTS:")
    print("  • 'We've built the foundation: data collection and entity extraction'")
    print("  • 'This enables us to collect data from Reddit and extract key identifiers'")
    print("  • 'With this foundation, we can now add more platforms (YouTube, Twitter, etc.)'")
    print("  • 'The extracted entities form the basis for our multi-signal correlation engine'")
    print("  • 'Each entity is stored with full provenance and timestamps'")
    print()
    print("🚀 NEXT STEPS (POST-MIDTERM):")
    print("  • Add YouTube crawler (using YouTube Data API)")
    print("  • Add Twitter/X crawler (using Twitter API v2)")
    print("  • Implement multi-signal correlation engine")
    print("  • Build web dashboard for visualization")
    print("  • Add explainability features (show why entities are correlated)")
    print("=" * 40)


def main():
    """Run the complete mid-term demo"""
    print("🚀 OSINT FRAMEWORK MID-TERM DEMO")
    print("=" * 50)
    print("Demonstrating: Reddit Crawler + Entity Extraction + Database Storage")
    print()

    setup_environment()
    demo_entity_extraction()
    demo_database_operations()
    show_midterm_presentation_tips()

    print("\n🎉 DEMO COMPLETE!")
    print("You're ready to showcase your mid-term progress!")


if __name__ == "__main__":
    main()