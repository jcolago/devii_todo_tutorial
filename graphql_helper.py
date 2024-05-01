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
  