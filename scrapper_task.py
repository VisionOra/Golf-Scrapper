import json
import os

import requests
from constants import url, headers, dirs
from filters import members_filter, section_filter, member_type_label, member_certification_label, member_certification, \
    results_count, facility_type_label, facility_type_filter


def create_directory():
    # Create directory, if it does not exist
    for directory_path in dirs:
        os.makedirs(directory_path, exist_ok=True)
        print(f'Directory "{directory_path}" created or already exists.')


def scrape_data(filter_1, label, json_folder_name):
    for member in filter_1:
        for section in section_filter:

            data = {
                "requests": [
                    {
                        "indexName": "MemberFacilityDirectory",
                        "params": f"query=&hitsPerPage={results_count}&maxValuesPerFacet=100&page=0&highlightPreTag=<ais-highlight-0000000000>&highlightPostTag=</ais-highlight-0000000000>&facets=[\"_geoloc\",\"zip\",\"member_type_label\",\"programHistory.programCode\",\"facility_type_label\",\"section_name\"]&tagFilters=&facetFilters=[[\"section_name:{section}\"],[\"{label}:{member}\"]]"
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=data)
            data = response.json()
            print(f"GETTING RECORD: {member} --- {section}")
            print(f"LENGTH OF RECORDS: {len(data.get('results', [])[0].get('hits', []))}")
            file_path = f"{json_folder_name}/{member}_{section}.json"
            if len(data.get('results', [])[0].get('hits', [])) > 0:
                # Dumping JSON data into a file
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                print(f"Data has been written to {file_path}")


if __name__ == '__main__':
    create_directory()
    # scrape_data(members_filter, member_type_label, dirs[0]) # With members type
    # scrape_data(member_certification, member_certification_label, dirs[1])
    scrape_data(facility_type_filter, facility_type_label, dirs[2])
