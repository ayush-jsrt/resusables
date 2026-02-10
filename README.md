# resusables

## JSON Analyzer

`jsonanalyzer.py` is a command-line tool to query and search within JSON files.

### Usage

**Basic Query (Dot Notation):**
```bash
python jsonanalyzer.py path/to/file.json --query "store.book[0].title"
```

**Search for a Key:**
```bash
python jsonanalyzer.py path/to/file.json --search "price"
```

**Filter Results:**
To filter a list of objects based on a key-value pair:
```bash
python jsonanalyzer.py path/to/file.json --filter "success!=true"
```
You can also combine query and filter:
```bash
python jsonanalyzer.py path/to/file.json --query "store.book" --filter "price>10"
```
(Note: currently only supports `=` and `!=` operators, strict typed comparison)

**Interactive Mode:**
Simply run the script with the file path:
```bash
python jsonanalyzer.py path/to/file.json
```
Then type your queries in the prompt.
