import boto3
import random

client = boto3.client("dynamodb")
DB = boto3.resource("dynamodb")
table_name = "WordDictionary"
table = DB.Table(table_name)
primary_column_name = "word_to_be_replaced"
columns = ["suggestions"]


def replace_word(word_to_be_replaced):
    db_item = get_item(word_to_be_replaced)
    status_code = db_item["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        if "Item" in db_item:
            suggestion_list = db_item["Item"][columns[0]]
            rand = random.randint(0, len(suggestion_list) - 1)
            replacement_word = suggestion_list[rand]
            return [200, replacement_word]
        else:
            return [200, "no_such_word_exists"]
    else:
        return [status_code, "API call failed"]


# Get a table item if "word_to_be_replaced" matches a primary key in the dynamodb table
def get_item(primary_key):
    response = table.get_item(
        Key={
            primary_column_name: primary_key
        }
    )
    return response


def add_item(word_to_be_replaced, suggestion):
    # Get an item from the table based on the word_to_be_replaced argument
    db_item = get_item(word_to_be_replaced)
    status_code = db_item["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        # The get_item function returned an object that exists in the table therefore it has an Item object in the response
        if "Item" in db_item:
            # Gets the list of all the suggestion words
            suggestion_list = db_item["Item"][columns[0]]
            # Add the new suggestion to the list if it does not already exist in it
            if suggestion not in suggestion_list:
                suggestion_list.append(suggestion)
                # Insert the item on the dynamodb table
                response = table.put_item(
                    Item={
                        primary_column_name: word_to_be_replaced,
                        columns[0]: suggestion_list
                    }
                )
                return response["ResponseMetadata"]["HTTPStatusCode"]
            else:
                # The suggestion already exists
                return -1
        else:
            # The word is new and has to be added
            response = table.put_item(
                   Item={
                       primary_column_name: word_to_be_replaced,
                       columns[0]: [suggestion]
                   })
        return response["ResponseMetadata"]["HTTPStatusCode"]
    else:
        return status_code


def remove_item(word_to_be_replaced, suggestion):
    # The get_item function returned an object that exists in the table therefore it has an Item key value
    db_item = get_item(word_to_be_replaced)
    status_code = db_item["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        # There is an Item with the word_to_be_replaced primary key in the database
        if "Item" in db_item:
            # Gets the list of all the suggestion words
            suggestion_list = db_item["Item"][columns[0]]
            # Add the new suggestion to the list if it does not already exist in it
            if suggestion in suggestion_list:
                suggestion_list.remove(suggestion)
                # Insert the item on the dynamodb table
                response = table.put_item(
                    Item={
                        primary_column_name: word_to_be_replaced,
                        columns[0]: suggestion_list
                    }
                )
                return response["ResponseMetadata"]["HTTPStatusCode"]
            else:
                return -1
        else:
            # The specified key doesnt exist in the database
            return -2
    else:
        return status_code

