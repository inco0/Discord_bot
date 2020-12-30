import os
import discord
import json
import random

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

try:
    with open('dict.json', 'r') as read:
        word_dictionary = json.load(read)
except FileNotFoundError:
    print("No file found")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_word_list = message.content.split(" ")

    if "very" in message.content:
        #while x
        for i in range(len(message_word_list)):
            if message_word_list[i] == "very":
                word_to_be_replaced = message_word_list[i+1]
        if word_to_be_replaced in word_dictionary:
            value_list = word_dictionary.get(word_to_be_replaced)
            rand = random.randint(0, len(value_list)-1)
            replacement_word = value_list[rand]
            await message.channel.send("You could use " + replacement_word + " instead of very " + word_to_be_replaced)

    if "!add" == message_word_list[0]:
        first_word = message_word_list[1]
        second_word = message_word_list[2]
        if len(message_word_list) > 3:
            await message.channel.send("Wrong command structure, try !remove x y")
        else:
            if first_word in word_dictionary:
                word_dictionary.get(first_word).append(second_word)
            else:
                word_dictionary[first_word] = [second_word]
            try:
                with open('dict.json', 'w') as write:
                    json.dump(word_dictionary, write)
            except FileNotFoundError:
                print("No file found")
            await message.channel.send("Very " + first_word + " -> " + second_word +
            " has been successfully added to the dictionary, thank you for your contribution.")

    if "!remove" == message_word_list[0]:
        first_word = message_word_list[1]
        second_word = message_word_list[2]
        if len(message_word_list) > 3:
            await message.channel.send("Wrong command structure, try !remove x y")
        else:
            if first_word in word_dictionary:  # The word exists in the dictionary
                value_list = word_dictionary.get(first_word)
                value_list.remove(second_word)  # Remove it from the dictionary
                try:
                    with open('dict.json', 'w') as write:
                        json.dump(word_dictionary, write)  # Rewrite the dictionary
                except FileNotFoundError:
                    print("No file found")
                await message.channel.send("Very " + first_word + " -> " + second_word +
                                           " has been successfully removed from the dictionary, thank you for your contribution.")
            else:
                await message.channel.send("The specified combination doesn't exist in the dictionary")


client.run(TOKEN)
