import sys

def analyze_log_file(filename):
    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    total_entries = 0

    try:
        with open(filename, "r", encoding="utf-8") as log_file:
            for line in log_file:
                cleaned_line = line.strip()
                parts = cleaned_line.split(" ", 3)

                if len(parts) != 4:
                    print(f"Skipping malformed line: {cleaned_line}")
                    continue

                date, time, level, message = parts

                if level not in counts:
                    print(f"Skipping invalid log level: {cleaned_line}")
                    continue

                counts[level] += 1
                total_entries += 1

        print("\nLog Summary")
        print("-" * 30)
        print(f"Total entries: {total_entries}")
        print(f"INFO: {counts['INFO']}")
        print(f"WARNING: {counts['WARNING']}")
        print(f"ERROR: {counts['ERROR']}")

    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'.")

if len(sys.argv) != 2:
    print("Usage: python analyzer.py <log-file>")
else:
    analyze_log_file(sys.argv[1])