from organizationWebsiteMatcher import cnameMatcher
from tqdm import tqdm
import pandas as pd

def calculate_matched_score(df):
    for index, row in tqdm(df.iterrows(),ncols=75,desc="Matching"): 
        match_score,matched_text = 0,""
        if bool(row['website_title'] or row['copyright_statement']):
            c5 = False
            if row['website_title']:
                error_msg = [
                    'timed out','page not found','not found','error','403 forbidden','forbidden','index of','coming soon',
                    '508 resource limit is reached','resource limit is reached','site maintenance','domain error','iis7',
                    'under construction','site unavailable','unavailable','bad request','untitled document','welcome to nginx!',
                    'welcome to nginx','410 gone',
                ]
                c5 = any(ele in row['website_title'].lower() for ele in error_msg)
            if not c5:
                matching = cnameMatcher(row['company_name'],row['website_title'],row['copyright_statement'])
                matching_result = matching.result()
                matched_text = matching_result[0]
                match_score = int(matching_result[1]) if int(matching_result[1]) == 100 else int(matching_result[1])+1
                
        row['matched_text'] = matched_text
        row['rapidfuzz_score'] = match_score
        
    return df

if __name__ == '__main__':
    df = pd.read_excel(r'company_webtitle_copyright.xlsx', sheet_name='Sheet1')
    df['matched_text'] = ""
    df['rapidfuzz_score'] = ""
    df = df.replace(float('nan'), '', regex=True)

    new_df = calculate_matched_score(df)
    new_df.to_excel(r'company_webtitle_copyright_match_result.xlsx', index = False, header=True)