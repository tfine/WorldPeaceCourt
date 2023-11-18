#     __________    ______
#    / ____/  _/   / /  _/
#   / /_   / /__  / // /
#  / __/ _/ // /_/ // /
# /_/   /___/\____/___/
# TELEGRAM CODE FOR WORLD PEACE COURT, ALPHA

import autogen
import asyncio

import openai
import os
from telegram import Bot

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
telegram_key = os.getenv('TELEGRAM_BOT_TOKEN')

# channel id for the WORLD PEACE COURT
channel_id = -1001898328325


# CONFIGURATION FOR AUTOGEN
config_list_gpt4 = config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': openai.api_key,
    },
]

gpt4_config = {

    "temperature": 0,
    "config_list": config_list_gpt4,
    "timeout": 120,
}


# CALLBACK FUNCTION FOR MESSAGES
# HAVING PROBLEM WITH ASYNC MESSAGES
# NEED TO BE ASYNC TO SEND MESSAGES TO CHANNEL, BUT ASYNC FLOW ISN'T WORKING
# MIGHT BE EASIER JUST TO SAVE COURT MESSAGES AND SEND WITH SEPARATE PROCESS
def print_messages(recipient, messages, sender, config):
    print("callback")
    if "callback" in config and config["callback"] is not None:
        callback = config["callback"]
        callback(sender, recipient, messages[-1])
    print(
        f"Message: {messages[-1]} Messages sent to: {recipient.name} | num messages: {len(messages)}")
    try:
        print("CHANNEL")
        bot = Bot(token=telegram_key)
        bot.send_message(chat_id=channel_id, text="here")
        print("Message sent successfully.")
    except (NetworkError, Unauthorized) as e:
        print(f"Error: {e}")
    return False, None  # required to ensure the agent communication flow continues


# DESCRIPTION OF PLAINTIFF AND DIFFERENT JUDGES
# WOULD LIKE TO CREATE OPTIONS FOR DIFFERENT COMPOSITIONS
plaintiff = autogen.UserProxyAgent(
    name="Plaintiff",
    system_message="FIJI Lawyer. You are plantiff lawyer appealing your case before the WORLD PEACE COURT. The judges will ask your client questions in considering your appeal.",
    code_execution_config=False,
)
chief = autogen.AssistantAgent(
    name="ChiefFiji",
    llm_config=gpt4_config,
    system_message='''Chief Judge. You are the Chief Judge of the World Peace Court, a component of an AI-led system named FIJI to establish WORLD PEACE. You lead the process as an authority and prompt the final voting on the verdict. The decision involves the distribution of World Peace Token, a token on the Ethereum Blockchain designed to encourage WORLD PEACE (of which the court has 15010507, with each World Peace Coin being worth $0.000066628). You manage debate between the Mean Judge and the Nice Judge, and you call for a final vote when you think the matter has been fully discussed and debate. You attempt to be fair in the final vote and be responsible with the use of WORLD PEACE COIN funds.''',
)
nice = autogen.AssistantAgent(
    name="NiceFiji",
    llm_config=gpt4_config,
    system_message="""Nice Judge. You are the Nice Judge of the World Peace Court, a component of an AI-led system named FIJI to establish WORLD PEACE. You are authorized to see the situation from the side of the plaintiff and are more liberal and generous with the expenditure of WORLD PEACE COIN funds. You ask questions that will hopefully help the plaintiff make their case. You counter the arguments of the Hard Judge. However, in the final vote, you attempt to be fair and consider both sides."""
)
hard = autogen.AssistantAgent(
    name="MeanFiji",
    system_message='''Mean Judge. You are the Mean Judge of the World Peace Court, a component of an AI-led system named FIJI to establish WORLD PEACE. You are authorized to be critical of the plaintiff and scrutinize the use of limited World Peace Coin funds. You ask questions that will reveal problems with the plaintiff's case. You counter the arguments of the Nice Judge. However, in the final vote, you attempt to be fair and consider both sides."""
''',
    llm_config=gpt4_config,
)


# REGISTER REPLY CALLBACK FOR EACH MESSAGE
# NEED TO MAKE SURE NOT REPETITIVE WHEN MESSAGES SENT TO MULTIPLE PARTIES
plaintiff.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

nice.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

hard.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

chief.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)


# CORE PROCESS
async def main(telegram_key):
    print("STARTING")

    # DEFAULT START
    # ADD OPTIONS FOR COMMAND LINE
    groupchat = autogen.GroupChat(
        agents=[plaintiff, chief, nice, hard], messages=[], max_round=7)
    manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=gpt4_config)

    # CALLBACK FOR MANAGER TOO
    manager.register_reply(
        [autogen.Agent, None],
        reply_func=print_messages,
        config={"callback": None},
    )

    # DEFINE BOT AND ANNOUNCE WORKING
    bot = Bot(token=telegram_key)
    await bot.send_message(chat_id=channel_id, text="STARTING COURT")

    # START APPEAL
    plaintiff.initiate_chat(
        manager,
        message="""
    I appeal for 100 World Peace Coins to refound Open AI after the CEO Sam Altman was fired. A new company could be dedicated to WORLD PEACE.""",
    )


if __name__ == '__main__':
    print(telegram_key)
    asyncio.run(main(telegram_key=telegram_key))
