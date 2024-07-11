from keep_alive import keep_alive

import os

import discord

import time

openai_api_key = os.environ['OPENAI_API_KEY']
my_secret = os.environ['DISCORD_TOKEN']
import openai

openai_client = openai.OpenAI(api_key=openai_api_key)

replace = [
    "@Jord", "@Gumperto", "@Kappie", "@Spolfplif", "@Randomuser", "@spamtung",
    "@purplechair"
    ":dementedtroll:", ":lowresnooooo:", ":DUNN:", ":tf:", "@everyone",
    ":mewheboatmeal:", ":hmm:", ":voidful:"
]
replaced = [
    "<@508206357543911424>", "<@663379745236582400>", "<@352449578131390467>",
    "<@374862669976698881>", "<@763974099495944214>", "<@432407678699044874>",
    "<@316119123581206528>"
    "<:dementedtroll:938052827341811712>",
    "<:lowresnooooo:926115696222552084>", "<:DUNN:941713583434260560>",
    "<:tf:896011237538820128>", "<:tf:896011237538820128>",
    "<:mewheboatmeal:954350574814507119>", "<:hmm:954209539752861717>",
    "<:voidful:926512407281549382>"
]


class MyClient(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        print(message.content)

        if message.author.id == self.user.id:
            return

        elif message.content.startswith("lore"):
            async with message.channel.typing():

                #openai shits

                assistant = openai_client.beta.assistants.create(
                    instructions=
                    "Use the file provided as your knowledge base to best respond to questions or instructions.",
                    model="gpt-4o",
                    tools=[{
                        "type": "file_search"
                    }],
                    tool_resources={
                        "file_search": {
                            "vector_store_ids": [
                                'vs_2M1DuWunoHCSi8QMOQzch5mD'
                            ]  # Note: Make sure "retrieved_file.id" is replaced appropriately with your actual vector store ID string.
                        }
                    })

                thread = openai_client.beta.threads.create()
                thread_message = openai_client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=message.content,
                )

                #feed the thread to the assistant
                my_assistant = openai_client.beta.assistants.retrieve(
                    assistant.id)

                run = openai_client.beta.threads.runs.create(
                    thread_id=thread.id, assistant_id=my_assistant.id)

                time.sleep(5)

                retrieved_run = openai_client.beta.threads.runs.retrieve(
                    thread_id=thread.id, run_id=run.id)

                time.sleep(5)

                thread_messages = openai_client.beta.threads.messages.list(
                    thread.id)
                bot_response = thread_messages.data[0].content[0].text.value

                for index, string in enumerate(replace):
                    if string in bot_response:
                        bot_response = bot_response.replace(
                            string, replaced[index])

                await message.channel.send(bot_response)


def main():

    client = MyClient()

    keep_alive()
    client.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
    main()
