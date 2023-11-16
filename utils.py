def check_json_format(data):
    try:
        # Check if the required keys exist in the data dictionary
        required_keys = [
            "Contributors",
            "Source",
            "URL",
            "Categories",
            "Definition",
            "Input_language",
            "Output_language",
            "Instruction_language",
            "Domains",
            "Positive Examples",
            "Instances"
        ]
        for key in required_keys:
            if key not in data:
                return False, f"Key '{key}' is missing in the JSON data."
        # Check correctness within sub-structures
        if not isinstance(data.get("Source"), list):
            return False, "Key 'Source' should be a list."
        if not isinstance(data.get("URL"), str):
            return False, "Key 'URL' should be a string."
        if not isinstance(data.get("Contributors"), list):
            return False, "Key 'Contributors' should be a list."
        if not isinstance(data.get("Categories"), list):
            return False, "Key 'Categories' should be a list."
        if not isinstance(data.get("Definition"), list) or not all(isinstance(item, str) for item in data["Definition"]):
            return False, "Key 'Definition' should be a list of strings."
        if not isinstance(data.get("Input_language"), list) or not all(isinstance(item, str) for item in data["Input_language"]):
            return False, "Key 'Input_language' should be a list of strings."
        if not isinstance(data.get("Output_language"), list) or not all(isinstance(item, str) for item in data["Output_language"]):
            return False, "Key 'Output_language' should be a list of strings."
        if not isinstance(data.get("Instruction_language"), list) or not all(isinstance(item, str) for item in data["Instruction_language"]):
            return False, "Key 'Instruction_language' should be a list of strings."
        if not isinstance(data.get("Domains"), list) or not all(isinstance(item, str) for item in data["Domains"]):
            return False, "Key 'Domains' should be a list of strings."
        for example in data.get("Positive Examples", []):
            if not isinstance(example, dict) or not isinstance(example.get("input"), str) or not isinstance(example.get("output"), str):
                return False, "Each 'Positive Examples' entry should be a dictionary with 'input' and 'output' keys, and both keys should be strings."
        if len(data.get("Positive Examples", [])) != 2:
            return False, "The 'Positive Examples' list should contain exactly two elements."
        for instance in data.get("Instances", []):
            if not isinstance(instance, dict) or not isinstance(instance.get("id"), str) or not isinstance(instance.get("input"), str) or not isinstance(instance.get("output"), list) or len(instance.get("output", [])) != 1 or not isinstance(instance.get("output", [])[0], str):
                return False, "Each 'Instances' entry should be a dictionary with 'id', 'input', and 'output' keys. 'id', 'input', and 'output' should have specific data types and formats."
        return True, "JSON data format is valid."
    except Exception as e:
        return False, str(e)