"""This file initialises all bots
"""

from .bots import initialise

from .bot import activate_bot, on_user_register, on_channel_join, on_command,\
    on_message_send, Bot, BotContainer, CommandLinker
