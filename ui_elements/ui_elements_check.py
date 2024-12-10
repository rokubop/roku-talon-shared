from talon import app, registry

UPDATE_MESSAGE = (
    "MissingDependency: This code requires a newer version of ui_elements.\n"
    "Please install talon-ui-elements package at:\n"
    "https://github.com/rokubop/talon-ui-elements,\n"
    "and remove your current ui_elements."
)

MISSING_MESSAGE = (
    "MissingDependency: Please install the talon-ui-elements package at:\n"
    "https://github.com/rokubop/talon-ui-elements"
)

def check_ui_elements():
    if registry.actions.get("user.ui_elements"):
        if not registry.actions.get("user.ui_elements_version"):
            app.notify(UPDATE_MESSAGE)
            print(UPDATE_MESSAGE)
    else:
        app.notify(MISSING_MESSAGE)
        print(MISSING_MESSAGE)

app.register("ready", check_ui_elements)