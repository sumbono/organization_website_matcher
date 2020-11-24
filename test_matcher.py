from organizationWebsiteMatcher import cnameMatcher
from tqdm import tqdm
from pymongo import MongoClient,UpdateOne,InsertOne, UpdateMany
from pymongo.errors import BulkWriteError
# import uuid

# # make a UUID based on the host address and current time
# uuidOne = uuid.uuid1()
# print(type(str(uuidOne)))
# print(str(uuidOne))

# cr_txt = "Copyright © 2561 www | copyright © 2561 www.supervac.co.th สงวนสิทธิ์ทุกประการ  " 
# website_title = ""
# site_name = ""
# company_name = "SUPER VAC COMPANY LIMITED"
# website_url = "www.supervac.co.th"

# matching = cnameMatcher(company_name,website_title=website_title,copyright_statement=cr_txt,web_url=website_url)
# print(
#     f"{matching.company_name} \n{matching.copyright_statement} \n{matching.website_title} \n{matching.web_domain} "
# )
# print("===========================================================")
# print(
#     matching.result()
# )

#===============================================================================================#

# GET-EMAIL & MATCHING_SCORE
con_prod = MongoClient('localhost',9000,maxPoolSize=None)
con_dev = MongoClient('localhost',9001,maxPoolSize=None)

sansan_sgc_companies = con_prod['customer_proj']['sansan_sg_companies']
website_info_coll = con_dev['websiteinfo']['website_data']
website_info_aspackage_coll = con_dev['websiteinfo']['as_package']
sansan_others2 = con_prod['customer_proj']['sansan_others2']

# updated_data = []
# for elem in tqdm(sansan_others2.find({"updated":{"$exists":False}}, no_cursor_timeout=True, batch_size=1000), ncols=80, total=2226, desc="get email & matching_score"):
#     new_emails = []
#     cr_txt = None
#     crs_txt = None
#     website_title = None
#     site_name = None
#     company_name = elem["company_name"]
#     website_url = elem["company_website"]
#     company_website_match_score = None
    
#     # webinfo_data = website_info_coll.find_one({"website":elem["company_website"],"uid":'4d55575a-20ae-4f31-8f31-30dd36528763'})
#     webinfo_data = website_info_aspackage_coll.find_one({
#         "website":elem["company_website"],'uid':'630e97b7-1f6b-11eb-80f4-da86369e7e3f',
#         "current_url":{"$exists":True}, 
#         })
    
#     if webinfo_data:
#         if "error" in webinfo_data:
#             # updated_data.append( UpdateOne({"_id":elem["_id"]},{"$set":{"website_status":"UNREACHABLE","company_website_match_score":company_website_match_score}}) )
#             continue
#         if "emails" in webinfo_data:
#             if "contact_emails" in webinfo_data["emails"]:
#                 if webinfo_data["emails"]["contact_emails"]: new_emails.extend(webinfo_data["emails"]["contact_emails"])
#             if "other_emails" in webinfo_data["emails"]:
#                 if webinfo_data["emails"]["other_emails"]: new_emails.extend(webinfo_data["emails"]["other_emails"])
#         if "metadata" in webinfo_data:
#             if "title" in webinfo_data["metadata"]: website_title = webinfo_data["metadata"]["title"]
#             if "copyright" in webinfo_data["metadata"]: cr_txt = webinfo_data["metadata"]["copyright"]
#             if "site_name" in webinfo_data["metadata"]: site_name = webinfo_data["metadata"]["site_name"]
#         if "copyright_statement" in webinfo_data:
#             crs_txt = webinfo_data["copyright_statement"]
        
#         # get match_score
#         if not cr_txt and site_name:
#             cr_txt = site_name
#         if not website_title and site_name:
#             website_title = site_name
#         if crs_txt:
#             cr_txt = f"{cr_txt} | {crs_txt}"
#         try:
#             matching = cnameMatcher(company_name,website_title=website_title,copyright_statement=cr_txt,web_url=website_url)
#             company_website_match_score = matching.result()[1]
#             # print(f"matching_result: {matching.result()}")
#             # print(f"matching_result: {company_website_match_score}")
#         except Exception as err:
#             print(f"Error matching: {err}")

#         new_emails.extend(elem["company_emails"])

#         updated_data.append(
#             UpdateOne(
#                 {"_id":elem["_id"]},
#                 {"$set":{
#                     "website_status": "ACTIVE",
#                     "company_emails": list(set(new_emails)),
#                     "company_website_match_score": company_website_match_score,
#                     "updated2": True
#                     }}
#             )
#         )
    
#     if len(updated_data) > 499:
#         try:
#             sansan_others2.bulk_write(updated_data,ordered=False)
#         except Exception as err:
#             print(f"Error bulk_write: {err}")
#         updated_data = []

# if updated_data:
#     sansan_others2.bulk_write(updated_data,ordered=False)



query = {'uid':'f36330ab-3c8f-49af-8256-09e9a8dcafe4','emails.contact_emails':{'$ne':[]},'emails.other_emails':{'$ne':[]},"error":{'$exists':False}}

data_update = []
for elem in tqdm(website_info_coll.find(query, no_cursor_timeout=True, batch_size=100), ncols=80, desc="update sansan"):
    new_emails = []
    try:
        new_emails.extend(elem["emails"]["contact_emails"])
        new_emails.extend(elem["emails"]["other_emails"])
    except Exception as e:
        f"{e}"
    if new_emails:
        data_update.append( UpdateMany({'company_website':elem['website']},{"$set":{"company_emails":new_emails, "new_emails3":True}}) )

if data_update:
    sansan_sgc_companies.bulk_write(data_update,ordered=False)