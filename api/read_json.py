import json

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Example usage
if __name__ == "__main__":
    file_path = 'path_to_your_json_file.json'
    data = read_json(file_path)
    print(data)
