## Features

- Counts `INFO`, `WARNING`, and `ERROR` entries
- Filters entries by log level
- Filters entries by start and end date
- Skips invalid log entries
- Shows the most common error messages

## Usage

```bash
python analyzer.py sample.log
```

Filter by log level:

```bash
python analyzer.py sample.log --level ERROR
```

Filter by date range:

```bash
python analyzer.py sample.log --start-date 2026-09-13 --end-date 2026-09-13
```

Choose how many common errors to show:

```bash
python analyzer.py sample.log --top 3
```

View all available options:

```bash
python analyzer.py --help
```