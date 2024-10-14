"""This file contains a bot used to activate non-default bots for the server

Author: Miguel Guthridge
"""

from . import bot

from .. import state
from .. import message

class ActivatorBot(bot.Bot):
    """Bot that activates other bots when requested by an admin
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = "Activator"

    def register_commands(self):
        state.s.commands.register("activate", self, self.activate_bot)
    
    def activate_bot(self, args: list, c_id: int, u_id: int, m_id: int):
        """Respond to commands to activate bots
        """
        usr = state.s.users.get(u_id)
        if not usr.is_admin():
            message.Message(self._user.get_id(), c_id, 
                            "Error: user must be an admin to activate a bot")
            return

        try:
            bot.activate_bot(args[0])
            message.Message(self._user.get_id(), c_id, 
                            f"Successfully activated {args[0]} Bot")
        except KeyError:
            message.Message(self._user.get_id(), c_id, 
                            f"Error: bot with name '{args[0]}' not found")
