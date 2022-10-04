from time import sleep
import requests, json
import os, time

API_KEY = os.getenv("API_KEY")
WAIT_TIME = 1

PDL_COMPANY_SEARCH_URL = "https://api.peopledatalabs.com/v5/company/search"
PDL_PERSON_SEARCH_URL = "https://api.peopledatalabs.com/v5/person/search"
PDL_AUTOCOMPLETE_URL = "https://api.peopledatalabs.com/v5/autocomplete"
PDL_BULK_URL = "https://api.peopledatalabs.com/v5/person/bulk"

all_records = []
HEADERS = {
    'Content-Type': "application/json",
    'X-api-key': API_KEY
}


def generate_company_es_query(industry: str, size: int):
    return {
        "query": {
            "bool": {
                "must": [
                    {"term": {"industry": industry}},
                    {"range": {"employee_count": { "gt": size }}}
                ]
            }
        }
    }


def pdl_company_search(
        industry: str,
        company_size: int,
        num_records: int,
        title_level: str,
        title_role: str
):
    query = generate_company_es_query(industry, company_size)
    params = {
        'query': json.dumps(query),
        'size': num_records
    }
    response = requests.get(
        PDL_COMPANY_SEARCH_URL,
        headers = HEADERS,
        params = params
    ).json()
    if response["status"] == 200:
        data = response['data']
        for record in data:
            time.sleep(WAIT_TIME)
            ES_QUERY = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"job_company_id": record['id']}},
                            {"term": {"job_title_levels": title_level}},
                            {"term": {"job_title_role": title_role}},
                        ]
                    }
                }
            }
            PARAMS = {
                'query': json.dumps(ES_QUERY),
                'size': 10
            }
            response = requests.get(
                PDL_PERSON_SEARCH_URL,
                headers = HEADERS,
                params = PARAMS
            ).json()

            if response["status"] == 200:
                data = response['data']
                profile_data = [record.get('profiles') for record in data]
                if data:
                    all_records.extend([profile for sublist in profile_data for profile in sublist])
            else:
                print("Person Search Error:", response)
    else:
        print("Company Search Error:", response)

    return all_records
