import subprocess
import os
import sys

def call_package_manager():
    packages_root_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(packages_root_dir, 'package_tools', 'sparse_checkout.py')

    try:
        subprocess.check_call([sys.executable, script_path, packages_root_dir])
        # print("Packages updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute sparse checkout script: {str(e)}")
    except KeyboardInterrupt:
        pass

def main():
    try:
        call_package_manager()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()


# contributes vs depends
# linter
# ast
# focus on manifest
# SHA in manifest
# dict of deps rather than list
# deps hash?
# git sparse checkout
# git tags
# contributing vs dependency
# dep version?
# clone repo and enable what u want
# vscode extension linter
# git manaager
# making use of existing linter