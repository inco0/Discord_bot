import discord
import dynamodb as dyn
import parameters

TOKEN = parameters.get_discord_token("eu-central-1")
client = discord.Client()

# Get the API item of the column wih all the replaceable words in the dictionary
api_result_list = dyn.get_words_to_be_replaced()
# Create a list from the api result with the words that can be replaced
words_to_be_replaced_list = [x["word_to_be_replaced"]["S"] for x in api_result_list]
# Convert the list to set for better performance
words_to_be_replaced_set = set(words_to_be_replaced_list)

# Read messages asynchronously from the discord server
@client.event
async def on_message(message):

    # Do not read messages made from the bot itself to avoid a loop
    if message.author == client.user:
        return

    message_word_list = message.content.split(" ")
    sentence_length = len(message_word_list)

    for word_to_be_replaced in words_to_be_replaced_set:
        if word_to_be_replaced in message.content:
            api_result = dyn.replace_word(word_to_be_replaced)
            if api_result[0] == 200:
                if api_result == "no_such_word_exists":
                    await message.channel.send("The word " + word_to_be_replaced + " doesn't exist in the dictionary,you can add a suggestion with !add x y")
                else:
                    await message.channel.send("You can use " + api_result[1] + " instead of " + word_to_be_replaced)
            else:
                await message.channel.send("API call failed with status code" + api_result)

    if "!add" == message_word_list[0]:
        if sentence_length > 3 | sentence_length < 2:
            await message.channel.send("Wrong command structure, try !add x y")
        elif sentence_length == 3:
            word_to_be_replaced = message_word_list[1]
            replacement_word = message_word_list[2]
            # Call the dynamodb add item function
            api_result = dyn.add_item(word_to_be_replaced, replacement_word)
            if api_result == 200:

                await message.channel.send(word_to_be_replaced + " -> " + replacement_word + " has been successfully added to the dictionary, thank you for your contribution.")
            elif api_result == -1:
                await message.channel.send("The suggestion already exists")
            else:
                await message.channel.send("API call failed with status code" + api_result)

    if "!remove" == message_word_list[0]:
        if sentence_length > 3 | sentence_length < 3:
            await message.channel.send("Wrong command structure, try !remove x y")
        elif sentence_length == 3:
            word_to_be_replaced = message_word_list[1]
            replacement_word = message_word_list[2]
            # Call the dynamodb remove function
            api_result = dyn.remove_item(word_to_be_replaced, replacement_word)
            if api_result == 200:
                await message.channel.send(word_to_be_replaced + " -> " + replacement_word +
                                    " has been successfully removed from the dictionary, thank you for your contribution.")
            elif api_result == -1:
                await message.channel.send("The specified suggestion does not exist")
            elif api_result == -2:
                await message.channel.send("The word " + word_to_be_replaced +
                                           " does not have a valid entry in the database")
            else:
                await message.channel.send("API call failed with status code" + api_result)

client.run(TOKEN)
