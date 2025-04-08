from pathlib import Path
import os
import sys
import json
from talon import actions
from talon.experimental.parrot import ParrotFrame
from talon_init import TALON_USER

def get_talon_user_path():
    """Get the talon user path based on the platform."""
    if sys.platform == "win32":
        return os.path.join(os.getenv("APPDATA"), "talon", "user")
    else:
        return os.path.join(os.getenv("HOME"), ".talon", "user")

def get_parrot_integration_path():
    """Get the path to the parrot_integration.py file."""
    talon_user_path = get_talon_user_path()
    matches = list(Path(talon_user_path).rglob("parrot_integration.py"))

    for path in matches:
        print("Found parrot_integration.py:", path)

    return matches[0] if matches else None

def get_patterns_py_path():
    """Get the path to the patterns.py file."""
    talon_user_path = get_talon_user_path()
    matches = list(Path(talon_user_path).rglob("patterns.json"))

    for path in matches:
        print("Found patterns.json:", path)

    return matches[0] if matches else None

def load_patterns(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Failed to load patterns from {path}: {e}")
        return {}

def build_relative_import_path(current_file: Path, target_file: Path) -> str:
    # Root of all Talon scripts
    user_root = Path.home() / ".talon" / "user"
    if not all(part.isidentifier() for part in target_file.parts):
        raise ValueError(f"Invalid import path — folder/file names must be valid Python identifiers: {target_file}")

    # Determine how many levels up we need to go from current file
    up_levels = len(current_file.parts) - 1
    dot_prefix = "." * up_levels if up_levels > 0 else "."

    # Module path: foo/bar/baz.py → foo.bar.baz
    target_module = ".".join(target_file.parts)

    return f"{dot_prefix}.{target_module}"

def wrap_pattern_match(pattern_match: callable):
    def wrapper(frame: ParrotFrame):
        # print("items", frame.classes.items())
        # winner_label, winner_prob = next(iter(frame.classes.items()))
        # print('parrot', f"predict {winner_label} {winner_prob * 100:.2f}% pow={frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")
        active =  pattern_match(frame)
        if active:
            print("----------------------")
            # print(f"{len(active)} active patterns")
            # print("active", active)
            top_classes = sorted(frame.classes.items(), key=lambda item: item[1], reverse=True)
            print('parrot', f"top classes: {[(k, round(v*100, 2)) for k, v in top_classes[:3]]} pow={frame.power:.2f}")

            top = sorted(frame.classes.items(), key=lambda item: item[1], reverse=True)
            if len(top) > 1:
                first, second = top[0], top[1]
                if second[1] > 0.6 * first[1]:  # tweak threshold as needed
                    print(f"[SPY] Close call: {first[0]} ({first[1]:.2f}) vs {second[0]} ({second[1]:.2f})")
            # for a in active:
            #     winner_label, winner_prob = next(iter(frame.classes.items()))
            #     print('parrot', f"predict {winner_label} {winner_prob * 100:.2f}% pow={frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")
        return active
    return wrapper

original_pattern_match = None

def parrot_tester_wrap_parrot_integration(parrot_delegate, file: str):
    global original_pattern_match
    if original_pattern_match is None:
        with open(file, "r", encoding="utf-8") as f:
            print("Wrapping pattern_integration.py")
            original_pattern_match = parrot_delegate.pattern_match
            parrot_delegate.pattern_match = wrap_pattern_match(parrot_delegate.pattern_match)
            parrot_delegate.set_patterns(json.load(f))

def parrot_tester_restore_parrot_integration(parrot_delegate, original_file: str):
    """Restore pattern patterns."""
    global original_pattern_match
    if original_pattern_match is not None:
        parrot_delegate.pattern_match = original_pattern_match
        original_pattern_match = None

    with open(original_file, "r", encoding="utf-8") as f:
        parrot_delegate.set_patterns(json.load(f))
        print("Restored pattern_integration.py")

def generate_parrot_integration_hook(import_path: str, current_file: Path):
    target_dir = current_file.parent.parent / "auto_generated"
    test_file = target_dir / "parrot_integration_hook.py"

    code = f"""\
# AUTO-GENERATED
try:
    from talon import Module
    from {import_path} import parrot_delegate
    from ..src.utils import (
        parrot_tester_wrap_parrot_integration,
        parrot_tester_restore_parrot_integration
    )

    mod = Module()

    @mod.action_class
    class Actions:
        def parrot_tester_wrap_parrot_integration(file: str):
            \"\"\"Wrap parrot_integration file\"\"\"
            parrot_tester_wrap_parrot_integration(parrot_delegate, file)

        def parrot_tester_restore_parrot_integration(original_file: str):
            \"\"\"Restore parrot_integration file\"\"\"
            parrot_tester_restore_parrot_integration(parrot_delegate, original_file)
except ImportError:
    pass
"""

    test_file.write_text(code)
    print(f"✅ Wrote test file to {test_file}")

def copy_patterns_to_generated(original_path: Path, generated_path: Path):
    generated_path = generated_path / "patterns_draft.json"
    try:
        with original_path.open("r", encoding="utf-8") as f:
            patterns = json.load(f)

        for pattern in patterns.values():
            for section in ("threshold", "grace_threshold"):
                if section in pattern:
                    if ">power" in pattern[section]:
                        pattern[section][">power"] = 1

        with generated_path.open("w", encoding="utf-8") as f:
            json.dump(patterns, f, indent=2)

        print(f"✅ Copied patterns.json to: {generated_path}")
        return patterns
    except Exception as e:
        print(f"❌ Failed to copy patterns.json: {e}")
        return {}

def create_auto_generated_folder(generated_folder: Path):
    """Create the auto_generated folder if it doesn't exist."""
    try:
        generated_folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created auto_generated folder: {generated_folder}")
    except Exception as e:
        print(f"❌ Failed to create auto_generated folder: {e}")

def generate_talon_noises_file(patterns: dict, generated_folder: Path):
    """Generate the talon_noises.py file based on the patterns."""
    target_file = generated_folder / "parrot_tester_active.talon"
    code = f"""# AUTO-GENERATED
tag: user.parrot_tester
not mode: sleep
-
<phrase>: skip()
parrot(pop):
    user.parrot_tester_discrete("pop", power, f0, f1, f2)
    mouse_click()
"""
    for name, config in patterns.items():
        if name == "pop":
            continue

        is_continuous = config.get("graceperiod", False)

        if is_continuous:
            code += f"parrot({name}): user.parrot_tester_continuous_start(\"{name}\", power, f0, f1, f2)\n"
            code += f"parrot({name}:stop): user.parrot_tester_continuous_stop(\"{name}\")\n"
        else:
            code += f"parrot({name}): user.parrot_tester_discrete(\"{name}\", power, f0, f1, f2)\n"

    target_file.write_text(code)
    print(f"✅ Wrote talon_noises.py to {target_file}")

def parrot_tester_initialize():
    """Test function to check if the paths are correct."""
    parrot_integration_path = get_parrot_integration_path().resolve()
    patterns_py_path = get_patterns_py_path().resolve()
    current_path = Path(__file__).resolve()
    generated_folder = Path(current_path.parent.parent / "auto_generated").resolve()

    current = Path(__file__).resolve()
    target = Path(parrot_integration_path).resolve()
    user_root = Path(TALON_USER).resolve()

    current_rel = current.relative_to(user_root)
    target_rel = target.relative_to(user_root).with_suffix("")  # drop .py

    patterns_json = load_patterns(patterns_py_path)

    # Example:
    # for name, config in patterns.items():
    #     print(f"{name}: {config}")

    print("TALON_USER:", TALON_USER)
    print("current_path:", current_path)
    print("parrot_integration_path:", parrot_integration_path)
    import_path = build_relative_import_path(current_rel, target_rel)
    print(import_path)
    create_auto_generated_folder(generated_folder)
    copy_patterns_to_generated(patterns_py_path, generated_folder)
    generate_talon_noises_file(patterns_json, generated_folder)
    generate_parrot_integration_hook(import_path, current_path)
    patterns_draft = Path(generated_folder / "patterns_draft.json").resolve()
    print(f"patterns_draft: {patterns_draft}")
    actions.user.parrot_tester_wrap_parrot_integration(patterns_draft)

    print(f"Parrot Integration Path: {parrot_integration_path}")
    print(f"Patterns.py Path: {patterns_py_path}")

def restore_patterns():
    """Restore the original patterns.json file."""
    original_path = get_patterns_py_path()
    actions.user.parrot_tester_restore_parrot_integration(original_path)