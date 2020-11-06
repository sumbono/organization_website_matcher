from rapidfuzz import fuzz,process #rapidfuzz should install with python-Levenshtein
import re, tldextract
from std_name import std_name

class cnameMatcher:
    def __init__(self,company_name=None,website_title=None,copyright_statement=None,web_url=None):
        error_msg = [
            'timed out','page not found','not found','error','403 forbidden','forbidden','index of','coming soon',
            '508 resource limit is reached','resource limit is reached','site maintenance','domain error','iis7',
            'under construction','site unavailable','unavailable','bad request','untitled document','welcome to nginx!',
            'welcome to nginx','410 gone',
        ]
        self.company_name, self.website_title, self.copyright_statement, self.company_name_normalized, self.web_domain = None, None, None, None, None
        if company_name: self.company_name = company_name.lower()  
        if website_title: self.website_title = website_title.lower()
        if self.website_title:
            if any(ele in self.website_title for ele in error_msg):
                self.website_title = None
        if copyright_statement: self.copyright_statement = copyright_statement.lower()
        if self.company_name: self.company_name_normalized = std_name(self.company_name,level=7)
        if web_url: self.web_domain = tldextract.extract(web_url.lower()).domain

    def year_cleaner(self,text):
        is_stop = 0
        while is_stop == 0:
            year_txt = None
            try:
                year_txt = re.search(r"(\d{4})", text).group(1)
            except Exception as err:
                err
            if year_txt: text = text.replace(year_txt,'')
            else: is_stop = 1
        return text

    def text_cleaner(self,text):
        text1 = None
        if text:
            # cleaning_splitter = '[^a-zA-Z0-9]+|singapore|copyright|©|all rights reserved|all right reserved|corporation|corp|incorporated|company|ltd|limited|pllc|llc|group|private|pte'
            cleaning_splitter = 'copyright|©|all rights reserved|all right reserved|corporation|corp|incorporated|company|ltd|limited|pllc|plc|llc|private|pte|privacy|statement|sdn|bhd'
            text_split = [s.strip() for s in re.split(cleaning_splitter, text.lower()) if s]
            text1 = self.year_cleaner(" ".join(text_split))
            # print(f"cleaned_text: {text1} \n")
        return text1

    def result(self):
        match_score_set = ("",0)
        title_list,cr_list = [],[]
        splitter = r'[|\t\n\r\f\v]+| – '
        if self.website_title:
            title_list = [std_name(s,level=7) for s in re.split(splitter, self.text_cleaner(self.website_title)) if s]
        if self.copyright_statement:
            cr_list = [std_name(s,level=7) for s in re.split(splitter, self.text_cleaner(self.copyright_statement)) if s]
        compare_list = title_list + cr_list + [std_name(self.web_domain,level=7)]
        
        # print(f"compare_list: {compare_list} \n")
        
        if self.company_name_normalized and compare_list:
            # match_score_set = process.extract(self.company_name_normalized, compare_list)
            # match_score_set = max(match_score_set, key=lambda x:x[1])
            match_score_set = process.extractOne(self.company_name_normalized, compare_list)
        return (match_score_set)