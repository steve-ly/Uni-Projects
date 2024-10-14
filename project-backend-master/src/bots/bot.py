"""Contains data structures and functions to do with the functioning of bots

Author: Miguel Guthridge [z5312085@ad.unsw.edu.au]
"""


from .. import generic_data
from ..user import User

class Bot(generic_data.GenericData):
    """Class for generic bot type. This is extended by other bot types in the src.bots module
    """
    _commands = dict()
    def __init__(self) -> None:
        """Create a bot. This method should be overridden by subclasses
        """
        super().__init__()
        self._name = "Unnamed"
        self._user = None
        self._is_active = False
        state.s.bots.add(self)

    def register_commands(self): # pragma: no cover
        """Register commands associated with the bot
        Inheriting classes should implement this if they use commands
        """
        pass

    def activate(self):
        """Registers the bot, allowing it to be activated
        """
        self._user = User("[None]", "", self._name, "Bot", is_bot=True)
        self._is_active = True
        self.register_commands()
    
    def is_active(self) -> bool:
        """Get whether the bot is active and able to process commands

        Returns:
            bool
        """
        return self._is_active
    
    def get_name(self) -> str:
        """Returns the name of the bot

        Returns:
            str: name
        """
        return self._name
    
    def on_user_register(self, u_id: int) -> bool:
        """Called when a new user registers

        Args:
            u_id (int): ID of registering user
        """
        return True
    
    def on_channel_join(self, c_id: int, u_id: int) -> bool: # pragma: no cover
        """Called when a user joins a channel

        Args:
            c_id (int): channel ID
            u_id (int): ID of user join channel
        """
        return True
    
    def on_message_send(self, msg_id: int) -> bool:
        """Called when a message was sent into a channel

        Args:
            msg_id (int): message that was sent
        
        Returns:
            bool: whether to continue notifying bots
                return False if actions have been taken that will prevent other
                bots from acting on the message (eg deleting it)
        """
        return True

class BotContainer(generic_data.GenericDataContainer):
    """Contianer for bot types (used in state)
    """
    def get(self, get_id: int) -> Bot:
        return super().get(get_id) # pragma: no cover
    
    def get_by_name(self, name: str) -> Bot:
        for bot in self._contained.values():
            if bot.get_name() == name:
                return bot
        raise KeyError(f"Bot with name '{name}' not found")
    
    def __iter__(self):
        return BotContainerIterator(self)

class BotContainerIterator(generic_data.GenericDataContainerIterator):
    def __next__(self) -> Bot:
        return super().__next__()

class CommandLinker:
    """Links commands to bot functions
    """
    def __init__(self):
        """Creates an instance of a command linker
        """
        self._links = dict()
    
    def register(self, name: str, instance, function):
        """Add a command to the list of commands, use this as a function 
        decorator to implicitly reg

        Args:
            name (str): name of command
            instance (bot): bot to call function in
            function (function): function to call

        Raises:
            ValueError: command already exists
        """
        if name in self._links: # pragma: no cover
            raise ValueError(f"This command already exists, and links to "
                                f"{self._links[name]}")

        # Insert the wrapper function into the dict of links
        self._links[name] = (instance, function)
    
    def run_command(self, name: str, args: list, c_id: int, u_id: int, m_id: int):
        """Runs a command

        Args:
            name (str): name of command to run
            args (list): command arguments
            c_id (int): channel where command was sent
            u_id (int): ID of user sending the command
            m_id (int): ID of message through which command was sent
        """
        # Attempt to run the command
        try:
            inst, func = self._links[name]
        except KeyError: # pragma: no cover
            # The function doesn't exist, return early
            return
        
        # Call the command
        if inst.is_active(): # pragma: no cover
            return func(args, c_id, u_id, m_id)
        else: return True

def activate_bot(bot_name):
    """Activates a bot to allow it to respond to commands and events

    Args:
        bot_name (str): Name of the bot to activate
    """
    state.s.bots.get_by_name(bot_name).activate()

def call_bots_method(method_name, *args):
    """Calls a method with all the requried args for every bot that is active

    Args:
        method_name (str): name of the method to call
    """
    for bot in state.s.bots:
        if bot.is_active():
            # If performing the action returns False, stop the actions
            if not bot.__getattribute__(method_name)(*args):
                break

def on_user_register(u_id):
    """Notify all bots that a user has registered

    Args:
        u_id (int): ID of registering user
    """
    call_bots_method("on_user_register", u_id)

def on_channel_join(c_id, u_id):
    """Called when a user joins a channel

    Args:
        c_id (int): channel ID
        u_id (int): ID of user join channel
    """
    call_bots_method("on_channel_join", u_id)

def on_message_send(msg_id):
    """Notify all bots that a message was sent

    Args:
        msg_id (int): message data of message that was sent
    """
    msg = state.s.messages.get(msg_id)
    # If the message was sent in a DM, return early, bots shouldn't have access
    # to messages sent in DMs
    try:
        state.s.dms.get(msg.get_channel_id())
        return
    except:
        # If it raised an error, the message was sent in a channel, and we can
        # notify our bots
        pass
    # Scan for command and parse out args, call on_command if applicable
    if str(msg).startswith("/"):
        # Slice out everything past the slash
        ret = on_command(str(msg)[1:], msg.get_channel_id(), msg.get_sender_id(), msg_id)
        if ret == False: return
    
    call_bots_method("on_message_send", msg_id)

def get_full_arg(cmd_list: list, i: int):
    """Appends items from the list to a string until
    the end char for an element is equal to the start of the first element

    Args:
        cmd_list (list): list of elements to parse
        i (int): starting index
    
    Returns:
        str: resultant argument
        int: new counter position
    """
    end_key = cmd_list[i][0]
    
    # If we finish the quote in this word
    if cmd_list[i].endswith(end_key):
        # Return it without the quotes
        return cmd_list[i][1:-1], i
    else:
        # Add this one without the opening quote to a string
        arg_str = cmd_list[i][1:]
        # Increment counter
        i += 1
        
        # Until we find one with a closing quote (if we search past the 
        # end of the list, we'll get an error: this means the command
        # was invalid and we shouldn't do anything)
        while not cmd_list[i].endswith(end_key):
            # Append the current one, then increment the counter
            arg_str += " " + cmd_list[i]
            i += 1
        
        # This one will finish with an ending quote
        # Append it without it
        arg_str += " " + cmd_list[i][:-1]
        
        # Return the full argument and the new index position
        return arg_str, i

def parse_args(cmd_list: list) -> list:
    """Generate a list of command arguments

    Args:
        cmd_list (list): list of words (split by spaces)

    Returns:
        list: list of command arguments
    """
    args = []
    i = 0
    while i < len(cmd_list):
        # Check for opening single quotes
        if cmd_list[i][0] in ["'", '"']:
            arg_str, i = get_full_arg(cmd_list, i)
            args.append(arg_str)
        # There was no opening quote
        else:
            # Append it normally
            args.append(cmd_list[i])
        
        # Increment the counter
        i += 1
    
    # Return the args list
    return args

def on_command(cmd_str: str, c_id: int, u_id: int, m_id: int):
    """Called when a message starts with a '/' character.
    Parses out command arguments, and attempts to call command with the linked
    bot

    Args:
        cmd_str (str): command string including arguments
        c_id (int): channel of command
        u_id (int): user initiating command
        m_id (int): ID of the message in which the command was initiated
    """
    # Split by spaces
    cmd_list = cmd_str.split(" ")
    
    command = cmd_list[0]
    
    if len(cmd_list) > 0:
        # Get the remaining args
        # If this fails, they were invalid (probably due to a quote imbalance)
        # So we should return
        try:
            args = parse_args(cmd_list[1:])
        except IndexError:
            return
    else:
        args = []
    
    # Run the command
    return state.s.commands.run_command(command, args, c_id, u_id, m_id)


from .. import state
