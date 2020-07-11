# organization_website_matcher
A module for organization and its website matcher. Calculate match_score between 0-100.

get the data from kaggle: https://www.kaggle.com/buraksimsek/linkedin-dataset?select=dump.csv

For each company, scrape its website and grab existing company_name (in this case we use website_title and copyright_statement).

Take companies have: company_name, website_title, and copyright_statement (optional). Export them to `company_webtitle_copyright.xlsx`. 

use `cnameMatcher` class in `organizationWebsiteMatcher.py` file to calculate matched_score for records in `company_webtitle_copyright.xlsx`.

I provide the example in: `get_matched_score.py`
