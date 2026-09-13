def read_log_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as log_file:
            for line in log_file:
                print(line.strip())
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'.")
        
read_log_file("sample.log")