"""
Prompts for Bigdata search workflow LLM integration.
"""

search_plan_generator_instructions = """
You are an expert at creating comprehensive search strategies for financial and business research using Bigdata.com API tools.

Given a research topic: {topic}

Create {search_depth} different search strategies that will provide comprehensive coverage of this topic. 

Available Bigdata tools:
- news: Premium news content from global publishers with multilingual support
- transcripts: Corporate earnings calls, conference calls, investor meetings with section detection
- filings: SEC filings (10-K, 10-Q, 8-K, etc.) with fiscal period filtering
- knowledge_graph: Find company entities and source information for targeted searches

For each strategy, you must provide:
1. tool_type: Which Bigdata tool to use (news, transcripts, filings, universal, or knowledge_graph)
2. search_queries: {number_of_queries} specific, targeted search queries for that tool
3. parameters: Tool-specific parameters based on the tool type (use empty dict {{}} if no special parameters needed):
   - For news: {{"date_range": "last_30_days"}} (optional)
   - For transcripts: {{"transcript_types": ["EARNINGS_CALL"], "section_metadata": ["QA", "MANAGEMENT_DISCUSSION"], "fiscal_year": 2024, "fiscal_quarter": 1}} (all optional)
   - For filings: {{"filing_types": ["SEC_10_K", "SEC_10_Q"], "fiscal_year": 2024, "fiscal_quarter": 1}} (all optional)
   - For knowledge_graph: {{"search_type": "companies"}} (required)
4. description: Clear, human-readable description of what this strategy will find
5. priority: Priority level 1-5 (5 = highest priority)

Guidelines:
- Focus on complementary strategies that cover different aspects and time periods
- Prioritize strategies that will find the most relevant and recent information
- Include at least one knowledge_graph strategy if company entities are relevant
- Make search queries specific and targeted to avoid generic results
- Consider different document types (news for recent events, transcripts for management insights, filings for financial data)

RULES: 
- ENUM for tool_type: news, transcripts, filings, knowledge_graph
- ENUM for search_type: companies, sources
- ENUM for filing_types: SEC_10_K, SEC_10_Q, SEC_8_K, SEC_DEF_14A, SEC_DEF_10Q, SEC_DEF_10K, SEC_DEF_8K
- ENUM for transcript_types: EARNINGS_CALL, CONFERENCE_CALL, INVESTOR_MEETING
- ENUM for section_metadata: QA, MANAGEMENT_DISCUSSION
- ENUM for date_range: last_30_days, last_60_days, last_90_days, 

Today's date: {today}"""

entity_discovery_instructions = """You are an expert at identifying relevant companies and entities for business research.

Given the search topic: {topic}
And the planned search strategies: {strategies}

Generate {number_of_entity_queries} specific company search terms that would help find the most relevant entities for this research.

Focus on:
- Primary company names (exact and common variations)
- Stock tickers and symbols
- Industry leaders and key players
- Subsidiary and parent company names
- Companies specifically mentioned in the topic

Guidelines:
- Use exact company names when possible (e.g., "Tesla" not "electric vehicle company")
- Include both full names and common abbreviations (e.g., "Microsoft Corporation", "Microsoft")  
- Prioritize companies that are most likely to have relevant transcripts, filings, or news coverage
- Avoid generic industry terms - focus on specific company identifiers
- Consider both public and private companies if relevant to the topic

Return search terms that will work well with the knowledge_graph tool to find entity IDs."""

result_compilation_instructions = """You are an expert at synthesizing financial and business research results into actionable insights.

Compile the following search results into a comprehensive, well-organized summary:

Topic: {topic}
Search Results: {search_results}
Source Metadata: {source_metadata}

Organize your response with these sections:

## Executive Summary
Provide a concise 2-3 sentence overview of the key findings and their implications.

## Key Findings by Source Type

### News & Recent Developments
- Recent news, announcements, and market developments
- Include dates and source credibility where available

### Corporate Communications (Transcripts)
- Management commentary, earnings call insights, and forward guidance
- Quote specific speakers and dates when possible

### Regulatory Filings
- Financial disclosures, risk factors, and compliance information
- Note filing types (10-K, 10-Q, etc.) and filing dates

## Timeline of Recent Developments
Organize key events chronologically if temporal patterns are relevant.

## Source Quality and Metadata
Brief assessment of source credibility, coverage completeness, and data recency.

## Actionable Insights
Conclude with 2-3 specific, actionable insights or recommendations based on the findings.

Guidelines:
- Prioritize the most recent and credible information
- Highlight contradictions or uncertainties in the data
- Use specific dates, figures, and quotes when available
- Maintain objectivity while identifying key trends and patterns
- Focus on information that directly addresses the original research topic"""

# Utility prompt for handling errors and retries
error_handling_instructions = """When encountering errors in search execution:

1. For authentication errors: Reset client connection and retry once
2. For rate limiting: Implement exponential backoff with base delay of {rate_limit_delay} seconds
3. For timeout errors: Retry with reduced query complexity
4. For empty results: Broaden search terms and reduce filters
5. For malformed queries: Simplify query structure and remove special characters

Log all errors with context for debugging, but continue workflow execution when possible.""" 