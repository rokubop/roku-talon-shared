import ast
from dataclasses import dataclass, field
import json
import os
import re

"""
Script that creates manifest.json file for each CREATE_MANIFEST_DIRS

Usage: `python ./scripts/manifest_builder.py`
"""

CREATE_MANIFEST_DIRS = [
    # 'drag_mode',
    # 'dynamic_noises',
    # 'face_tester',
    # 'game_tools',
    # 'mouse_move_adv',
    # 'parrot_config',
    # 'vgamepad',
    # 'roku_games/celeste',
    # 'roku_games/hi_fi_rush',
    # 'roku_games/rdr2',
    # 'roku_games/sheepy',
    # 'roku_games/stray',
    # 'roku_games/talos_2',
    '../../talon-ui-elements'
]

ENTITIES = ["captures", "lists", "modes", "scopes", "settings", "tags", "actions"]
MOD_ATTR_CALLS = ["setting", "tag", "mode", "list"]
NAMESPACES = ["user", "edit", "core", "app", "code"]

@dataclass
class Entities:
    captures: set = field(default_factory=set)
    lists: set = field(default_factory=set)
    modes: set = field(default_factory=set)
    scopes: set = field(default_factory=set)
    settings: set = field(default_factory=set)
    tags: set = field(default_factory=set)
    actions: set = field(default_factory=set)

@dataclass
class AllEntities:
    contributes: Entities = field(default_factory=Entities)
    depends: Entities = field(default_factory=Entities)

class ParentNodeVisitor(ast.NodeVisitor):
    """A helper visitor class to set the parent attribute for each node."""
    def __init__(self):
        self.parent = None

    def visit(self, node):
        node.parent = self.parent
        previous_parent = self.parent
        self.parent = node
        super().visit(node)
        self.parent = previous_parent

class EntityVisitor(ParentNodeVisitor):
    def __init__(self, all_entities: AllEntities):
        super().__init__()
        self.all_entities = all_entities

    def visit_Attribute(self, node):
        # Check for actions like actions.user.something, actions.edit.something, or actions.core.something
        if isinstance(node.value, ast.Attribute):
            if node.value.attr in NAMESPACES:
                if isinstance(node.value.value, ast.Name) and node.value.value.id == 'actions':
                    # Construct the full action name
                    full_action_name = f"{node.value.attr}.{node.attr}"
                    if full_action_name not in self.all_entities.depends.actions:
                        self.all_entities.depends.actions.add(full_action_name)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        try:
            # function's parent is a class decorated with action_class
            if isinstance(node.parent, ast.ClassDef):
                class_def = node.parent
                for dec in class_def.decorator_list:
                    # @x.action_class(...)
                    if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                        if dec.func.attr == 'action_class':
                            if isinstance(dec.args[0], ast.Constant):
                                # @ctx.action_class("context")
                                context = dec.args[0].value
                                full_action_name = f"{context}.{node.name}"
                                if full_action_name not in self.all_entities.depends.actions:
                                    self.all_entities.depends.actions.add(full_action_name)
                    # @x.action_class
                    elif isinstance(dec, ast.Attribute) and dec.attr == 'action_class':
                        full_action_name = f"user.{node.name}"
                        if full_action_name not in self.all_entities.contributes.actions:
                            self.all_entities.contributes.actions.add(full_action_name)

            # function directly decorated with action
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                    if dec.func.attr == 'action' and isinstance(dec.args[0], ast.Constant):
                        # Assume full action name is already provided in the decorator
                        full_action_name = dec.args[0].value
                        if full_action_name not in self.all_entities.contributes.actions:
                            self.all_entities.contributes.actions.add(full_action_name)

        except Exception as e:
            print(f"Error processing function definition: {e}")
        finally:
            self.generic_visit(node)



    def visit_Assign(self, node):
        try:
            if isinstance(node.targets[0], ast.Attribute):
                target = node.targets[0].attr
                value = node.value

                # Handle lists (e.g., ctx.lists["user.symbol_key"] = {...})
                if isinstance(node.targets[0].value, ast.Attribute) and node.targets[0].value.attr == "lists":
                    if isinstance(value, ast.Dict) and target not in self.all_entities.depends.lists:
                        self.all_entities.depends.lists.add(target)

                # Handle tags (e.g., ctx.tags = ["user.tabs"])
                elif target == "tags":
                    if isinstance(value, ast.List):
                        for elt in value.elts:
                            if isinstance(elt, ast.Constant):
                                self.all_entities.depends.tags.add(elt.value)

            if isinstance(node.targets[0], ast.Attribute) and node.targets[0].attr == 'matches':
                if isinstance(node.value, ast.Constant):
                    full_string = node.value.value
                elif isinstance(node.value, ast.JoinedStr):
                    full_string = "".join(
                        value.value if isinstance(value, ast.Constant) else "" for value in node.value.values
                    )
                else:
                    full_string = ""

                matches = re.findall(r'(mode|tag):\s*([\w\.]+)', full_string)
                for match_type, match_value in matches:
                    if match_type == 'mode':
                        if match_value not in self.all_entities.depends.modes:
                            self.all_entities.depends.modes.add(match_value)
                    elif match_type == 'tag':
                        if match_value not in self.all_entities.depends.tags:
                            self.all_entities.depends.tags.add(match_value)

        except Exception as e:
            print(f"Error processing assignment: {e}")
        finally:
            self.generic_visit(node)

    def visit_Call(self, node):
        try:
            if isinstance(node.func, ast.Attribute):
                func_attr = node.func.attr
                if func_attr in MOD_ATTR_CALLS:
                    entity_name = None

                    # Handle positional arguments
                    if node.args and isinstance(node.args[0], ast.Constant):
                        entity_name = node.args[0].value

                    # Handle keyword arguments
                    if not entity_name and node.keywords:
                        for kw in node.keywords:
                            if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                                entity_name = kw.value.value

                    if entity_name and func_attr in MOD_ATTR_CALLS:
                        attr_name = func_attr + 's'
                        getattr(self.all_entities.contributes, attr_name).add(f"user.{entity_name}")

            # Handle actions.user.something calls
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Attribute):
                if node.func.value.attr in NAMESPACES:
                    # Capture the full name, including the prefix
                    action_name = f"{node.func.value.attr}.{node.func.attr}"
                    if action_name not in self.all_entities.depends.actions:
                        self.all_entities.depends.actions.add(action_name)

            # Handle something.get('user.some_setting')
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'get' and isinstance(node.func.value, ast.Name) and node.func.value.id == 'settings':
                arg = node.args[0]
                if isinstance(arg, ast.Constant):
                    entity_name = arg.value
                    if entity_name not in self.all_entities.depends.settings:
                        self.all_entities.depends.settings.add(entity_name)

        except Exception as e:
            print(f"Error processing call: {e}")
        finally:
            self.generic_visit(node)

def parse_file(file_path: str, all_entities: AllEntities) -> None:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        tree = ast.parse(file_content)
        visitor = EntityVisitor(all_entities)
        visitor.visit(tree)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

def process_folder(folder_path: str) -> AllEntities:
    all_entities = AllEntities()

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                parse_file(file_path, all_entities)

    return all_entities

def entity_extract(folder_path: str) -> AllEntities:
    if not os.path.isdir(folder_path):
        raise ValueError(f"The provided path is not a directory: {folder_path}")

    return process_folder(folder_path)

def update_manifest(package_dir: str, manifest_data) -> None:
    manifest_path = os.path.join(package_dir, 'manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest_data, f, indent=2)

def prune_empty_arrays(data):
    """
    Recursively prune empty arrays from the dictionary.
    """
    if isinstance(data, dict):
        # Recursively prune within each dictionary
        return {k: prune_empty_arrays(v) for k, v in data.items() if not (isinstance(v, list) and len(v) == 0)}
    return data

def prune_manifest_data(manifest_data):
    """
    Prune empty arrays from the 'contributes' and 'depends' sections of the manifest data.
    """
    if 'contributes' in manifest_data:
        manifest_data['contributes'] = prune_empty_arrays(manifest_data['contributes'])

    if 'depends' in manifest_data:
        manifest_data['depends'] = prune_empty_arrays(manifest_data['depends'])

    return manifest_data

def load_existing_manifest(package_dir: str) -> dict:
    manifest_path = os.path.join(package_dir, 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def create_or_update_manifest() -> None:
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    print(f"Packages path: {root_path}")

    if not os.path.exists(root_path):
        print(f"Error: Packages directory not found at {root_path}")
        return

    for relative_dir in CREATE_MANIFEST_DIRS:
        full_package_dir = os.path.abspath(os.path.join(root_path, relative_dir))

        if os.path.isdir(full_package_dir):
            existing_manifest_data = load_existing_manifest(full_package_dir)
            new_entity_data = entity_extract(full_package_dir)

            for key in ENTITIES:
                contributes_set = sorted(list(getattr(new_entity_data.contributes, key)))
                depends_filtered = sorted([
                    entity for entity in getattr(new_entity_data.depends, key)
                    if entity not in contributes_set
                ])
                setattr(new_entity_data.contributes, key, contributes_set)
                setattr(new_entity_data.depends, key, depends_filtered)

            new_manifest_data = {
                "name": existing_manifest_data.get("name", os.path.basename(full_package_dir)),
                "description": existing_manifest_data.get("description", "Auto-generated manifest."),
                "version": existing_manifest_data.get("version", "0.1.0"),
                "contributes": vars(new_entity_data.contributes),
                "depends": vars(new_entity_data.depends)
            }

            new_manifest_data = prune_manifest_data(new_manifest_data)
            update_manifest(full_package_dir, new_manifest_data)
            print(f"Manifest updated for {full_package_dir}")

if __name__ == "__main__":
    create_or_update_manifest()