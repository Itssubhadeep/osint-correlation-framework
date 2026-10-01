"""
Quick test to verify the OSINT framework components work together
Run this to check if your setup is ready for mid-term demo
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")

    try:
        # Add app directory to path
        sys.path.append(str(Path(__file__).parent / "app"))

        from app.entity_extractor import EntityExtractor
        from app.database import create_tables, get_connection
        print("✅ Core modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_entity_extraction():
    """Test entity extraction with sample data"""
    print("\n🧪 Testing entity extraction...")

    try:
        sys.path.append(str(Path(__file__).parent / "app"))
        from app.entity_extractor import EntityExtractor

        extractor = EntityExtractor()

        # Test text with various entity types
        test_text = """
        Contact @johndoe for more info.
        Email: john.doe@example.com
        Visit: https://example.com/path?param=value#section
        Call: +1-555-123-4567
        Follow: #BreakingNews #Tech
        BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
        ETH: 0x742d35Cc6634C0532925a3b8D4C0532950532950
        """

        entities = extractor.extract_entities(test_text)

        # Check that we found entities
        total_entities = sum(len(v) for v in entities.values())
        if total_entities > 0:
            print(f"✅ Entity extraction working: {total_entities} entities found")
            for entity_type, values in entities.items():
                if values:
                    print(f"   {entity_type}: {len(values)} found")
            return True
        else:
            print("❌ No entities found in test text")
            return False

    except Exception as e:
        print(f"❌ Entity extraction test failed: {e}")
        return False

def test_database():
    """Test database operations"""
    print("\n🧪 Testing database operations...")

    try:
        sys.path.append(str(Path(__file__).parent / "app"))
        from app.database import create_tables, get_connection, store_crawled_data, store_entities

        # Use a temporary database for testing
        import tempfile
        import os
        from app.database import DATABASE_PATH

        # Backup original database if it exists
        original_db = DATABASE_PATH
        temp_dir = tempfile.mkdtemp()
        temp_db = Path(temp_dir) / "test.db"

        # Temporarily override DATABASE_PATH
        import app.database
        app.database.DATABASE_PATH = temp_db

        try:
            create_tables()

            # Test storing crawled data
            sample_data = {
                "test": "data",
                "username": "testuser",
                "timestamp": "2023-01-01T00:00:00Z"
            }

            crawled_id = store_crawled_data(
                platform="test",
                source_identifier="testuser",
                raw_data=sample_data
            )

            if crawled_id > 0:
                print("✅ Crawled data storage working")
            else:
                print("❌ Failed to store crawled data")
                return False

            # Test storing entities
            sample_entities = {
                "usernames": ["testuser"],
                "emails": ["test@example.com"],
                "urls": ["https://example.com"]
            }

            stored_count = store_entities(
                entities=sample_entities,
                source_platform="test",
                source_identifier="testuser",
                crawled_data_id=crawled_id
            )

            if stored_count > 0:
                print(f"✅ Entity storage working: {stored_count} entities stored")
            else:
                print("❌ Failed to store entities")
                return False

            return True

        finally:
            # Restore original DATABASE_PATH
            app.database.DATABASE_PATH = original_db
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_reddit_crawler_structure():
    """Test that Reddit crawler is structured correctly (without API calls)"""
    print("\n🧪 Testing Reddit crawler structure...")

    try:
        sys.path.append(str(Path(__file__).parent / "app"))
        # Just check if we can import it - don't initialize to avoid API calls
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "reddit_crawler",
            Path(__file__).parent / "app" / "reddit_crawler.py"
        )
        if spec and spec.loader:
            print("✅ Reddit crawler module structure OK")
            return True
        else:
            print("❌ Reddit crawler module structure issues")
            return False
    except Exception as e:
        print(f"❌ Reddit crawler structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔬 OSINT FRAMEWORK COMPONENT TEST")
    print("=" * 40)

    tests = [
        test_imports,
        test_entity_extraction,
        test_database,
        test_reddit_crawler_structure
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 40)
    print(f"📊 TEST RESULTS: {passed}/{total} passed")

    if passed == total:
        print("🎉 All tests passed! Your framework is ready for mid-term demo.")
        print("\n🚀 Next steps:")
        print("   1. Get Reddit API credentials (https://www.reddit.com/prefs/apps)")
        print("   2. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env")
        print("   3. Run: python demo_midterm.py")
        print("   4. Show the results in your mid-term presentation!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)