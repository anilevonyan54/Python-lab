def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            print("File content read successfully:")
            print(data)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while trying to read '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

file_path = 'data.txt'

read_file(file_path)
