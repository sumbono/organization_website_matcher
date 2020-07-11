from rapidfuzz import fuzz,process #rapidfuzz should install with python-Levenshtein
import re

class cnameMatcher:
    def __init__(self,company_name,website_title,copyright_statement):
        self.company_name = company_name
        self.website_title = website_title
        self.copyright_statement = copyright_statement
        # self.result = ("",0)

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
            if text1:
                lst = text1.split(" ")
                lst = ["".join(txt1.replace('.','').replace(',','').replace(')','').replace('(','').replace('-','').strip().split())  for txt1 in lst if txt1]
                text1 = " ".join(lst).strip()
        return text1

    def result(self):
        match_score_set = ("",0)
        title_list,cr_list = [],[]
        splitter = r'[)(\/\|,;:\t\n\r\f\v]+| and |-'
        if self.website_title:
            title_list = [s.strip() for s in re.split(splitter, self.website_title) if s]
            title_list = [self.text_cleaner(txt) for txt in title_list if self.text_cleaner(txt)]
        if self.copyright_statement:
            cr_list = [s.strip() for s in re.split(splitter, self.copyright_statement) if s]
            cr_list = [self.text_cleaner(txt) for txt in cr_list if self.text_cleaner(txt)]
        compare_list = title_list + cr_list
        
        splitter = r'[)(\/\|,;:\t\n\r\f\v]+|-'
        cname_list = [self.text_cleaner(s.strip()) for s in re.split(splitter, self.company_name) if s if self.text_cleaner(s.strip())]
        
        if cname_list and compare_list:
            result = [process.extractOne(comp_name, compare_list) for comp_name in cname_list] 
            match_score_set = max(result, key=lambda x:x[1])
        return (match_score_set)