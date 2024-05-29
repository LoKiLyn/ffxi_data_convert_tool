import os
import yaml
import json

def reformat(item_json):
    data = {}
    data["ID"] = item_json["id"]
    data["name"] = item_json["strings"]["name"]
    data["item_type"] = item_json["item_type"]
    data["description"] = item_json["strings"]["description"]
    data["flags"] = ', '.join(map(str, item_json["flags"]))
    data["stack_size"] = item_json["stack_size"]
    equipment_json = {
        "level": item_json["equipment"]["level"],
        "ilevel": item_json["equipment"]["ilevel"],
        "jobs": ', '.join(map(str, item_json["equipment"]["jobs"])),
        "races": ', '.join(map(str, item_json["equipment"]["races"])),
        "slots": ', '.join(map(str, item_json["equipment"]["slots"])),
        "superior_level": item_json["equipment"]["superior_level"],
        "shield_size": item_json["equipment"]["shield_size"],
        "max_charges": item_json["equipment"]["max_charges"],
        "casting_time": item_json["equipment"]["casting_time"],
        "use_delay": item_json["equipment"]["use_delay"],
        "reuse_delay": item_json["equipment"]["reuse_delay"]
    }
    data["equipment"] = equipment_json
    data["icon_bytes"] = item_json["icon_bytes"]
    return data

def convert_yaml_to_json(yaml_folder, json_folder):
    # Ensure the output directory exists
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    
    # Loop through all files in the yaml_folder
    for filename in os.listdir(yaml_folder):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            # Construct full file path
            yaml_file_path = os.path.join(yaml_folder, filename)
            json_file_path = os.path.join(json_folder, filename.replace('.yaml', '.json').replace('.yml', '.json'))

            # Read the YAML file
            with open(yaml_file_path, 'r') as yaml_file:
                yaml_content = yaml.safe_load(yaml_file)

            # Write to the JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(yaml_content, json_file, indent=4)
            
            print(f"Converted {yaml_file_path} to {json_file_path}")

def split_json_array(json_folder):
    for filename in os.listdir(json_folder):
        if filename.endswith('json'):
            # Ensure the output directory exists
            json_folder_path = os.path.join(json_folder, filename.replace('.json', ''))
            if not os.path.exists(json_folder_path):
                os.makedirs(json_folder_path)

            json_file_path = os.path.join(json_folder, filename)
            # Read the input JSON file
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                items = data["items"]
            # Check if the data is a list
            if not isinstance(items, list):
                raise ValueError("The input JSON file does not contain a JSON array with key items.")
            
            # Loop through each item in the JSON array and write to a separate file
            for index, item in enumerate(items):
                item_id = item["id"]
                print(json.dumps(item, indent=4))
                if filename.startswith('armor') or filename.startswith('weapons'):
                    data_reformat = reformat(item)
                else:
                    data_reformat = item
                output_file = os.path.join(json_folder_path, f"{item_id}.json")
                with open(output_file, 'w') as out_file:
                    json.dump(data_reformat, out_file, indent=4)
                print(f"Created {output_file}")


# Example usage
yaml_folder = './yaml'
json_folder = './json'
convert_yaml_to_json(yaml_folder, json_folder)
split_json_array(json_folder)