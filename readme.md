# 🕵️‍♂️ OSINT Framework: Multi-Platform Social Media Crawling & Intelligence Extraction

**A college minor project for collecting publicly available OSINT data and identifying potential cross-source entity relationships using multiple independent correlation signals.**

## 🎯 Project Goal

The system aims to:
- Collect publicly available data from multiple online sources
- Extract cyber-relevant entities (usernames, emails, URLs, phone numbers, etc.)
- Normalize extracted entities for cross-platform comparison
- Correlate entities across different sources using multiple independent signals
- Calculate explainable confidence scores
- Preserve source provenance (chain of custody)
- Present investigation results through a web dashboard and REST API

## 🚀 **IMPORTANT: Reddit API Credentials REQUIRED**

**To answer your question: YES, you NEED Reddit API credentials.** The Reddit crawler does NOT connect automatically - it requires explicit API authentication.

### 🔑 How to Get Reddit API Credentials:
1. Go to: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the form (name, description, about URL, redirect URL)
5. Click "Create App"
6. **SAVE YOUR CREDENTIALS:**
   - **Client ID** (found under the app name)
   - **Client Secret** (found under 'secret' field)
7. Set these in your `.env` file:
   ```
   REDDIT_CLIENT_ID=your_actual_client_id_here
   REDDIT_CLIENT_SECRET=your_actual_client_secret_here
   REDDIT_USER_AGENT=OSINTFrameworkDemo/1.0 by your_reddit_username
   ```

**Without these credentials, the Reddit crawler will NOT work.**

## 🚀 Mid-Term Focus: Working Proof of Concept

For the mid-term evaluation, we have implemented:
- ✅ **Reddit crawler** using PRAW (Reddit API) - **requires credentials**
- ✅ **Entity extraction module** (usernames, emails, URLs, phones, hashtags, crypto)
- ✅ **SQLite database** with provenance tracking
- ✅ **REST API endpoints** for investigations
- ✅ **Demo scripts** to showcase functionality

This foundation enables the future addition of more platforms (YouTube, Twitter/X, etc.) and the multi-signal correlation engine.

## 📊 Current Status

**Ready for mid-term demonstration:**

### Implemented Components:
- **FastAPI application** with health-check and API documentation
- **Reddit crawler** (`app/reddit_crawler.py`) - fetches user data, posts, comments (**requires API credentials**)
- **Entity extractor** (`app/entity_extractor.py`) - regex-based extraction of 6 entity types
- **Enhanced database** (`app/database.py`) - stores crawled data, entities, provenance
- **Demo script** (`demo_midterm.py`) - showcases extraction and storage capabilities
- **Test suite** (`test_demo.py`) - verifies component functionality

### Database Schema:
- `investigations` - tracking investigation queries
- `crawled_data` - raw platform-specific data (JSON format)
- `entities` - extracted and normalized entities with provenance
- Proper indexing for fast lookup and correlation

## 🔧 Setup Instructions

### 1. Clone Repository & Activate Environment
```bash
# If you haven't already cloned:
# git clone <repository-url>
# cd osint-correlation-framework

# Activate virtual environment (already created)
.venv\Scripts\Activate.ps1  # Windows
# OR
source .venv/bin/activate   # Linux/Mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*Note: This includes `praw==7.7.0` for Reddit API access*

### 3. **GET REDDIT API CREDENTIALS (MANDATORY)**
**You MUST complete this step for the demo to work:**
1. Visit: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in:
   - Name: `OSINTFrameworkDemo` (or similar)
   - Description: `OSINT Framework Mid-Term Demo`
   - About URL: `https://github.com/yourusername/osint-framework` (can be placeholder)
   - Redirect URI: `http://localhost:8080` (can be anything for script auth)
5. Click "Create App"
6. Note your:
   - **Client ID** (found under the app name)
   - **Client Secret** (found under 'secret' field)

### 4. Configure Environment Variables
```bash
# Copy the example environment file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac

# Edit .env and add your credentials:
# REDDIT_CLIENT_ID=your_actual_client_id_here
# REDDIT_CLIENT_SECRET=your_actual_client_secret_here
# REDDIT_USER_AGENT=OSINTFrameworkDemo/1.0 by your_reddit_username
```

### 5. Initialize Database
```bash
python -c "from app.database import create_tables; create_tables(); print('Database initialized')"
```

## 🎯 Mid-Term Demo: What to Show

Run the demonstration script to see your framework in action:

```bash
python demo_midterm.py
```

This will show:
1. 🔍 **Entity extraction** from sample social media text
2. 💾 **Database storage** of crawled data and entities
3. 📊 **Investigation statistics** 
4. 🔎 **Entity search capabilities**
5. 🎓 **Presentation tips** for your mid-term evaluation

### Expected Output:
```
🚀 OSINT FRAMEWORK MID-TERM DEMO
==================================================

🔧 ENVIRONMENT SETUP CHECK
...

🎯 ENTITY EXTRACTION DEMO
...
🔍 Extracted Entities:
  USERNAMES: @johndoe
  EMAILS: john.doe@example.com
  URLS: https://example.com/path
  PHONE_NUMBERS: +1-555-123-4567
  HASHTAGS: #BreakingNews, #Tech
  CRYPTO_ADDRESSES: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa, 0x742d35Cc...

💾 DATABASE OPERATIONS DEMO
...
📊 Investigation Stats:
  Total crawled records: 1
  Total unique entities: 8
  Entities by type: {
    'usernames': 2,
    'emails': 1,
    'urls': 2,
    'hashtags': 2,
    'crypto_addresses': 2
  }

🔍 Entity Search Examples:
  Found 'spez': 1 match(es)
    - username: spez (from reddit)
  Found 'api@reddit.com': 1 match(es)
    - email: api@reddit.com (from reddit)
  ...

🎓 MID-TERM PRESENTATION TIPS
...
```

## 📁 File Structure

```
osint-correlation-framework/
├── README.md                 # This file
├── .gitignore               # Ignores secrets, __pycache__, *.db, etc.
├── requirements.txt         # Python dependencies (includes praw)
├── .env.example             # Template for credentials (copy to .env)
├── demo_midterm.py          # Mid-term demonstration script
├── test_demo.py             # Component verification tests
├── osint.db                 # SQLite database (auto-generated)
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Enhanced database operations
│   ├── entity_extractor.py  # Entity extraction logic
│   ├── reddit_crawler.py    # Reddit API crawler (**requires credentials**)
│   └── schemas.py           # Pydantic models
└── .venv/                   # Virtual environment (already created)
```

## 💻 API Endpoints

The FastAPI application provides these endpoints:

```
GET  /                    # API root - "API is running"
GET  /health              # Health check - returns {"status": "healthy"}
POST /api/investigations  # Create new investigation
                           # Body: {"query": "string", "sources": ["array"]}
                           # Returns: investigation ID and details

GET  /docs                # Automatic Swagger UI documentation
GET  /redoc               # Alternative ReDoc documentation
```

## 📈 Mid-Term Presentation Guide

### 🎯 What to Demonstrate:
1. **Working Code Showcase**
   - Open `app/reddit_crawler.py` - show the Reddit API integration (**emphasize that credentials are required**)
   - Open `app/entity_extractor.py` - show the regex patterns for 6 entity types
   - Open `app/database.py` - show the enhanced schema for provenance tracking

2. **Live Demo Execution**
   - Run: `python demo_midterm.py`
   - Show entity extraction from sample text
   - Show database storage and retrieval
   - Show investigation statistics

3. **Explain the Architecture**
   - **Data Flow**: Reddit API → Raw Data Storage → Entity Extraction → Entity Storage
   - **Provenance**: Every entity stores source platform, identifier, extraction time
   - **Normalization**: Usernames lowercased, URLs stripped of tracking params, etc.
   - **Foundation**: This enables cross-platform correlation (future work)

### 💬 Key Talking Points:
- **"We've solved the first hard problem: automated data collection and entity extraction"**
- **"Instead of manually visiting Reddit profiles, our crawler fetches posts/comments and extracts key identifiers"**
- **"Each extracted entity is stored with full provenance - we know exactly where it came from"**
- **"This foundation lets us add more platforms (YouTube, Twitter, etc.) without changing the core logic"**
- **"The extracted entities form the basis for our multi-signal correlation engine (to be built post-midterm)"**
- **"We're respecting platform terms by only accessing public data through official APIs where available"**
- **"**CRITICAL: The Reddit crawler requires API credentials - it does not connect automatically**"

### 📊 Show These Results:
- Number of entities extracted from sample text
- Database statistics showing stored crawled data and entities
- Successful entity search demonstrations
- Clear before/after: raw social media text → structured entity data

## 🔮 Future Work (Post-Midterm)

1. **Add More Platforms**:
   - YouTube crawler (YouTube Data API)
   - Twitter/X crawler (Twitter API v2)
   - Instagram (limited public data via web scraping with rate limiting)
   - Reddit enhancements (subreddit monitoring, search)

2. **Build Multi-Signal Correlation Engine**:
   - Exact identifier matches (username, email, etc.)
   - Fuzzy string similarity (Levenshtein, Jaro-Winkler for usernames)
   - Shared contextual analysis (bio keywords, linked websites)
   - Temporal activity patterns (posting frequency, time of day)
   - Network analysis (common followers/friends when available via API)

3. **Explainability & Visualization**:
   - Web dashboard showing correlation networks
   - "Why correlated?" explanations showing which signals contributed
   - Confidence score breakdown by signal type
   - Timeline views of entity activity

4. **Advanced Features**:
   - Entity resolution and merging
   - Alerting for new entity sightings
   - Export capabilities (CSV, JSON, PDF reports)
   - Rate limiting and error handling for production use

## 🙏 Acknowledgments

- Reddit for providing public API access (requires developer registration and credentials)
- FastAPI team for excellent Python API framework
- PRAW team for Reddit API wrapper
- Open-source OSINT community for inspiration and ethical guidelines

---

**🎯 Ready for Mid-Term**: Demonstrate working crawler → entity extraction → stored provenance  
**🔑 REMEMBER**: You **MUST** get Reddit API credentials for the demo to work  
**💡 Tip**: Show working code and clear progression from idea to demonstrable result!