def write(file_path, content, mode='a'):
    with open(file_path, mode, encoding='utf-8') as file:
        file.write(content)