# organization_website_matcher
A module for organization and its website matcher. Calculate match_score between 0-100.

get the data from kaggle: https://www.kaggle.com/buraksimsek/linkedin-dataset?select=dump.csv

For each company, scrape company_name written in its website (in this case we use website_title and copyright_statement).

Pull and export to csv, for companies have: company_name, website_title, and copyright_statement (optional).

use `cnameMatcher` class in `organizationWebsiteMatcher.py` file to calculate matched_score.

I provide the example in: `get_matched_score.py`
