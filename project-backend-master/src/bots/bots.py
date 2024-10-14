"""Contains functions relating to all bots
"""

from . import welcome_bot, activator_bot, standup_bot

def initialise():
    """Initialises all bots. To add more bots, make them be initialised in this function
    """
    
    # Create an activator bot instance
    activator_bot.ActivatorBot()
    
    # Create a welcome bot instance
    welcome_bot.WelcomeBot()

    # Create a standup bot instance
    standup_bot.StandupBot()
