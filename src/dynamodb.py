import boto3
import random

client = boto3.client("dynamodb")
DB = boto3.resource("dynamodb")
table_name = "WordDictionary"
table = DB.Table(table_name)
primary_column_name = "word_to_be_replaced"
columns = ["suggestions"]


def get_words_to_be_replaced():
    """
    :return: Returns a dictionary item with all the primary keys in the dynamodb table
    """
    response = client.scan(
        TableName=table_name,
        ProjectionExpression=primary_column_name
    )
    return response["Items"]


def replace_word(word_to_be_replaced):
    '''
    Queries the database with the string parameter as key and if it exists, return a random from the suggestions column
    :param word_to_be_replaced: Self explanatory
    :return: The status code of the API call and some meta information to print the corresponding message
    '''
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


def get_item(primary_key):
    '''
    Get a table item if the string primary_key exists in the dynamodb table
    :param primary_key: The key to be queried in the database
    :return: A dictionary item corresponding to the primary key
    '''
    response = table.get_item(
        Key={
            primary_column_name: primary_key
        }
    )
    return response


def add_item(word_to_be_replaced, suggestion):
    """
    Add an item to the dynamodb table e.g {big} -> {colossal, ginormous}
    !add big huge  -------> {big} -> {colossal, ginormous, huge}
    :return: -1 If the suggestion already exists
             Else the status code of the API call
    """
    db_item = get_item(word_to_be_replaced)
    status_code = db_item["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        if "Item" in db_item:
            suggestion_list = db_item["Item"][columns[0]]
            if suggestion not in suggestion_list:
                suggestion_list.append(suggestion)
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
    """
    Remove an item from the dynamodb table e.g {average} -> {mediocre}
    !remove average mediocre -------> {average} -> {}
    :word_to_be_replaced:
    :return: -2 If the word_to_be_replaced doesnt exist in the database
             -1 If the suggestion doesnt exist in the database
             Else return the status code of the api call
    """
    db_item = get_item(word_to_be_replaced)
    status_code = db_item["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        if "Item" in db_item:
            # Gets the list of all the suggestion words
            suggestion_list = db_item["Item"][columns[0]]
            if suggestion in suggestion_list:
                suggestion_list.remove(suggestion)
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
            # The specified word doesnt exist in the database
            return -2
    else:
        return status_code
