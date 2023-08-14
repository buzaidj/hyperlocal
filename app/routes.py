from flask import Flask
from scraper import SOURCE, getPage

app = Flask(__name__)


@app.route("/update")
@app.route("/update/<choice>")
def index(choice=None):
    # TODO: Don't let everyone invoke the update route! Block it with a
    # specific header key that only admins have

    valid_choices = [source.value for source in SOURCE]

    if choice and choice in valid_choices:
        # TODO: pass the page data to llm_layer.py
        getPage(SOURCE[choice])

    elif choice and choice not in valid_choices:
        raise Exception(
            f"Choice {choice} not valid. Valid choices include {valid_choices}"
        )
    else:
        for c in valid_choices:
            # TODO: pass the page data to llm_layer.py
            getPage(SOURCE[c])

    return "Done"


if __name__ == "__main__":
    app.run(debug=True)
