"""A simple bot to demonstrate some of the methods that can be used by bots

Author: Miguel Guthridge
"""

from . import bot

from .. import dm
from .. import message
from .. import state

class WelcomeBot(bot.Bot):
    """Bot that sends a DM to users that have just registered
    """
    BOT_COMMAND = "welcome"
    CUSTOMISE_CMD = "customise"
    def __init__(self) -> None:
        super().__init__()
        self._name = "Welcome"
        self._message = "Welcome to Dreams, {name}"
    
    def on_user_register(self, u_id: int) -> bool:
        """Create a DM with the user and send a message welcoming them
        """
        # Get new user
        user_name = state.s.users.get(u_id).get_name()
        
        # Create DM
        d = dm.Dm(self._user.get_id(), [u_id])
        
        # Send message welcoming user, replace the '{name}' substring with the
        # user's name
        message.Message(self._user.get_id(), d.get_id(),
                        self._message.replace("{name}", 
                                              f"{user_name[0]} {user_name[1]}"))
        
        return True

    def print_usage(self, ch_id):
        """Print usage for setting welcome message

        Args:
            ch_id (int): channel to send usage to
        """
        message.Message(self._user.get_id(), ch_id, "To customise the welcome "
                        f"message, use the command `/{self.BOT_COMMAND} "
                        f"{self.CUSTOMISE_CMD} [new message]`\n"
                        "Include '{name}' inside the new message to use the new "
                        "user's name."
                        )

    def customise_msg(self, new_message: str, c_id: int):
        """Customise the welcome message

        Args:
            new_message (str): new message to use
            c_id (int): channel where command was caled
        """
        self._message = new_message
        message.Message(self._user.get_id(), c_id, "Successfully updated welcome"
                        f"message to '{new_message}'.")
    
    def welcome(self, args: list, c_id: int, u_id: int, m_id: int):
        """Run commands on welcome bot, or if a command wasn't recognised, 
        prints usage

        Args:
            args (list): arguments
            c_id (int): channel ID
            u_id (int): user id
            m_id (int): message id
        """
        if not state.s.users.get(u_id).is_admin():
            message.Message(self._user.get_id(), c_id, "You must be an admin to "
                            "customise the welcome message.")
            return
        if len(args) >= 2 and args[0] == self.CUSTOMISE_CMD:
            self.customise_msg(" ".join(args[1:]), c_id)
        else:
            self.print_usage(c_id)
        
    def register_commands(self):
        state.s.commands.register(self.BOT_COMMAND, self, self.welcome)
