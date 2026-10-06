import argparse
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze a log file and summarise its entries."
    )
    
    parser.add_argument(
        "filename",
        help="Path to the log file"
    )
    
    parser.add_argument(
        "-1",
        "--level",
        choices=["INFO", "WARNING", "ERROR"],
        help="Only include entries with this log level"
    )
    
    parser.add_argument(
        "--start-date",
        help="Only include entries on or after this date"
    )
    
    return parser.parse_args()

def analyze_log_file(filename, level_filter=None, start_date=None):
    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }
    print(f"Start date received: {start_date}")

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
                
                timestamp_text = f"{date} {time}"
                
                try:
                    converted_timestring = datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print(f"Skipping invalid timestamp: {cleaned_line}")
                    continue
                
                if start_date is not None and converted_timestring < start_date:
                    continue
                
                if level_filter is not None and level != level_filter:
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

if __name__ == "__main__":
    args = parse_arguments()
    
    start_date = None
    if args.start_date is not None:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    
    analyze_log_file(args.filename, args.level, start_date)
    