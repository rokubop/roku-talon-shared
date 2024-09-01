# import os
# import sys
# import json
# import string
# import shutil
# import subprocess

# RED = '\033[0;31m'
# GREEN = '\033[0;32m'
# YELLOW = '\033[1;33m'
# CYAN = '\033[0;36m'
# GRAY = '\033[0;37m'
# NC = '\033[0m'  # No Color

# def print_error(message):
#     print(f"{RED}Error:{NC} {message}")

# def print_warning(message):
#     print(f"{YELLOW}Warning:{NC} {message}")

# def print_info(message):
#     print(f"{GREEN}{message}{NC}")

# def index_to_char(index):
#     return chr(97 + index)

# def char_to_index(char):
#     return ord(char) - 97

# def load_manifest(package_dir):
#     manifest_path = os.path.join(package_dir, 'manifest.json')
#     if os.path.isfile(manifest_path):
#         with open(manifest_path, 'r') as f:
#             return json.load(f)
#     return {}

# def find_talon_dir():
#     dir = os.path.dirname(os.path.abspath(__file__))
#     while not os.path.isfile(os.path.join(dir, 'talon.log')):
#         parent_dir = os.path.dirname(dir)
#         if parent_dir == "/" or parent_dir == ".":
#             print_error("Unable to find talon dir where the 'talon.log' file is located.")
#             sys.exit(1)
#         dir = parent_dir
#     return dir

# def copy_package(source_path, target_path):
#     try:
#         if os.path.exists(target_path):
#             print_warning(f"Target directory {target_path} already exists. Backing up...")
#             shutil.move(target_path, f"{target_path}_backup")

#         shutil.copytree(source_path, target_path)
#         print_info(f"Copied {source_path} to {target_path}")
#     except Exception as e:
#         print_error(f"Failed to copy {source_path} to {target_path}: {str(e)}")

# def get_package_version(package_dir):
#     manifest = load_manifest(package_dir)
#     return manifest.get('version', 'Unknown')

# def display_package_info(package, package_dir):
#     manifest = load_manifest(package_dir)
#     if manifest:
#         print(f"  Name: {manifest.get('name', package)}")
#         print(f"  Description: {manifest.get('description', 'No description')}")
#         print(f"  Version: {manifest.get('version', '0.1.0')}")
#         print(f"  Lists: {manifest.get('lists', [])}")
#         print(f"  Modes: {manifest.get('modes', [])}")
#         print(f"  Settings: {manifest.get('settings', [])}")
#         print(f"  Tags: {manifest.get('tags', [])}")
#         print(f"  Actions: {manifest.get('actions', [])}")
#         print(f"  Dependencies: {manifest.get('dependencies', [])}")

#     input("\nPress Enter to return to the package selection...")

# def run_conflict_checker(package_name):
#     script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
#     conflict_checker_path = os.path.join(script_dir, 'conflict_checker.py')  # Path to conflict_checker.py

#     try:
#         result = subprocess.run(['python', conflict_checker_path, package_name], capture_output=True, text=True)
#         if result.returncode == 0:
#             print_info(result.stdout)
#         else:
#             print_warning(result.stderr)
#     except Exception as e:
#         print_error(f"Failed to run conflict checker for {package_name}: {str(e)}")


# def main():
#     if len(sys.argv) < 2:
#         print_error("No root folder specified. Usage: python package_manager.py {root_folder}")
#         sys.exit(1)

#     packages_root_dir = sys.argv[1]
#     TARGET_DIR = os.path.basename(os.path.normpath(packages_root_dir))
#     talon_dir = find_talon_dir()
#     user_dir = os.path.join(talon_dir, 'user')
#     symlink_target_dir = os.path.join(user_dir, TARGET_DIR)
#     os.makedirs(symlink_target_dir, exist_ok=True)

#     packages = [d for d in os.listdir(packages_root_dir)
#                 if os.path.isdir(os.path.join(packages_root_dir, d)) and
#                 not d.startswith('.') and
#                 os.path.isfile(os.path.join(packages_root_dir, d, 'manifest.json'))]

#     if not packages:
#         print_warning("No packages found.")
#         sys.exit(0)

#     installed_packages = {}
#     for package in os.listdir(symlink_target_dir):
#         installed_package_dir = os.path.join(symlink_target_dir, package)
#         if os.path.isdir(installed_package_dir):
#             installed_version = get_package_version(installed_package_dir)
#             installed_packages[package] = installed_version

#     while True:
#         print("Select packages to copy to /user dir (e.g., adf for multiple selections):")
#         for i, package in enumerate(packages):
#             current_version = get_package_version(os.path.join(packages_root_dir, package))
#             installed_version = installed_packages.get(package)
#             status = f"{YELLOW}(not installed){NC}"
#             if installed_version:
#                 if current_version == installed_version:
#                     status = f"{GREEN}(installed, version {installed_version}){NC}"
#                 else:
#                     status = f"{CYAN}(installed, version {installed_version}, upgrade available: {current_version}){NC}"
#             char = index_to_char(i)
#             print(f"{GREEN}{char}{NC}) {package} ({current_version}) {status}")

#         # for i, package in enumerate(packages):
#         #     status = "(installed)" if package in installed_packages else "(not installed)"
#         #     char = index_to_char(i)
#         #     print(f"{GREEN}{char}{NC}) {package} {GRAY}({get_package_version(package)}){NC} {status}")
#             # display_package_info(package, os.path.join(packages_root_dir, package))
#         print_info(f"{GREEN}*{NC}) All packages")
#         print_info(f"{GREEN}info [letter]{NC}) View detailed information about a package")
#         print_info(f"{GREEN}check [letter]{NC}) Check for conflicts between a package and user directory")
#         print_info(f"{GREEN}q{NC}) Quit")

#         choices = input("Enter your choice(s): ").strip()

#         if choices.lower() == "q":
#             print_info("Exiting...")
#             sys.exit(0)

#         if choices.startswith("info"):
#             _, letter = choices.split()
#             index = char_to_index(letter)
#             if 0 <= index < len(packages):
#                 package = packages[index]
#                 display_package_info(package, os.path.join(packages_root_dir, package))
#             continue

#         if choices.startswith("check"):
#             _, letter = choices.split()
#             index = char_to_index(letter)
#             if 0 <= index < len(packages):
#                 package = packages[index]
#                 print(f"Running conflict check for {package}...")
#                 run_conflict_checker(package)  # Pass only the package name
#             input("\nPress Enter to return to the package selection...")
#             continue

#         selected_packages = []
#         if choices == "*":
#             selected_packages = packages
#         else:
#             for choice in choices:
#                 index = char_to_index(choice)
#                 if 0 <= index < len(packages):
#                     selected_packages.append(packages[index])

#         if selected_packages:
#             break  # Exit loop and proceed to copying

#     for package in selected_packages:
#         source_path = os.path.join(packages_root_dir, package)
#         target_path = os.path.join(symlink_target_dir, package)

#         copy_package(source_path, target_path)

# if __name__ == "__main__":
#     main()