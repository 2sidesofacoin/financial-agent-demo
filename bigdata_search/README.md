# Bigdata Search Tools

A standalone Python module for comprehensive search across Bigdata.com's premium financial and news content. Features advanced search capabilities for news, corporate transcripts, SEC filings, and knowledge graph entities.

## Features

- **News Search**: Premium global news content with multilingual support
- **Transcript Search**: Corporate earnings calls with section detection and speaker identification
- **Filings Search**: SEC documents with fiscal period and entity filtering  
- **Universal Search**: Cross-document search with unified ranking
- **Knowledge Graph**: Company and source discovery with entity ID lookup
- **LangChain Integration**: Ready-to-use tools for AI agents and workflows

## Installation

```bash
# Install required dependencies
pip install bigdata-client langchain-core

# Set environment variables
export BIGDATA_USERNAME="your_username"
export BIGDATA_PASSWORD="your_password"
```

## Quick Start

### 1. Basic Search Example

```python
import asyncio
from bigdata_search.tools import bigdata_news_search, bigdata_knowledge_graph

async def main():
    # Find Tesla's entity ID
    companies = await bigdata_knowledge_graph.ainvoke({
        "search_type": "companies",
        "search_term": "Tesla",
        "max_results": 3
    })
    
    # Search Tesla news
    news = await bigdata_news_search.ainvoke({
        "queries": ["Tesla earnings", "Model 3 production"],
        "max_results": 5,
        "date_range": "last_30_days",
        "entity_ids": ["DD3BB1"]  # Tesla's entity ID
    })
    
    print(news)

asyncio.run(main())
```

### 2. Advanced Transcript Search

```python
from bigdata_search.tools import bigdata_transcript_search

# Search Q&A sections of earnings calls
results = await bigdata_transcript_search.ainvoke({
    "queries": ["guidance for next quarter", "margin outlook"],
    "transcript_types": ["EARNINGS_CALL"],
    "section_metadata": ["QA"],  # Only Q&A sections
    "fiscal_year": 2024,
    "entity_ids": ["DD3BB1"]  # Tesla
})
```

### 3. SEC Filings Search

```python
from bigdata_search.tools import bigdata_filings_search

# Search Tesla's 10-K and 10-Q filings
results = await bigdata_filings_search.ainvoke({
    "queries": ["risk factors", "competition"],
    "filing_types": ["SEC_10_K", "SEC_10_Q"],
    "reporting_entity_ids": ["DD3BB1"],  # Filed by Tesla
    "fiscal_year": 2024
})
```

## Available Tools

### Core Search Tools

| Tool | Description | Key Features |
|------|-------------|--------------|
| `bigdata_news_search` | Premium news content | Multilingual, real-time, source filtering |
| `bigdata_transcript_search` | Corporate transcripts | Section detection, speaker ID, fiscal filters |
| `bigdata_filings_search` | SEC filings | Form types, reporting entities, fiscal periods |
| `bigdata_universal_search` | Cross-document search | Unified ranking, all content types |
| `bigdata_knowledge_graph` | Entity discovery | Company IDs, source credibility, autosuggest |

### Advanced Features

#### Section Detection (Transcripts)
```python
# Search specific transcript sections
"section_metadata": [
    "QA",                    # Questions & Answers
    "QUESTION",              # Questions only  
    "ANSWER",                # Answers only
    "MANAGEMENT_DISCUSSION"  # Management discussion
]
```

#### Transcript Types
```python
"transcript_types": [
    "EARNINGS_CALL",
    "CONFERENCE_CALL", 
    "ANALYST_INVESTOR_SHAREHOLDER_MEETING",
    "GENERAL_PRESENTATION",
    "GUIDANCE_CALL"
]
```

#### SEC Filing Types
```python
"filing_types": [
    "SEC_10_K",    # Annual reports
    "SEC_10_Q",    # Quarterly reports
    "SEC_8_K",     # Current reports
    "SEC_20_F",    # Foreign annual reports
    "SEC_S_1",     # IPO registration
    "SEC_S_3"      # Shelf registration
]
```

#### Date Range Filtering
```python
# Rolling ranges
"date_range": "today"           # Today only
"date_range": "last_week"       # Past 7 days
"date_range": "last_30_days"    # Past 30 days
"date_range": "last_90_days"    # Past 90 days
"date_range": "year_to_date"    # Current year

# Absolute ranges
"date_range": "2024-01-01,2024-12-31"  # Specific period
```

## Module Structure

```
bigdata_search/
├── __init__.py          # Main module exports
├── utils.py             # Core async search functions
├── tools.py             # LangChain tool wrappers
└── README.md            # This file

examples/
└── bigdata_tools_example.py  # Comprehensive usage example
```

## Error Handling

The module includes robust error handling:

- **Authentication**: Automatic client management and token refresh
- **Rate Limiting**: Built-in delays and retry logic
- **Connection Issues**: Graceful fallbacks and error messages
- **Invalid Parameters**: Clear validation and helpful error messages

## Performance Features

- **Singleton Client**: Prevents "too many logins" errors
- **Connection Pooling**: Efficient concurrent requests
- **Result Caching**: Automatic JWT token reuse
- **Async Processing**: Non-blocking search execution

## Use Cases

### Financial Research
- Earnings call analysis with speaker identification
- SEC filing risk factor extraction
- Cross-document correlation analysis
- Sentiment tracking across news and transcripts

### News Monitoring
- Real-time news alerts for specific companies
- Source credibility filtering
- Multilingual content analysis
- Historical news trend analysis

### Compliance & Risk
- SEC filing change detection
- Regulatory disclosure monitoring
- Management guidance tracking
- Risk factor evolution analysis

## Examples

See `examples/bigdata_tools_example.py` for a comprehensive demonstration of all features.

## Requirements

- Python 3.8+
- `bigdata-client` - Official Bigdata.com Python client
- `langchain-core` - For tool decorators and integration
- Valid Bigdata.com account with API access

## Environment Variables

```bash
BIGDATA_USERNAME=your_username
BIGDATA_PASSWORD=your_password
```

## License

This module is designed to work with the Bigdata.com API. Please ensure you have appropriate API access and comply with Bigdata.com's terms of service. 