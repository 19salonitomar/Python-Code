import re

def get_functions_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        functions = re.findall(r"def\s+(\w+)\s*\(", content)
        return len(functions), functions

if __name__ == "__main__":
    file_path = "C:\\Users\\tomar\\Desktop\\Python Practice\\OneClick\\Email.py"  
    count, function_names = get_functions_from_file(file_path)
    print(f"Total number of functions: {count}")
    print("Function names:")
    for name in function_names:
        print(name)
