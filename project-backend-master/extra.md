
# Extra Features

## Bots

Basic support for bots has been added, with the standups system using this feature set for its implementation.

There are also two other bots that are much more visible:

* Activator Bot can be used to activate other bots. To do so, send a message with the following format: `/activate <bot_name>`.

* Welcome Bot can be used to send a customisable welcome message to a user that has just registered. It must first be activated by running the command `/activate Welcome`. After that, the welcome message can be customised by server admins using the command `/welcome customise [message]`.

* A complex system for registering commands has been put into place. It has been coded so that no bots can register the same command.

* Bots can also respond to events such as `on_user_register()` or `on_message_send()`.

## Classes

The entire data structure has been migrated to classes. These classes make use of inheritance and polymorphism to reduce the amount of repeated code. They allow for many time-saving techniques, such as operating on an `AbstractChannel` which can be either a `Dm` or a `Channel` object.

## Self-updating data system

Many components of the data structure automatically update if things they reference change.

* Quoted messages will update if the original is edited.

* Notifications will be retracted for tags if a message tagging someone is removed or edited to exclude that tag (but people won't get a new notification every time a message tagging them is edited).

* Notifications will be retracted for reactions if a user removes their reaction to a post.

These are best observed using the front-end.
