from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("")

# Prepare the Actor input
run_input = {
            "searchUrl": "https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3Atrue%2CrecentSearchParam%3A(id%3A3640761801%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3AFUNCTION%2Cvalues%3AList((id%3A4%2Ctext%3ABusiness%2520Development%2CselectionType%3AINCLUDED))))%2Ckeywords%3ADirector%252B)&sessionId=Z9ZM7CjPTdy9YeJa44njEQ%3D%3D",
            "cookie": [{"name": "li_at",
            "value": "",
            "domain": "www.linkedin.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,}],
            "maxResults": 5,
            "deepScrape": False,
            "startPage": 1,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyCountry": "IN",
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
            "minDelay": 5,
            "maxDelay": 30,
        }

# Run the Actor and wait for it to finish
run = client.actor("put actor id").call(run_input=run_input)

# Fetch scraped results from the Actor's dataset.
dataset_items = client.dataset(run['defaultDatasetId']).list_items().items
print(dataset_items)