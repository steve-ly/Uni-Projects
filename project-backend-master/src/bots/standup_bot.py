
import datetime

from .. import state, error, message

from . import bot

class Standup:
    def __init__(self, channel_id: int, u_id: int, finish_time: datetime.datetime) -> None:
        """Create a stabndup in a channel

        Args:
            channel_id (int): channel with standup
            u_id (int): user creating standup
            finish_time (datetime): time that the standup finishes
        """
        self._target_channel = channel_id
        self._creator = u_id
        self._finish_time = finish_time
        
        self._standup_msg = message.Message(u_id, channel_id, "", send_time=finish_time)

    def query_timeout(self) -> int:
        """Returns the timestamp at which the standup should end
        """
        return self._finish_time.timestamp()

    def add_message(self, msg):
        """Adds a message to the standup
        
        Args:
            msg (Message): Message to add to the standup
        """
        new_msg = str(self._standup_msg)
        # If if's not empty, add a new-line
        if len(new_msg) > 0:
            new_msg += '\n'
        
        # Add message contents
        new_msg += \
            f"{state.s.users.get(msg.get_sender_id()).get_handle()}: {str(msg)}"
        
        self._standup_msg.edit(new_msg)
    
    def is_active(self):
        """Return whether the standup is still active
        """
        return self._finish_time > datetime.datetime.now()

class StandupBot(bot.Bot):
    """Bot for managing standups
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = "Standup"
        self._standups = dict()
    
    def update_standup(self, c_id: int):
        """Ensure standup is still running and removes it if it isn't

        Args:
            c_id (int): channel id
        """
        try:
            # If a stand-up has finished
            if not self._standups[c_id].is_active():
                self._standups.pop(c_id)
        except KeyError:
            pass

    def register_commands(self):
        state.s.commands.register("standup", self, self.create_standup)
    
    def create_standup(self, args: list, c_id: int, u_id: int, m_id: int) -> bool:
        """Create a standup in channel c_id

        Args:
            args (list): arguments
            c_id (int): channel ID
            u_id (int): user id
            m_id (int): message id
        """
        
        # Remove message from data (since it shouldn't be visible)
        state.s.messages.remove(m_id)
        
        # Update standups in the channel (if applicable)
        self.update_standup(c_id)
        
        # Ensure there isn't a standup already active
        if c_id in self._standups:
            raise error.InputError(description="A standup is already active in this channel")

        # Ensure standup has been given correct number of args
        if len(args) != 1:
            # The behaviour here is undefined
            return False
        
        # Tru to convert standup length to an int. If it fails, return since the input is invalid
        try:
            standup_len = int(args[0])
        except ValueError:
            return False
        
        # Ensure standup has a proper duration
        if standup_len <= 0:
            raise error.InputError(description="Standups cannot have negative duration")
        
        # Create standup
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=standup_len)
        self._standups[c_id] = Standup(c_id, u_id, end_time)
        
        return False
        
    def query_standup(self, c_id: int) -> int:
        """Return time standup finishes as timestamp, or None if no standup is
        active

        Args:
            c_id (int): channel to query

        Returns:
            int: time standup finishes (None if no stand-up active)
        """
        # Update standups in channel (if applicable)
        self.update_standup(c_id)
        
        if c_id not in self._standups:
            return None

        return self._standups[c_id].query_timeout()
    
    def on_message_send(self, msg_id: int) -> bool:
        """When a message is sent, perform standup actions if required
        """
        msg = state.s.messages.get(msg_id)
        
        # Check if a standup is happening in that channel
        if self.query_standup(msg.get_channel_id()) is None:
            # If not, return (continuing processing)
            return True
        
        # Add message to standup
        self._standups[msg.get_channel_id()].add_message(msg)
        
        # Remove original message
        state.s.messages.remove(msg_id)
        
        return False
