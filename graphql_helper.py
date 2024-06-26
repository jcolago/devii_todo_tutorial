"""Helper functions for GraphQL queries and mutations"""
import requests
import auth

QUERY_URL = "https://api.devii.io/query"

def execute_graphql_query(query, variables=None):
    """helper function for all queries and mutations"""
    # This will load the query or mutation and variable, if any, into the GraphQL quey or mutation
    payload = {"query": query, "variables": variables}

    # the query will always recieve a return response of data in the same shape as the query
    response = requests.post(QUERY_URL, headers=auth.headers, json=payload)

    # the response is returned in json form
    return response.json()

def get_list_data():
    #query taht will be sent to Devii to retrieve all data from the list and item tables
    list_name_query="""
    {
        list {
            listid
            listname
            statusid
            item_collection{
                itemid
                itemname
                statusid
            }
        }
    }
    """
    # creates the payload
    list_name_payload = {"query": list_name_query, "variable": {}}

    #send the query payload and authorization token to devii
    list_name_response = requests.post(
        QUERY_URL, headers=auth.headers, json=list_name_payload
    )

    #retuns the response from GraphQL in a json nested dictionary, retrieves the values from the keys data and list
    return list_name_response.json()["data"]["list"]

def get_status_name():
    query_status_name="""
    {
        status_value{
            statusis
            statusname
        }
    }
    """
    #creates a payload for Devii
    status_name_payload = {"query": query_status_name, "variables":{}}

    # Sends payload and auth token to devii
    status_name_response = requests.post(
        QUERY_URL, headers=auth.headers, json=status_name_payload
    )

    # Returns response from GraphQL, values in keys data and status_value
    return status_name_response.json()["data"]["status_value"]
# queries for mutations
def add_item(item_name, list_id, status_id):
    #add an item to the item table with a listid FK
    add_item_mutation = """
        mutation ($i: itemInput){
            create_item(input: $i){
                itemid
                itemname
                status_value{
                    statusname
                }
                list{
                    listname
                }
            }
        }
    """

    # Variable that will be retrieved from a form the user will submit
    variables = {"i": {"itemname": item_name, "listid": int(list_id), "statusid": int(status_id)}}

    # GraphQL mutation 
    return execute_graphql_query(add_item_mutation, variables)

# Functions from here on have the same format as add_item

def add_list(listname, status_id):
    add_list_mutation = """
        mutation($i: listInput){
            create_list(input:$i){
                listid
                listname
                status_value{
                    statusid
                    statusname
                }
            }
        }
    """
    variables = {"i": {"listname": listname, "statusid":int(status_id)}}
    return execute_graphql_query(add_list_mutation, variables)

# Editing items requires identifying the Primay Key of the item you want to edit, PK is the itemid that will be variable $j, $i will be the changes to the item
def edit_item(itemid, new_name, list_id, status_id):
    edit_item_mutation = """
        mutation ($i: itemInput, $j: ID!) {
            update_item(input: $i, itemid: $j) {
                itemid
                itemname
                status_value{
                    statusid
                    statusname
                }
                list {
                    listid
                    listname
                }
            }
        }
        """
    variables = {
        "j": itemid, # Primary Key for items
        "i": {"itemname": new_name, "listid": int(list_id), "statusid": int(status_id)}
    }
    return execute_graphql_query(edit_item_mutation, variables)

# Edit functions will have same format as edit_item
def edit_list(listid, new_list_name, status_id):
    edit_list_mutation = """
    mutation($i: listInput, $j: ID!){
        update_list(input: $i, listid: $j){
            listid
            listname
            status_value {
                statusname
                statusid
            }
        }
    }
    """

    variables = {"j": int(listid), "i": {"listname": new_list_name, "statusid": int(status_id)}}
    return execute_graphql_query(edit_list_mutation, variables)

# Deleted objects reqires the primary key of object to be deleted
def delete_item(itemid):
    delete_item_mutation = """
    mutation($i :ID!){
        delete_item(itemid: $i){
            itemid
            itemname
        }
    }
    """

    variables = {"i": int(itemid)}
    return execute_graphql_query(delete_item_mutation, variables)

# Delete list has same format as delete_item

def delete_list(listid):
    delete_list_mutation = """
    mutation($i: ID!){
        delete_list(listid: $i){
            listid
            listname
        }
    }
    """

    variables = {"i": int(listid)}
    return execute_graphql_query(delete_list_mutation, variables)