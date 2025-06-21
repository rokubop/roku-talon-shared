# Manifest builder

A tool to generate `manifest.json` files for target folders.

This allows you to generate a `manifest.json` file for your talon package to define all necessary metadata, including automatic parsing of all the actions, modes, tags, lists, and other talon entities the package "contributes" and "depends" on.

# Usage

1. ✏️ Edit `manifest_targets.txt` to include the relative paths of directories where you want to create or update manifests.
2. ▶️ Run: `python manifest_builder.py` to generate `manifest.json` in the specified target directories.