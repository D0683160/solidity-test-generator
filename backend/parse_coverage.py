import json

def parse_uncovered_functions(coverage_json_path="coverage/coverage.json"):
    uncovered_items = []

    with open(coverage_json_path, "r") as f:
        coverage_data = json.load(f)

    for file, data in coverage_data.items():
        if file.endswith(".sol"):
            for func_name, covered in data["fnMap"].items():
                func_id = func_name
                is_covered = data["f"][func_id] > 0
                if not is_covered:
                    uncovered_items.append(covered["name"])

    return list(set(uncovered_items))  # 不重複

