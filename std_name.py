import re
# company name normalizer
term_mappings = {
    "default": {
        "center": "centre", "p/l": "pte ltd", "saint": "st", "tech": "technology", "int'l": "international",
        "engrg": "engineering", "s'pore": "singapore", "corpn": "corporation", "tdg": "trading", "rstnt": "restaurant",
        "agcy": "agency", "assn": "association", "bldg": "building", "comm": "communications", "devlpmnt": "development",
        "elec": "electric", "internatl": "international", "mfg": "manufacturing", "mgt": "management", "ofc": "office",
        "prods": "products", "prod": "products", "prtg": "printing", "schl":    "school", "serv": "service",
        "servs": "services", "transp": "transportation", "trdg": "trading", "advtg": "advertising", "constn": "construction",
        "embdy": "embroidery", "est": "estate", "gdn": "garden",
        "pac":          "pacific",
        "tech":         "technology",
        "coml":         "commercial",
        "equip":        "equipment",
        "hdwe":         "hardware",
        "lab":          "laboratory",
        "telecom":      "telecommunications",
        "acctnts":      "accountants",
        "agt":          "agent",
        "bros":         "brothers",
        "childrens":    "children",
        "exp":          "export",
        "exch":         "exchange",
        "gen":          "general",
        "imp":          "import",
        "intl":         "international",
        "mfr":          "manufacture",
        "mfrs":         "manufacturers",
        "rd":           "road",
        "solrs":        "solicitors",
        "stn":          "station",
        "s'pore":       "singapore",
        "int'l":        "international"
    },

    "singapore":
        {
            "sg":           "singapore"
    },

    "hong kong":
        {
            "hk":           "hong kong",
            "fty":          "factory",
            "ind":          "industrial",
            "internatl":        "international",
            "mfy":          "manufactory",
            "rest":         "restaurant",
            "rests":        "restaurants",
            "ins":          "insurance",
            "kln":          "kowloon",
    },

    "australia":
        {
            "vic":          "victoria",
            "qld":          "queensland",
            "aust":        "australia",
            "B V":          " ",
            "au":           "australia",
            "aust":         "australia",
            "aus":          "australia",
            " w a":         "western australia",
            " s a":         "south australia",
            "associat'n":       "association"
    },

    "others":
    {

    }
}

stop_words = {
    "default":
        ["pteltd",
            "coltd",
            "the",
            "and",
            "pte",
            "ltd",
            "pty",
            "pvt",
            "p/l",
            "llc",
            "private",
            "limited",
            "inc",
            "incorporation",
            "co",
            "company",
            "corp",
            "corporation",
            "p\\s*t",
            "sdn",
            "bhd",
            "pt"
         ],

    "australia": [],

    "singapore": [],

    "india": [],

    "hong kong":
        ["ct"
         ],

    "malaysia":
        [
            "Sendirian",
            "berhad"
    ],

    "indonesia":
        ["cv",
            "sd",
            "ud",
            "sh"
         ],

    "japan":
        ["k\\s*k",
            "y\\s*k"
         ],

    "germany":
        ["gmbh",
            "kg$",
            "und",
            "ag$"
         ],

    "austria":
        ["gmbh",
            "kg$",
            "und",
            "ag$"
         ],

    "switzerland":
        ["gmbh",
            "kg$",
            "ag$",
            "und"
         ],

    "vietnam":
        ["[,.]+jsc$",
            "\\s+jsc$",
            "\\s+joint\\s+stock\\s+company$"
         ],

    "others": []
}

for key in stop_words.keys():
    if key != 'default':
        stop_words[key] = stop_words['default']+stop_words[key]

for key in term_mappings.keys():
    if key != 'default':
        term_mappings[key].update(term_mappings['default'])

ptns_stop = {}
for key in stop_words.keys():
    ptns_stop[key] = re.compile(
        r'\b(' + r'|'.join(stop_words[key]) + r')\b\s*')

ptn_punc = re.compile(r"[^a-z0-9A-Z']")
ptn_punc = re.compile(r"\W|_", re.UNICODE)
ptn_brac = re.compile(r'\([^)]+\)')
ptn_apostrophe = re.compile("'")
ptn_2str = re.compile(r'\s+')


def std_name(name0, country=None, level=0, rm_country=False):

    if name0:
        name = name0.lower()
        if country and rm_country:
            name = re.sub(r'\b'+country.lower()+'$', '', name)
        ptn_stop = ptns_stop['default']
        mappings = term_mappings['default']
        if country and ptns_stop.get(country.lower()):
            ptn_stop = ptns_stop[country.lower()]
        if country and term_mappings.get(country.lower()):
            mappings = term_mappings[country.lower()]

        if level == 0:  # remove punctuations
            name = ptn_punc.sub(' ', name)
            if mappings:
                name = ' '.join([mappings.get(x, x) for x in name.split()])
            name = ptn_apostrophe.sub('', name)

        elif level == 1:  # remove punctuations + brackets
            name = ptn_brac.sub(' ', name)
            name = ptn_punc.sub(' ', name)
            if mappings:
                name = ' '.join([mappings.get(x, x) for x in name.split()])
            name = ptn_apostrophe.sub('', name)

        elif level == 2:  # remove punctuations + stop words
            name = ptn_punc.sub(' ', name)
            if mappings:
                name = ' '.join([mappings.get(x, x) for x in name.split()])
            name = ptn_apostrophe.sub('', name)
            name = ptn_stop.sub(' ', name)

        elif level == 3:  # remove punctuations + bracketed + stop words
            name = ptn_brac.sub(' ', name)
            name = ptn_punc.sub(' ', name)
            if mappings:
                name = ' '.join([mappings.get(x, x) for x in name.split()])
            name = ptn_apostrophe.sub('', name)
            name = ptn_stop.sub(' ', name)

        elif level == 4:  # remove punctures, convert to string
            name = ptn_punc.sub(' ', name)
            name = ptn_apostrophe.sub('', name)
            name = ptn_2str.sub('', name)

        elif level == 5:  # remove punctures, bracket, convert to string
            name = ptn_brac.sub(' ', name)
            name = ptn_punc.sub(' ', name)
            if mappings:
                name = ' '.join([mappings.get(x, x) for x in name.split()])
            name = ptn_apostrophe.sub('', name)
            name = ptn_2str.sub('', name)

        elif level == 6:  # remove punctures, stop words, convert to string
            name = ptn_punc.sub(' ', name)
            if mappings:
                name = ' '.join([mappings.get(x, x) for x in name.split()])
            name = ptn_apostrophe.sub('', name)
            name = ptn_stop.sub(' ', name)
            if rm_country and name[-len(country):] == country.lower():
                name = name[:(-len(country))].strip()
            name = ptn_2str.sub('', name)

        elif level == 7:  # remove punctures, brackets, stop words, convert to string
            name = ptn_brac.sub(' ', name)
            name = ptn_punc.sub(' ', name)
            if mappings:
                name = ' '.join([mappings.get(x, x) for x in name.split()])
            name = ptn_apostrophe.sub('', name)
            name = ptn_stop.sub(' ', name)
            if rm_country and name[-len(country):] == country.lower():
                name = name[:(-len(country))].strip()
            name = ptn_2str.sub('', name)

        name = re.sub(r'\s+', ' ', name).strip()
        return name
    else:
        return None