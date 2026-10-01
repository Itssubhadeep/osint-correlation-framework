import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
from datetime import datetime


DATABASE_PATH = Path("osint.db")


def get_connection():
    """Get a database connection with row factory"""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create all necessary tables for the OSINT framework"""
    connection = get_connection()

    # Investigations table (existing)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            sources TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'created',
            created_at TEXT NOT NULL
        )
        """
    )

    # Crawled data table - stores raw platform data
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS crawled_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            source_identifier TEXT NOT NULL,
            raw_data TEXT,  -- JSON serialized
            crawled_at TEXT NOT NULL,
            investigation_id INTEGER,
            FOREIGN KEY (investigation_id) REFERENCES investigations (id)
        )
        """
    )

    # Entities table - stores extracted and normalized entities
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT NOT NULL,  -- username, email, url, phone, hashtag, crypto
            entity_value TEXT NOT NULL,
            source_platform TEXT NOT NULL,
            source_identifier TEXT NOT NULL,
            confidence_score REAL DEFAULT 1.0,
            provenance TEXT,  -- JSON: where exactly we found it
            extracted_at TEXT NOT NULL,
            crawled_data_id INTEGER,
            investigation_id INTEGER,
            FOREIGN KEY (crawled_data_id) REFERENCES crawled_data (id),
            FOREIGN KEY (investigation_id) REFERENCES investigations (id),
            UNIQUE(entity_type, entity_value, source_platform, source_identifier, crawled_data_id)
        )
        """
    )

    # Create indices for performance
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_crawled_platform_source
        ON crawled_data(platform, source_identifier)
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_entities_value
        ON entities(entity_value)
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_entities_type
        ON entities(entity_type)
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_crawled_investigation
        ON crawled_data(investigation_id)
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_entities_investigation
        ON entities(investigation_id)
        """
    )

    connection.commit()
    connection.close()


def store_crawled_data(
    platform: str,
    source_identifier: str,
    raw_data: Dict[str, Any],
    investigation_id: Optional[int] = None
) -> int:
    """Store raw crawled data and return the record ID"""
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO crawled_data (platform, source_identifier, raw_data, crawled_at, investigation_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            platform,
            source_identifier,
            json.dumps(raw_data),
            datetime.utcnow().isoformat(),
            investigation_id
        )
    )

    connection.commit()
    crawled_data_id = cursor.lastrowid
    connection.close()

    return crawled_data_id


def store_entities(
    entities: Dict[str, List[str]],
    source_platform: str,
    source_identifier: str,
    crawled_data_id: int,
    investigation_id: Optional[int] = None
) -> int:
    """Store extracted entities and return count of new entities stored"""
    connection = get_connection()

    stored_count = 0

    for entity_type, values in entities.items():
        if not values:
            continue

        for value in values:
            if not value or not isinstance(value, str):
                continue

            try:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO entities
                    (entity_type, entity_value, source_platform, source_identifier,
                     crawled_data_id, investigation_id, extracted_at, provenance)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        entity_type,
                        value,
                        source_platform,
                        source_identifier,
                        crawled_data_id,
                        investigation_id,
                        datetime.utcnow().isoformat(),
                        json.dumps({"source_type": "crawled_data", "crawled_data_id": crawled_data_id})
                    )
                )

                if connection.total_changes > 0:
                    stored_count += 1

            except Exception as e:
                # Log error but continue processing other entities
                print(f"Warning: Failed to store entity {entity_type}:{value} - {e}")

    connection.commit()
    connection.close()

    return stored_count


def get_investigation_stats(investigation_id: int) -> Dict[str, Any]:
    """Get statistics for a specific investigation"""
    connection = get_connection()

    stats = {}

    # Total crawled records
    cursor = connection.execute(
        """
        SELECT COUNT(*) as count
        FROM crawled_data
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    )
    stats['total_crawled'] = cursor.fetchone()['count']

    # Total entities by type
    cursor = connection.execute(
        """
        SELECT entity_type, COUNT(*) as count
        FROM entities
        WHERE investigation_id = ?
        GROUP BY entity_type
        """,
        (investigation_id,)
    )
    stats['entities_by_type'] = {row['entity_type']: row['count'] for row in cursor.fetchall()}

    # Total unique entities
    cursor = connection.execute(
        """
        SELECT COUNT(DISTINCT entity_value) as count
        FROM entities
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    )
    stats['total_unique_entities'] = cursor.fetchone()['count']

    # Platforms crawled
    cursor = connection.execute(
        """
        SELECT DISTINCT platform
        FROM crawled_data
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    )
    stats['platforms_crawled'] = [row['platform'] for row in cursor.fetchall()]

    connection.close()

    return stats


def search_entities(
    entity_value: str,
    investigation_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Search for entities by value"""
    connection = get_connection()

    if investigation_id:
        cursor = connection.execute(
            """
            SELECT e.*, c.platform as source_platform_name
            FROM entities e
            LEFT JOIN crawled_data c ON e.crawled_data_id = c.id
            WHERE e.entity_value = ? AND e.investigation_id = ?
            """,
            (entity_value, investigation_id)
        )
    else:
        cursor = connection.execute(
            """
            SELECT e.*, c.platform as source_platform_name
            FROM entities e
            LEFT JOIN crawled_data c ON e.crawled_data_id = c.id
            WHERE e.entity_value = ?
            """,
            (entity_value,)
        )

    results = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return results


if __name__ == "__main__":
    # Demo the database functions
    print("🔧 Database Initialization Demo")
    print("=" * 40)

    create_tables()
    print("✅ Tables created/verified")

    # Store sample crawled data
    sample_reddit_data = {
        "platform": "reddit",
        "username": "spez",
        "posts": [
            {"title": "Hello Reddit!", "selftext": "Just testing the API", "url": "https://reddit.com/r/test"}
        ],
        "comments": [
            {"body": "Great post! Check out https://example.com", "subreddit": "test"}
        ]
    }

    crawled_id = store_crawled_data("reddit", "spez", sample_reddit_data)
    print(f"✅ Stored crawled data with ID: {crawled_id}")

    # Store sample entities
    sample_entities = {
        "usernames": ["spez", "testuser"],
        "urls": ["https://example.com", "https://github.com/osint"],
        "emails": ["contact@example.com"]
    }

    stored_count = store_entities(sample_entities, "reddit", "spez", crawled_id)
    print(f"✅ Stored {stored_count} new entities")

    # Get stats
    stats = get_investigation_stats(1)  # Assuming investigation ID 1 exists
    print(f"📊 Stats: {stats}")

    print("\n🎯 Database ready for OSINT framework!")