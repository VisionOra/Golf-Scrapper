import json
import pandas as pd


def load_json_file(file_path="Members_data.json"):
    """Read a JSON file and return its content as a Python dictionary."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def create_excel_from_payload(payload, filename='members_excel.xlsx'):
    # Convert payload to DataFrame
    df = pd.DataFrame(payload)
    df = df.drop(columns=['objectID'])
    # Drop duplicate entries
    df = df.drop_duplicates()

    # Write DataFrame to Excel file
    df.to_excel(filename, index=False)

    print(f'Excel file "{filename}" created successfully.')


filter_file_name = ["filtered_fields_member.json", "filtered_fields_facility_type.json"]


def merge_excel_files():
    main_payload = []
    for json_file in filter_file_name:
        filter_file_payload = load_json_file(json_file)
        main_payload.extend(filter_file_payload)
    create_excel_from_payload(main_payload, "merged_excel_updated.xlsx")
    print(f"LEN >> {len(main_payload)}")


if __name__ == '__main__':
    payload = load_json_file()
    filtered_data = []
    for item in payload:
        section_location = ""
        if item.get("section") and item.get('section').get('address'):
            section_location = f"{item.get('section', {}).get('address', {}).get('address1')} {item.get('section', {}).get('address', {}).get('address2')} {item.get('section', {}).get('address', {}).get('address3')}"
        filtered_data.append(
            {
                "objectID": item.get("objectID"),
                "object_type": "member",
                "member_type_label": item.get("type"),
                "name": item.get("displayName"),
                "first_name": item.get("firstName"),
                "last_name": item.get("lastLame"),
                "facility_name": item.get("primaryFacility", {}).get("name") if item.get('primaryFacility') else "",
                "member_status": item.get("memberClassDescription"),
                "section_location": section_location,
                "section_name": item.get('section', {}).get('name', "") if item.get('section') else "",
                "state_name": item.get('section', {}).get('address', {}).get("state", "") if item.get('section') is None else "",
                "job_title": item.get("memberClassDescription"),
                "profile_name": item.get("displayName"),
                "facility_id": item.get("primaryFacility", {}).get('id') if item.get('primaryFacility') else "",
                "email": item.get("publicEmail"),
                "phone": item.get("publicPhone"),
                "mobile": item.get("publicMobile"),
                "address1": item.get("primaryFacility", {}).get('address', {}).get('address1') if item.get('primaryFacility') else "",
                "address2": item.get("primaryFacility", {}).get('address', {}).get('address2') if item.get('primaryFacility') else "",
                "address3": item.get("primaryFacility", {}).get('address', {}).get('address3') if item.get('primaryFacility') else "",
                "address4": item.get("primaryFacility", {}).get('address', {}).get('address4') if item.get('primaryFacility') else ""
            }
        )
    print(filtered_data[0])
    # with open("filtered_fields_member.json", 'w') as json_file:
    #     json.dump(filtered_data, json_file, indent=4)
    merge_excel_files()

