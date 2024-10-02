import json

import requests
import pandas as pd


def get_member(operation_name, member_id):
    url = "https://developers.pga.org/graphql"
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "origin": "https://directory.pga.org",
        "priority": "u=1, i",
        "referer": "https://directory.pga.org/",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    # JSON data for the POST request
    data = {
        "operationName": operation_name,
        "variables": {"id": member_id},
        "query": """
        query GetMember($id: ID!) {
          memberByUid(universalId: $id) {
            firstName
            lastName
            class
            memberClassDescription
            type
            informalName
            displayName
            photo
            certified
            certifiedProfessional
            masterProfessional
            specialized
            specializedProfessional
            address {
              address1
              address2
              address3
              address4
              city
              country
              state
              zip
              __typename
            }
            section {
              id
              name
              address {
                address1
                address2
                address3
                address4
                city
                state
                zip
                __typename
              }
              primaryFacility {
                phoneNumber
                geolocation {
                  lat
                  lng
                  __typename
                }
                __typename
              }
              __typename
            }
            publicPhone
            publicMobile
            role
            primaryEmail
            publicEmail
            primaryFacility {
              id
              name
              phoneNumber
              geolocation {
                lat
                lng
                __typename
              }
              address {
                address1
                address2
                address3
                address4
                city
                country
                state
                zip
                __typename
              }
              __typename
            }
            expertise {
              id
              name
              __typename
            }
            social {
              facebook
              linkedin
              twitter
              youtube
              instagram
              website
              __typename
            }
            personalCertifications {
              description
              effectiveYear
              __typename
            }
            officialCertifications {
              description
              effectiveYear
              __typename
            }
            personalAwards {
              description
              effectiveYear
              __typename
            }
            officialAwards {
              description
              effectiveYear
              __typename
            }
            personalAffiliations {
              description
              effectiveYear
              __typename
            }
            officialAffiliations {
              description
              effectiveYear
              __typename
            }
            overview
            viewingPermissions {
              viewProfilePublic
              viewEmailPublic
              __typename
            }
            __typename
          }
        }
        """
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"


def call_api_for_address(df: pd.DataFrame, output_excel_path: str = "output_merged.xlsx"):
    operation_name = "GetMember"

    # List to store the address information
    addresses = []
    count = 0
    data = []
    json_file = "Members_data.json"
    # Iterate over the DataFrame and call the API for each objectID
    for index, row in df.iterrows():
        object_id = row['objectID']  # Get the objectID from the DataFrame
        if row["object_type"] == "member":
            print(f"CALLING FOR MEMBER: {object_id}")
            response = get_member(operation_name, object_id)
            data.append(response.get("data", {}).get("memberByUid"))
        else:
            print("NOT A MEMBER")
    with open(json_file, "w") as j_file:
        json.dump(data, j_file, indent=4)
        # Check if we have a valid response
        # if response and 'data' in response and response['data']['memberByUid']:
        #     address_data = response['data']['memberByUid']['address']
        #
        #     # Construct the address as a single string
        #     address = f"{address_data.get('address1', '')}, {address_data.get('address2', '')}, {address_data.get('city', '')}, {address_data.get('state', '')}, {address_data.get('zip', '')}, {address_data.get('country', '')}"
        #     print(f"ADDRESS: {address}")
        #     addresses.append(address)
        # else:
        #     addresses.append("Address not found")  # Fallback if no valid response

    # Add the address data as a new column in the original DataFrame
    # df['Address'] = addresses

    # Save the updated DataFrame to an Excel file
    # df.to_excel(output_excel_path, index=False)

    # print(f"Updated data with addresses saved to {output_excel_path}")



