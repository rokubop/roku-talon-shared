import os
import json
import re
import tokenize
from io import StringIO

"""
update_manifests.py script

This script is used to generate/update the manifest file for each
directory at '../{folders}'. It will scan and accumulate all actions,
modes, settings, tags, and dependencies and update the manifest.json
"""

PACKAGE_DIRS = [
    '../drag_mode',
    '../dynamic-noises',
    '../game_tools',
    '../mouse_move_adv',
    '../parrot_config',
    '../ui_elements',
    '../vgamepad',
    '../roku_games/celeste',
    '../roku_games/hi_fi_rush',
    '../roku_games/rdr2',
    '../roku_games/sheepy',
    '../roku_games/stray',
    '../roku_games/talos_2',
]

def find_dependencies(content, known_entities):
    """
    Find all `user.something` references that are not in the known_entities list.
    """
    dependencies = []

    tokens = tokenize.generate_tokens(StringIO(content).readline)

    for token_type, token_string, _, _, _ in tokens:
        if token_type == tokenize.NAME and token_string == 'user':
            next_token = next(tokens, None)
            if next_token and next_token.type == tokenize.OP and next_token.string == '.':
                next_token = next(tokens, None)
                if next_token and next_token.type == tokenize.NAME:
                    reference = next_token.string
                    if reference not in known_entities:
                        dependencies.append(reference)
    print(f"Found dependencies: {len(dependencies)}")

    return dependencies

def scan_for_non_package_user_references(package_dir, known_entities):
    non_package_user_refs = []

    for root, dirs, files in os.walk(package_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        dependencies = find_dependencies(content, known_entities)
                        non_package_user_refs.extend(dependencies)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return non_package_user_refs

def omit_comments_and_docstrings(code):
    """
    Omit comments and docstrings from the given code.
    """
    pattern = re.compile(
        r'(""".*?"""|\'\'\'.*?\'\'\'|#.*?$)', re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, '', code)

def extract_actions(content):
    """
    Extract all method names within a class decorated with @mod.action_class.
    """
    actions = []

    class_regex = re.compile(r'@mod\.action_class\s*class\s+(\w+):')
    # Match def statements with 4 spaces of indentation (not inner functions)
    def_regex = re.compile(r'^\s{4}def\s+(\w+)\s*\(', re.MULTILINE)

    for class_match in class_regex.finditer(content):
        class_name = class_match.group(1)
        print(f"Found action class: {class_name}")

        class_start = class_match.end()
        class_end = len(content)  # Default to end of content

        class_body = content[class_start:class_end]
        class_body = omit_comments_and_docstrings(class_body)

        method_names = def_regex.findall(class_body)
        actions.extend(f"user.{method_names}" for method_names in method_names)
        print(f"Methods found in {class_name}: {method_names}")

    return actions

def parse_arguments(arguments_string, entity_type):
    """
    Parse the first positional argument or the 'name' keyword argument for settings, tags, or modes.
    """
    print(f"Parsing {entity_type} arguments: {arguments_string}")

    name_match = re.search(r'name\s*=\s*"([^"]+)"', arguments_string)

    if name_match:
        name = name_match.group(1)
    else:
        first_param_match = re.match(r'\s*"([^"]+)"', arguments_string)
        name = first_param_match.group(1) if first_param_match else None

    if name:
        print(f"Found {entity_type} name: {name}")
    else:
        print(f"No valid {entity_type} name found")

    return f"user.{name}" if name else None

def load_existing_manifest(package_dir):
    manifest_path = os.path.join(package_dir, 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def scan_and_extract_metadata(package_dir, existing_manifest_data=None):
    manifest_data = {
        "name": os.path.basename(package_dir) if "name" not in existing_manifest_data else existing_manifest_data["name"],
        "description": "Auto-generated manifest." if "description" not in existing_manifest_data else existing_manifest_data["description"],
        "version": "0.1.0" if "version" not in existing_manifest_data else existing_manifest_data["version"],
        "lists": [],
        "modes": [],
        "settings": [],
        "tags": [],
        "actions": [],
        "dependencies": [],
    }

    entity_regex = re.compile(r'mod\.(setting|tag|mode|list)\(\s*(.*?)\s*\)', re.DOTALL)

    for root, dirs, files in os.walk(package_dir):
        # Skip all hidden folders (those starting with a dot)
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Find all mod.setting(...), mod.tag(...), and mod.mode(...) occurrences
                        entity_calls = entity_regex.findall(content)
                        print(f"Found {len(entity_calls)} entities in {file_path}")
                        for entity_type, arguments_string in entity_calls:
                            entity_name = parse_arguments(arguments_string, entity_type)
                            if entity_name:
                                manifest_data[f"{entity_type}s"].append(entity_name)

                        action_methods = extract_actions(content)
                        manifest_data["actions"].extend(action_methods)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return manifest_data

def update_manifest(package_dir, manifest_data):
    manifest_path = os.path.join(package_dir, 'manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest_data, f, indent=2)

def create_or_update_manifest():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    print(f"Packages path: {root_path}")

    if not os.path.exists(root_path):
        print(f"Error: Packages directory not found at {root_path}")
        return


    for relative_dir in PACKAGE_DIRS:
        full_package_dir = os.path.abspath(os.path.join(root_path, relative_dir))
        known_entities = set()

        if os.path.isdir(full_package_dir):
            existing_manifest_data = load_existing_manifest(full_package_dir)
            new_manifest_data = scan_and_extract_metadata(full_package_dir, existing_manifest_data)
            known_entities.update(new_manifest_data["settings"])
            known_entities.update(new_manifest_data["modes"])
            known_entities.update(new_manifest_data["tags"])
            known_entities.update(new_manifest_data["actions"])
            known_entities = [entity.split('user.')[1] for entity in known_entities]
            deps = scan_for_non_package_user_references(full_package_dir, known_entities)
            new_manifest_data["dependencies"] = list(set(f"user.{dep}" for dep in deps))
            new_manifest_data["settings"] = list(set(new_manifest_data["settings"]))
            new_manifest_data["modes"] = list(set(new_manifest_data["modes"]))
            new_manifest_data["tags"] = list(set(new_manifest_data["tags"]))
            new_manifest_data["actions"] = list(set(new_manifest_data["actions"]))
            new_manifest_data["lists"] = list(set(new_manifest_data["lists"]))
            for key in ["settings", "modes", "actions", "tags", "lists", "dependencies"]:
                new_manifest_data[key].sort()

            update_manifest(full_package_dir, new_manifest_data)
            print(f"Found {len(deps)} non-package user references")
            print(f"Manifest updated for {full_package_dir}")

if __name__ == "__main__":
    create_or_update_manifest()