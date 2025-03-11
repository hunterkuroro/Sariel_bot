import json

def create_json(file_path):
    data = {f'variable_{i}': i for i in range(1, 11)}
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Example usage
if __name__ == "__main__":
    file_path = 'variable_settings.json'
    create_json(file_path)
    print(f'JSON file created at {file_path}')
    
    data = read_json(file_path)
    print(f'Read JSON data: {data}')
