import argparse
from datetime import datetime
from collections import Counter

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
    
    parser.add_argument(
        "--end-date",
        help="Only include enteries on or before this date"
    )
    
    parser.add_argument(
        "--top",
        type=int,
        default=3,
        help="Number of common errors to display"
    )
    
    return parser.parse_args()

def analyze_log_file(filename, level_filter=None, start_date=None, end_date = None, top_n = 3):
    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    total_entries = 0
    skipped_entries = []
    error_messages = Counter()

    try:
        with open(filename, "r", encoding="utf-8") as log_file:
            for line in log_file:
                cleaned_line = line.strip()
                parts = cleaned_line.split(" ", 3)

                if len(parts) != 4:
                    skipped_entries.append(
                        f"Malformed line: {cleaned_line}"
                    )
                    continue

                date, time, level, message = parts

                if level not in counts:
                    skipped_entries.append(
                        f"Invalid log level: {cleaned_line}"
                    )
                    continue
                
                timestamp_text = f"{date} {time}"
                
                try:
                    converted_timestring = datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    skipped_entries.append(
                        f"Invalid timestamp: {cleaned_line}"
                    )
                    continue
                
                if start_date is not None and converted_timestring < start_date:
                    continue
                
                if end_date is not None and converted_timestring.date() > end_date.date():
                    continue
                
                if level_filter is not None and level != level_filter:
                    continue

                counts[level] += 1
                total_entries += 1
                
                if level == "ERROR":
                    error_messages[message] +=1
                    
            if skipped_entries:
                print("\nSkipped Entries")
                print("-" * 30)

                for entry in skipped_entries:
                    print(entry)        
                    
            top_errors = error_messages.most_common(top_n)
            print("\nMost Common Errors")
            print("-" * 30)
            for position, (message, count) in enumerate(top_errors, start=1):
                print(f"{position}. {message}: {count}")
        
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
    
    end_date = None
    if args.end_date is not None:
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    analyze_log_file(args.filename, args.level, start_date, end_date, args.top)
