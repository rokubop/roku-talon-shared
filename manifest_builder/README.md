# Manifest builder

A tool to generate `manifest.json` files for folders defined in `manifest_targets.txt`.

- automatic parses talons actions, modes, tags, lists, and other talon entities the package contributes and depends on.

# Usage

1. ✏️ Edit `manifest_targets.txt` to include the relative paths of directories where you want to create or update manifests.
2. ▶️ Run: `python manifest_builder.py` to generate `manifest.json` in the specified target directories.