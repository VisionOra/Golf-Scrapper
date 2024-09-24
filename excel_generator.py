import json
import os

import pandas as pd

root_json_dir = "facility_type/"  # Change directory for which excel file is creating.
filter_file_name = ["filtered_fields_facility_type.json", "filtered_fields_member_type.json",
                    "filtered_fields_facility_type.json"
                    ]
filter_excel_name = ["filtered_fields_facility_type.xlsx", "filtered_fields_member_type.xlsx",
                     "filtered_fields_facility_type.xlsx"
                     ]


def load_files():
    json_files = os.listdir(root_json_dir)
    return json_files


def load_json_file(file_path):
    """Read a JSON file and return its content as a Python dictionary."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def create_excel_from_payload(payload, filename='output.xlsx'):
    # Convert payload to DataFrame
    df = pd.DataFrame(payload)

    # Drop duplicate entries
    df = df.drop_duplicates()

    # Write DataFrame to Excel file
    df.to_excel(filename, index=False)

    print(f'Excel file "{filename}" created successfully.')


def generate_filtered_data_file(json_files_list):
    list_data = []
    for json_file in json_files_list:
        print(f"LOADING FILE >>> {json_file}")
        resp = load_json_file(f"{root_json_dir}{json_file}")
        list_data.extend(resp.get("results")[0].get("hits"))
        print(len(resp.get("results")[0].get("hits")))

    # Code portion to generate data with filtered fields
    filtered_data = []
    for item in list_data:
        filtered_data.append(
            {
                "objectID": item.get("objectID"),
                "object_type": item.get("object_type"),
                "member_type_label": item.get("member_type_label"),
                "name": item.get("name"),
                "first_name": item.get("first_name"),
                "last_name": item.get("last_name"),
                "facility_name": item.get("facility_name"),
                "member_status": item.get("member_status"),
                "section_location": item.get("section_location"),
                "state_name": item.get("state_name"),
                "job_title": item.get("job_title"),
                "profile_name": item.get("profile_name"),
                "facility_id": item.get("facility_id"),
                "section_name": item.get("section_name"),
                "email": item.get("email"),
                "phone": item.get("phone"),
                "mobile": item.get("mobile"),
            }
        )
    print("DUMPING DATA IN JSON FILE")
    with open(filter_file_name[2], 'w') as json_file:
        json.dump(filtered_data, json_file, indent=4)


def merge_excel_files():
    main_payload = []
    for json_file in filter_file_name:
        filter_file_payload = load_json_file(json_file)
        main_payload.extend(filter_file_payload)
    create_excel_from_payload(main_payload, "merged_excel.xlsx")
    print(f"LEN >> {len(main_payload)}")


if __name__ == '__main__':
    # if not os.path.exists(filter_file_name[2]):
    #     print(f"GENERATING {filter_file_name} File")
    #     json_files_list = load_files()
    #     print(json_files_list)
    #     generate_filtered_data_file(json_files_list)
    # print("FILE FOUND")
    # data = load_json_file(filter_file_name)
    # create_excel_from_payload(data, filter_excel_name[2])  # Change excel file name accordingly
    merge_excel_files()
