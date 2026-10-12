# 🛰️ OSINT Correlation Framework

### 🔍 Multi-Source Intelligence Collection & Cross-Source Indicator Analysis

> 🛡️ **Transforming scattered public information into structured, explainable intelligence.**

**OSINT Correlation Framework** is a Python-powered intelligence collection platform that aggregates publicly available information from multiple sources, extracts technical indicators, and identifies shared indicators across independent records.

Built with **FastAPI, SQLite, Python, HTML, CSS, and JavaScript**, the project focuses on modular backend development, data processing, source normalization, and transparent evidence-based correlation.

---

## ✨ Key Features

### 🌐 Multi-Source Intelligence Collection

- 🔎 Collects public search results from **Hacker News, DEV Community, and Stack Overflow**.
- 🔄 Normalizes collected information into consistent record structures.
- 🧹 Filters duplicate records using source identifiers.
- ⚡ Handles individual source failures without terminating the entire search.
- 📊 Displays aggregated search results through a web dashboard.

### 🧠 Cross-Source Indicator Correlation

- 📧 Extracts email addresses from supplied source records.
- 🔗 Extracts and normalizes URL hostnames.
- 🧩 Identifies indicators appearing across multiple independent sources.
- 📈 Calculates distinct source counts.
- 🧾 Provides supporting source references for each match.

**Note:** Shared technical indicators are evidence of overlap, not proof that separate accounts belong to the same person.

### 🗄️ SQLite Database Components

- Investigation and entity storage modules.
- Source-record persistence functions.
- Indexed database queries.
- Provenance metadata for tracing collected information.

### 🖥️ Interactive Web Dashboard

- Search interface for public intelligence collection.
- Aggregated source results.
- FastAPI-powered backend integration.
- Responsive frontend built with HTML, CSS, and JavaScript.

The correlation API is implemented separately and is not yet automatically connected to live dashboard searches.

---

## 🏗️ System Architecture

```text
                  👤 User
                     |
                     v
             🖥️ Web Dashboard
              HTML / CSS / JS
                     |
                     v
               ⚡ FastAPI
                REST Layer
                     |
          +----------+----------+
          |                     |
          v                     v
    🌐 OSINT Collectors    🧠 Correlation API
          |                     |
    +-----+------+       Indicator Extraction
    |     |      |               |
 Hacker  DEV    Stack            v
 News  Community Overflow   Cross-Source Matches
    |     |      |
    +-----+------+
          |
          v
    Normalized Results

    🗄️ SQLite Storage Modules
       (separate components)
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| 🐍 Language | Python |
| ⚡ Backend | FastAPI, Uvicorn |
| 🗄️ Database | SQLite |
| 🎨 Frontend | HTML, CSS, JavaScript |
| 🧠 Processing | Regular Expressions, Data Normalization |
| 🌐 Integration | Public OSINT Sources |
| 📚 Documentation | OpenAPI / Swagger UI |

---

## 📁 Project Structure

```text
osint-correlation-framework/
│
├── app/
│   ├── main.py
│   ├── correlation.py
│   ├── entity_extractor.py
│   ├── database.py
│   └── ...
│
├── requirements.txt
├── README.md
└── ...
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Itssubhadeep/osint-correlation-framework.git
cd osint-correlation-framework
```

### 2️⃣ Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3️⃣ Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

Ensure `requirements.txt` is saved in UTF-8 encoding.

### 4️⃣ Launch the Application

```powershell
python -m uvicorn app.main:app --reload --port 8080
```

### 5️⃣ Access the Application

| Service | Local URL |
|---|---|
| 🖥️ Web Dashboard | http://127.0.0.1:8080/dashboard |
| 📚 API Documentation | http://127.0.0.1:8080/docs |
| ❤️ API Root | http://127.0.0.1:8080/ |

---

## 🔌 REST API

### 🔎 Search Intelligence

**`POST /api/search`**

Collects and aggregates publicly available information from supported OSINT sources.

### 🧠 Correlate Indicators

**`POST /api/correlate`**

Identifies shared email addresses and URL hostnames across records from distinct sources.

**📤 Example Request**

```json
{
  "records": [
    {
      "source": "Hacker News",
      "external_id": "101",
      "content": "Contact security@example.org"
    },
    {
      "source": "DEV Community",
      "external_id": "202",
      "content": "Email security@example.org"
    }
  ]
}
```

**📥 Example Response**

```json
{
  "total_records": 2,
  "total_correlations": 1,
  "correlations": [
    {
      "indicator_type": "email",
      "indicator": "security@example.org",
      "sources": [
        "DEV Community",
        "Hacker News"
      ],
      "source_count": 2,
      "evidence": [
        {
          "source": "DEV Community",
          "external_id": "202"
        },
        {
          "source": "Hacker News",
          "external_id": "101"
        }
      ]
    }
  ]
}
```

---

## 🧪 Testing & Validation

The project includes initial component-level tests and supports manual API testing through FastAPI's Swagger UI.

To verify the correlation module, run:

```powershell
python -c "from app.correlation import correlate_records; print(correlate_records([{'source':'Hacker News','external_id':'1','content':'Contact test@example.org'},{'source':'DEV Community','external_id':'2','content':'Email test@example.org'}]))"
```

Expected behavior: the output contains one email indicator shared by two distinct sources.

---

## 📊 Current Capabilities

| Capability | Status |
|---|---|
| Multi-source public data collection | ✅ Implemented |
| FastAPI backend | ✅ Implemented |
| Interactive search dashboard | ✅ Implemented |
| Email and domain extraction | ✅ Implemented |
| Cross-source indicator matching API | ✅ Implemented |
| SQLite storage components | ✅ Implemented |
| Automatic dashboard correlation | 🚧 Planned |
| Live-search database persistence | 🚧 In progress |
| Advanced entity resolution | 📋 Planned |

---

## 🗺️ Development Roadmap

- [x] Build modular FastAPI backend.
- [x] Integrate multiple public data sources.
- [x] Implement normalized search results.
- [x] Develop web dashboard.
- [x] Implement basic indicator extraction.
- [x] Add cross-source correlation API.
- [ ] Automatically correlate live search results.
- [ ] Connect investigation storage to live search.
- [ ] Add comprehensive API integration tests.
- [ ] Introduce relationship graph visualization.
- [ ] Improve source error handling and rate-limit management.

---

## ⚠️ Known Limitations

- Correlation currently uses exact normalized indicators, not probabilistic identity matching.
- Some external sources may be temporarily unavailable or rate-limited.
- Live search results are not automatically persisted through the search endpoint.
- Correlation results are accessible through the API rather than a dedicated dashboard visualization.

---

## 🔐 Ethical & Responsible Use

This project is intended for **educational research, authorized investigations, and analysis of publicly available information**.

Users should respect privacy, source terms of service, applicable laws, and data-retention requirements. The framework should not be used to harass, profile, or deanonymize individuals.

---

## 👨‍💻 Developer

**Subhadeep Ghosh**

🎓 Master of Computer Applications (MCA)

🔐 Cybersecurity | Digital Forensics | Python Backend Development

🌐 **GitHub:** https://github.com/Itssubhadeep

🔗 **Project Repository:** https://github.com/Itssubhadeep/osint-correlation-framework

---

### ⭐ Support the Project

If you find this project useful, consider giving the repository a star!

*Built with Python, curiosity, and a focus on responsible security engineering.*
