import os
import json
import sys
from scan_user_dir import scan_user_dir

def load_manifest(root_dir, package_name):
    package_path = os.path.join(root_dir, package_name)
    manifest_path = os.path.join(package_path, "manifest.json")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest file not found in {manifest_path}")

    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    return manifest_data

def check_conflicts(manifest_data, user_data):
    conflicts = {
        "settings": [],
        "modes": [],
        "tags": [],
        "actions": [],
        "lists": [],
    }

    for key in conflicts.keys():
        manifest_set = set(manifest_data.get(key, []))
        user_set = user_data.get(key, set())

        conflicts[key] = manifest_set.intersection(user_set)

    return conflicts

def display_conflicts(conflicts):
    conflict_found = False
    for key, items in conflicts.items():
        if items:
            conflict_found = True
            print(f"Conflicts found in {key}:")
            for item in items:
                print(f" - {item}")
    if not conflict_found:
        print("No conflicts found.")

def main(package_name):
    package_path = os.path.abspath(os.path.join("..", package_name))

    try:
        manifest_data = load_manifest(package_path, package_name)
    except FileNotFoundError as e:
        print(e)
        return

    user_data = scan_user_dir()

    conflicts = check_conflicts(manifest_data, user_data)
    display_conflicts(conflicts)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python conflict_checker.py <package_name>")
        sys.exit(1)

    package_name = sys.argv[1]
    main(package_name)