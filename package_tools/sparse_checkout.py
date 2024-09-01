import os
import sys
import subprocess
from pathlib import Path

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
GRAY = '\033[0;37m'
NC = '\033[0m'

AVAILABLE_DIRECTORIES = [
    'drag_mode',
    'dynamic_noises',
    'game_tools',
    'mouse_move_adv',
    'parrot_config',
    'scripts',
    'ui_elements',
    'vgamepad'
]

def print_error(message):
    print(f"{RED}Error:{NC} {message}")

def print_warning(message):
    print(f"{YELLOW}Warning:{NC} {message}")

def print_info(message):
    print(f"{GREEN}{message}{NC}")

def index_to_char(index):
    return chr(97 + index)

def char_to_index(char):
    return ord(char) - 97

def run_git_command(args, repo_dir):
    try:
        subprocess.run(args, cwd=repo_dir, check=True)
    except subprocess.CalledProcessError as e:
        print_error(f"Command '{' '.join(args)}' failed: {str(e)}")
        sys.exit(1)

def get_git_repo_root():
    try:
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True)
        return Path(result.stdout.strip()).resolve()
    except subprocess.CalledProcessError:
        print_error("This script must be run within a Git repository.")
        sys.exit(1)

def get_sparse_checkout_paths(repo_dir):
    try:
        result = subprocess.run(['git', 'sparse-checkout', 'list'], cwd=repo_dir, capture_output=True, text=True, check=True)
        return [Path(line.strip()).as_posix() for line in result.stdout.splitlines()]
    except subprocess.CalledProcessError:
        return []

def is_sparse_checkout_enabled(repo_dir):
    sparse_checkout_file = repo_dir / '.git' / 'info' / 'sparse-checkout'
    return sparse_checkout_file.exists()

def sparse_checkout_directories(repo_dir, directories):
    run_git_command(['git', 'sparse-checkout', 'init'], repo_dir)

    relative_directories = [Path(d).as_posix() for d in directories]
    print_info("The following directories will be included in the sparse checkout:")
    for directory in relative_directories:
        print(f"  - {directory}/")

    confirm_action(f"Proceed with adding the selected directories?", repo_dir, ['git', 'sparse-checkout', 'set', *relative_directories])

def confirm_action(message, repo_dir, command, details=None):
    print_info(f"\nThe following command will be executed in {repo_dir}:\n{CYAN}{' '.join(command)}{NC}")
    if details:
        print_info(f"Details: {details}")
    confirm = input(f"{YELLOW}{message} (y/n): {NC}").strip().lower()
    if confirm == 'y':
        run_git_command(command, repo_dir)
    else:
        print_info("Operation canceled.")

def prompt_user_for_action():
    print_info(f"{GREEN}*{NC}) Include all")
    print_info(f"{YELLOW}- [letter]{NC}) Remove selected package(s)")
    print_info(f"{YELLOW}!{NC}) Disable sparse checkout (include all directories)")
    print_info(f"{GREEN}q{NC}) Quit")
    return input("Enter your choice(s): ").strip()

def handle_add_selection(selected_packages, sparse_checkout_paths, git_repo_root):
    directories_to_add = [pkg for pkg in selected_packages if pkg not in sparse_checkout_paths]
    combined_directories = sparse_checkout_paths + directories_to_add
    details = f"Adding: {', '.join(directories_to_add)}"
    confirm_action("Do you want to add the selected packages to the sparse checkout?", git_repo_root, ['git', 'sparse-checkout', 'set', *combined_directories], details)
    return get_sparse_checkout_paths(git_repo_root)  # Refresh sparse checkout paths


def handle_remove_selection(selected_packages, sparse_checkout_paths, git_repo_root):
    directories_to_keep = [pkg for pkg in sparse_checkout_paths if pkg not in selected_packages]
    details = f"Removing: {', '.join(selected_packages)}"
    if directories_to_keep:
        confirm_action("Do you want to remove the selected packages from the sparse checkout?", git_repo_root, ['git', 'sparse-checkout', 'set', *directories_to_keep], details)
    else:
        confirm_action("No directories selected, sparse checkout will be disabled. Proceed?", git_repo_root, ['git', 'sparse-checkout', 'disable'], details)
    return get_sparse_checkout_paths(git_repo_root)  # Refresh sparse checkout paths


def handle_user_selection(choices, available_packages, sparse_checkout_paths, git_repo_root):
    remove = choices.startswith("-")
    if remove:
        choices = choices[1:].strip()

    selected_packages = []
    if choices == "*":
        selected_packages = available_packages
    else:
        for choice in choices:
            index = char_to_index(choice)
            if 0 <= index < len(available_packages):
                selected_packages.append(available_packages[index])

    if selected_packages:
        if remove:
            sparse_checkout_paths = handle_remove_selection(selected_packages, sparse_checkout_paths, git_repo_root)
        else:
            sparse_checkout_paths = handle_add_selection(selected_packages, sparse_checkout_paths, git_repo_root)
    else:
        print_info("No valid selection made.")

    return sparse_checkout_paths

def initialize_sparse_checkout(git_repo_root):
    print_warning(
        f"\nEnabling sparse checkout will remove all directories from your working directory "
        f"at {git_repo_root}, except those explicitly added back through this script."
    )
    confirm_action("Would you like to enable sparse checkout?", git_repo_root, ['git', 'sparse-checkout', 'init'])
    print_info(f"Sparse checkout has been enabled at {git_repo_root}. You can now select directories to include.")

def main():
    git_repo_root = get_git_repo_root()

    if not is_sparse_checkout_enabled(git_repo_root):
        initialize_sparse_checkout(git_repo_root)

    available_packages = AVAILABLE_DIRECTORIES
    sparse_checkout_paths = get_sparse_checkout_paths(git_repo_root)

    try:
        while True:
            print(f"Select packages to manage with git sparse-checkout (e.g., {GREEN}adf{NC} for {GREEN}a{NC}, {GREEN}d{NC}, and {GREEN}f{NC}):")
            for i, package in enumerate(available_packages):
                char = index_to_char(i)
                status = f"{GREEN}(installed){NC}" if package in sparse_checkout_paths else f"{GRAY}(not installed){NC}"
                print(f"{char}) {package} {status}")

            choices = prompt_user_for_action()
            if choices.lower() == "q":
                print_info("Exiting...")
                break

            if choices == "!":
                confirm_action("Disable sparse checkout and include all directories?", git_repo_root, ['git', 'sparse-checkout', 'disable'])
                break

            sparse_checkout_paths = handle_user_selection(choices, available_packages, sparse_checkout_paths, git_repo_root)


    except KeyboardInterrupt:
        print_info("\nOperation canceled by user. Exiting...")

if __name__ == "__main__":
    main()
