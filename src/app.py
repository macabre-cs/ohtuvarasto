import os
from flask import Flask, render_template, request, redirect, url_for, session
from varasto import Varasto

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# In-memory storage for warehouses
warehouse_store = {"warehouses": {}, "counter": 0}


def get_next_id():
    warehouse_store["counter"] += 1
    return warehouse_store["counter"]


def parse_float(value, default=0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def handle_create_post():
    name = request.form.get("name", "").strip()
    capacity = parse_float(request.form.get("capacity", 0))
    initial_balance = parse_float(request.form.get("initial_balance", 0))

    if name and capacity > 0:
        warehouse_id = get_next_id()
        warehouse_store["warehouses"][warehouse_id] = {
            "name": name,
            "varasto": Varasto(capacity, initial_balance)
        }
        return True
    return False

@app.route("/")
def index():
    theme = session.get("theme", "kawaii")
    return render_template(
        "index.html",
        warehouses=warehouse_store["warehouses"],
        theme=theme
    )


@app.route("/toggle-theme")
def toggle_theme():
    current = session.get("theme", "kawaii")
    session["theme"] = "gothic" if current == "kawaii" else "kawaii"
    return redirect(request.referrer or url_for("index"))


@app.route("/warehouse/new", methods=["GET", "POST"])
def create_warehouse():
    if request.method == "POST":
        handle_create_post()
        return redirect(url_for("index"))
    theme = session.get("theme", "kawaii")
    return render_template("create_warehouse.html", theme=theme)


@app.route("/warehouse/<int:warehouse_id>")
def view_warehouse(warehouse_id):
    warehouse = warehouse_store["warehouses"].get(warehouse_id)
    if warehouse is None:
        return redirect(url_for("index"))
    theme = session.get("theme", "kawaii")
    return render_template(
        "view_warehouse.html",
        warehouse_id=warehouse_id,
        warehouse=warehouse,
        theme=theme
    )


@app.route("/warehouse/<int:warehouse_id>/edit", methods=["GET", "POST"])
def edit_warehouse(warehouse_id):
    warehouse = warehouse_store["warehouses"].get(warehouse_id)
    if warehouse is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            warehouse["name"] = name
        return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))
    theme = session.get("theme", "kawaii")
    return render_template(
        "edit_warehouse.html",
        warehouse_id=warehouse_id,
        warehouse=warehouse,
        theme=theme
    )


@app.route("/warehouse/<int:warehouse_id>/add", methods=["POST"])
def add_content(warehouse_id):
    warehouse = warehouse_store["warehouses"].get(warehouse_id)
    if warehouse is None:
        return redirect(url_for("index"))

    amount = parse_float(request.form.get("amount", 0))
    if amount > 0:
        warehouse["varasto"].lisaa_varastoon(amount)
    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


@app.route("/warehouse/<int:warehouse_id>/remove", methods=["POST"])
def remove_content(warehouse_id):
    warehouse = warehouse_store["warehouses"].get(warehouse_id)
    if warehouse is None:
        return redirect(url_for("index"))

    amount = parse_float(request.form.get("amount", 0))
    if amount > 0:
        warehouse["varasto"].ota_varastosta(amount)
    return redirect(url_for("view_warehouse", warehouse_id=warehouse_id))


@app.route("/warehouse/<int:warehouse_id>/delete", methods=["POST"])
def delete_warehouse(warehouse_id):
    if warehouse_id in warehouse_store["warehouses"]:
        del warehouse_store["warehouses"][warehouse_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
