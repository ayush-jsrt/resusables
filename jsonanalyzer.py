import json
import argparse
import sys
from typing import Any, Union, List, Dict

class JSONAnalyzer:
    def __init__(self, data: Union[Dict, List]):
        self.data = data

    @classmethod
    def load_from_file(cls, filepath: str) -> 'JSONAnalyzer':
        """Loads JSON data from a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(data)
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from '{filepath}': {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
            sys.exit(1)

    def execute_query(self, query: str) -> Any:
        """
        Executes a simple query on the loaded JSON data.
        Supported syntax:
        - Dot notation for keys: key1.key2
        - Array indexing: key1[0].key2
        - '*' wildcard for lists: key1[*].key2 (returns list of values)
        """
        if not query or query == ".":
            return self.data

        parts = self._parse_query(query)
        results = [self.data]

        for part in parts:
            new_results = []
            for item in results:
                if isinstance(item, dict):
                    if part in item:
                        new_results.append(item[part])
                elif isinstance(item, list):
                    if part == "*":
                        new_results.extend(item)
                    elif part.isdigit():
                        idx = int(part)
                        if 0 <= idx < len(item):
                            new_results.append(item[idx])
                
                # Check for array syntax in key like key[0] which splits into key, 0
                # But my parser handles them separately.
            
            results = new_results
            if not results:
                return None
        
        if len(results) == 1:
            return results[0]
        return results

    def _parse_query(self, query: str) -> List[str]:
        """Parses the query string into traversable parts."""
        # Replace brackets with dots to unify parsing
        # key[0] -> key.0
        clean_query = query.replace('[', '.').replace(']', '')
        return [p for p in clean_query.split('.') if p]

    def search_key(self, key_name: str) -> List[Any]:
        """Recursively searches for all values associated with a specific key."""
        results = []
        self._recursive_search(self.data, key_name, results)
        return results

    def _recursive_search(self, current_data: Any, target_key: str, results: List[Any]):
        if isinstance(current_data, dict):
            for k, v in current_data.items():
                if k == target_key:
                    results.append(v)
                self._recursive_search(v, target_key, results)
        elif isinstance(current_data, list):
            for item in current_data:
                self._recursive_search(item, target_key, results)

    def _parse_value(self, value_str: str) -> Any:
        """Parses a string value into a Python type."""
        lowered = value_str.lower()
        if lowered == 'true':
            return True
        if lowered == 'false':
            return False
        if lowered == 'null':
            return None
        if value_str.isdigit():
            return int(value_str)
        try:
            return float(value_str)
        except ValueError:
            return value_str.strip('"').strip("'")

    def apply_filter(self, data: Any, filter_expr: str) -> Any:
        """
        Filters a list of objects based on a condition 'key=value' or 'key!=value'.
        """
        if not isinstance(data, list):
            print("Warning: Filter can only be applied to a list of objects.")
            return data
            
        operator = "="
        if "!=" in filter_expr:
            operator = "!="
            key, value_str = filter_expr.split("!=", 1)
        elif "=" in filter_expr:
            key, value_str = filter_expr.split("=", 1)
        else:
            print("Error: Invalid filter expression. Use 'key=value' or 'key!=value'.")
            return data
            
        key = key.strip()
        target_value = self._parse_value(value_str.strip())
        
        filtered_results = []
        for item in data:
            if not isinstance(item, dict):
                continue
                
            item_value = item.get(key)
            
            if operator == "=":
                if item_value == target_value:
                    filtered_results.append(item)
            elif operator == "!=":
                if item_value != target_value:
                    filtered_results.append(item)
                    
        return filtered_results

def main():
    parser = argparse.ArgumentParser(description="Analyze and query JSON files.")
    parser.add_argument("file", help="Path to the JSON file")
    parser.add_argument("--query", "-q", help="Query string (e.g. 'store.book[0].title')")
    parser.add_argument("--search", "-s", help="Search for all occurrences of a key")
    parser.add_argument("--filter", "-f", help="Filter list results (e.g. 'success!=true')")
    
    args = parser.parse_args()

    analyzer = JSONAnalyzer.load_from_file(args.file)

    if args.query or args.filter:
        result = analyzer.data
        if args.query:
            result = analyzer.execute_query(args.query)
        
        if args.filter:
            result = analyzer.apply_filter(result, args.filter)
            
        print(json.dumps(result, indent=2))
    elif args.search:
        matches = analyzer.search_key(args.search)
        print(f"Found {len(matches)} matches for key '{args.search}':")
        print(json.dumps(matches, indent=2))
    else:
        # Interactive mode
        print("JSON Analyzer Interactive Mode")
        print("Type 'exit' or 'quit' to leave.")
        while True:
            try:
                user_input = input("\nEnter query (or 'search <key>'): ").strip()
                if user_input.lower() in ('exit', 'quit'):
                    break
                
                if user_input.startswith("search "):
                    key = user_input.split(" ", 1)[1]
                    matches = analyzer.search_key(key)
                    print(json.dumps(matches, indent=2))
                else:
                    result = analyzer.execute_query(user_input)
                    print(json.dumps(result, indent=2))
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
