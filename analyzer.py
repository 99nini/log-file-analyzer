def read_log_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as log_file:
            for line in log_file:
                cleaned_line = line.strip()
                parts = cleaned_line.split(" ", 3)
                
                if len(parts) != 4:
                    print(f"Skipping malformed line: {cleaned_line}")
                    continue
            
                date, time, level, message = parts
                print(f"Date: {date}")
                print(f"Time: {time}")
                print(f"Level: {level}")
                print(f"Message: {message}")
                print("-" * 30)
    
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'.")
        
read_log_file("sample.log")