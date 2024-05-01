from flask import Flask, render_template, request, redirect, url_for
import graphql_helper
import json

app = Flask (__name__)


@app.route("/")
# Index page acting as the home page for the app
def index():
    #Get all data from the database via Devii
    list_data = graphql_helper.get_list_data()
    status_data = graphql_helper.get_status_name()

    #Sorts list by id then item
    list_data.sort(key=lambda x: x["listid"])
    for item in list_data:
        item["item_collection"].sort(key=lambda x: x["itemid"])

    #Return index.html template with list data
    return render_template("index.html", list_data=list_data, status_data=status_data)

@app.route("/add_item", methods=["POST"])
#this will be the Add Item route
def add_item():
    #items will be added via form in index.html
    item_name = request.form["itemname"]
    list_id = request.form["listid"]
    status_id = request.form["statusid"]

    # Response will add item to db and add list_id and status_id as FK for new item
    response = graphql_helper.add_item(item_name, list_id, status_id)

    # Each GraphQL query or mutation sends a nested json response back, we access the key "data" first, if key is found the response will redirect to the index page and refresh the list_data
    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error adding item"

@app.route("/add_list", methods=["POST"])
def add_list():
    list_name = request.form["listname"]
    status_id = request.form["statusid"]

    response = graphql_helper.add_list(list_name, status_id)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error adding catagory"
    
@app.route("/delete_item", methods=["POST"])
def delete_item():
    itemid = request.form["itemid"]

    response = graphql_helper.delete_item(itemid)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error deleteding item"
    
@app.route("/edit_item", methods=["POST"])
def edit_item():  # rename edit_item
    item_id = request.form["itemid"]
    item_name = request.form["itemname"]
    list_id = request.form["listid"]
    status_id = request.form["statusid"]

    response = graphql_helper.edit_item(item_id, item_name, list_id, status_id)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error editing item."


@app.route("/edit_list", methods=["POST"])
def edit_list():
    listid = request.form["listid"]
    new_list_name = request.form["listname"]
    statusid = request.form["statusid"]

    response = graphql_helper.edit_list(listid, new_list_name, statusid)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error editing catagory."


@app.route("/delete_list", methods=["POST"])
def delete_list():
    list_id = request.form["listid"]

    response = graphql_helper.delete_list(list_id)

    if response.get("data"):
        return redirect(url_for("index"))
    else:
        return "Error editing catagory."

@app.route("/get_status", methods=["GET", "POST"])
def get_status():
    status_data = graphql_helper.get_status_name()

    return status_data


if __name__ == "__main__":
    app.run(debug=True)