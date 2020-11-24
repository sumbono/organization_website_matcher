from organizationWebsiteMatcher import cnameMatcher
from tqdm import tqdm
import pandas as pd

def calculate_matched_score(df):
    for index, row in tqdm(df.iterrows(),ncols=75,desc="Matching"): 
        company_name,website_title,cr_txt,website_url = None,None,None,None
        company_name = row['Name']
        website_title = row['website_title']
        if not website_title:
            website_title = row['website_name']
        cr_txt = row['website_copyright']
        website_url = row['Company Website']

        matching = cnameMatcher(company_name,website_title=website_title,copyright_statement=cr_txt,web_url=website_url)
        matching_result = matching.result()
        matched_text = matching_result[0]
        # match_score = int(matching_result[1]) if int(matching_result[1]) == 100 else int(matching_result[1])+1
        match_score = matching_result[1]
        
        # row['matched_text'] = matched_text
        # row['matched_score'] = match_score

        df.at[index, 'matched_text'] = matched_text
        df.at[index, 'matched_score'] = match_score
        
    return df

if __name__ == '__main__':
    # df = pd.read_excel(r'company_webtitle_copyright.xlsx', sheet_name='Sheet1')
    # df['matched_text'] = ""
    # df['matched_score'] = ""
    # df = df.replace(float('nan'), '', regex=True)
    
    # new_df = calculate_matched_score(df)
    # new_df.to_excel(r'company_webtitle_copyright_match_result.xlsx', index = False, header=True)

    # df = pd.read_excel(r'StarHub-UEN_Batch 3 withdirector_count_MoreThanOne_new.xlsx', sheet_name='StarHub-UEN_Batch 3 withdirecto')
    # df['matched_text'] = ""
    # df['matched_score'] = ""
    # df = df.replace(float('nan'), '', regex=True)
    # print( df.head(15) )

    # new_df = calculate_matched_score(df)
    # print( new_df.head(15) )
    # new_df.to_excel(r'StarHub-UEN_Batch 3 withdirector_count_MoreThanOne_new1.xlsx', index=False, header=True)


    # =================================================================================================================== #

    cr_txt = "copyright © 2006 - 2020 by ttt corporation" 
    website_title = "TTT Corporation"
    site_name = "TTT Corporation"
    company_name = "TTT Co., Ltd"
    website_url = "www.vi.ttt.vn"

    matching = cnameMatcher(company_name,website_title=website_title,copyright_statement=cr_txt,web_url=website_url)
    print(
        f"{matching.company_name} \n{matching.copyright_statement} \n{matching.website_title} \n{matching.web_domain} "
    )
    print("")
    print(
        f"matching result: {matching.result()}"
    )

    # =================================================================================================================== #