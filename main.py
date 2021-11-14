import os
import discord
import dynamodb as dyn

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# Read messages asynchronously from the discord server
@client.event
async def on_message(message):

    # Do not read messages made from the bot itself to avoid a loop
    if message.author == client.user:
        return
    # Split the message content in tokens separated by a space
    message_word_list = message.content.split(" ")
    sentence_length = len(message_word_list)

    if "very" in message.content:
        for i in range(sentence_length):
            if message_word_list[i] == "very":
                word_to_be_replaced = message_word_list[i+1]
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
                await message.channel.send("Very " + word_to_be_replaced + " -> " + replacement_word +
                " has been successfully added to the dictionary, thank you for your contribution.")
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
                await message.channel.send("Very " + word_to_be_replaced + " -> " + replacement_word +
                                    " has been successfully removed from the dictionary, thank you for your contribution.")
            elif api_result == -1:
                await message.channel.send("The specified suggestion does not exist")
            elif api_result == -2:
                await message.channel.send("The word " + word_to_be_replaced + " does not have a valid entry in the database")
            else:
                await message.channel.send("API call failed with status code" + api_result)

client.run(TOKEN)
