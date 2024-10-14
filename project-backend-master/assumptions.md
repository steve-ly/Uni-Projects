# Assumptions

This file contains the assumptions we have made while working on the project.

Check here first if anything works weirdly, and add things here if you make an assumption.

# `src/`

## `admin.py`

### Deleting users

When a user is deleted:

 - Their handle is set to "removed_user". This is to make sure that the handle isn't used by users that have no
use for it (since they're deleted).
 - Their email is set to be empty, so that they aren't blocked from creating a new account in the future. This also
prevents them from logging into their existing account.
 - Their active sessions are all logged out, so that they can't continue using ✨Dreams✨ afterwards.
 - They are removed as members of every channel and they were in. This is to prevent member lists from being cluttered
with users who have been deleted.
 - Their user ID is persisted, so that any references to it (tags, sent messages, etc) won't be broken.
 - Their profile becomes locked and unmodifiable. This is to prevent people from doing things such as adding removed
users to channels.

As well as this:

 - Assume that removed users cannot be tagged. This is because there is the potential for multiple users to have the
`@deleted_user` handle, as well as because that sort of thing just doesn't make sense.
 - Assume that deleted profiles aren't included in the "All Members" list. This is to prevent clutter.

## `auth.py`
 - Assume that the 20 character limit for handle only applies to the concatenation of first and last names. 
It can exceed it if the final result of the handle generated results in it ending with a number 
(ie when a user with that name already exists). Quoting the interface table (section 6.2): 
*"The addition of this final number **may** result in the handle exceeding the 20 character limit"*.
We have chosen to interpret *may* as (insert these in place of it) *"is allowed to"*, rather than a 
*"be careful, it might"*.
- Assume that auth logout does not return is_success false for invalid token
Inferred from forum post https://edstem.org/courses/5306/discussion/404252, instead of the function
returning a boolean, it will raise an Access error in the case of an invalid token being inputted.
-When requesting a password, the most recent reset code is the only valid one.
If a user attempts to request multiple times, any previous reset code will be invalidated


## `channel.py`

**channel structure**
 - Assume that global owners are only channel owners for the duration of their global ownership. 
If they are removed as a global owner (in a future iteration), their ownership of all channels 
will be terminated. A side effect of this is that users should be able to add a global owner as
the local owner of a channel, even if they are listed as a channel owner (due to their global 
ownership). If that is done, their ownership of that channel will be persisted even if they are 
removed as a global owner.

**`channel_join_v1()`**
 - Assume that if a user is already a member of a channel, they won't be added again, but no
exceptions will be raised. A similar line of reasoning applies for `channel_invite_v1()`.

**`channel_leave_v1()`**
 - Assume that if a user who is already a member of a channel is invited again, no action should
be taken, and no exceptions should be raised.

**`channel_leave_v1()`**
 - Assume that if a local channel owner leaves a channel, they forfeit their ownership of the
channel, and will not be an owner of that channel, even if they are added back to it.

**`channel_addowner_v1()` and `channel_removeowner_v1()`**
 - Assume that global owners can add and remove local owners for channels they aren't a member of
 - Assume that channels with no local owners can exist (can remove last local owner). If this is
done, a future owner of the channel will only be able to be added by a global owner.

**`channel_messages_v1`**
 - The start index is invalid if it is greater than total number of messages in the channel.
When start index equals number of messages, the value of key 'messages' in the returned dictionary 
should be an empty list. Supported by 
[this forum response](https://edstem.org/courses/5306/discussion/384787).
 
## `channels.py`

**`channels_create_v1`**
 - The user creating the new channel should be added to the channel by default.
This is because otherwise it'd be impossible to join a private channel unless 
you were the global owner. Supported by 
[this forum response](https://edstem.org/courses/5306/discussion/379718).

## DMs
 
### DM removal

 - Assume that when a DM is removed, all the messages that have been sent to it are also removed.
otherwise, there would be orphanes messages where their channel wouldn't exist anymore.

## `echo.py`

## `error.py`

The following assumtpions are made about generic error cases (ones that aren't outlined in the docs):

**`InputError`** whenever:
 - An ID (eg user ID, channel ID, message ID) doesn't correspond to the required input. 
For example if a user with that particular ID doesn't exist when you try to send a message with it.

### Note on error hierarchy:

When an exception is raised for any reason, the exception class should be determined by making checks in the following order

1. **`AccessError`** Invalid `auth_user_id`
2. **`InputError`** Invalid references: eg IDs refer to non-existant users, channels or messages.
3. **`AccessError`** Action not allowed: eg a user doesn't have permission to perform the requested action.
4. **`InputError`** Invalid parameters: eg a user attempts to send a message that is too long.

This logic applies since, ordinarily, steps **2**, **3** and **4** shouldn't be reached if step **1** fails, 
steps **3** and **4** can't be reached if step **2** fails, and the functions shouldn't 
even go anywhere near adding the data if the current user doesn't have the permissions (hence having step **3** before step **4**).

## `identifier.py`

 - We have designated that `0` is an invalid identifier to help keep the code pythonic with the `get_new_identifier()` while loop,
and to ensure full code coverage.

 - We have assumed that identifiers should never be removed from the list of used identifiers (excluding a full reset of the program). 
This is to ensure that newly generated identifiers can't refer to previously deleted content. For example, if a message is
shared to a channel, then the original is deleted, then if the identifier was removed and another message is sent and happens to 
have the same ID, it will appear as the message that was shared, even if it wasn't.

## `message.py`

**`message_send_v1()`**
 - Assume that empty messages cannot be sent, as empty messages result in the deletion of the message in `message_edit_v1()`.

**`message_edit_v1()`**
 - Assume that users can edit messages they have sent, even if they are no-longer a member of the channel the message was sent in.

**`message_remove_v1()`**
 - Assume that users can delete messages they have sent, even if they are no-longer a member of the channel the message was sent in.

**`message_share_v1()`**
Note that we a treating this as a shared message, as opposed to a copy-paste (since if the user wanted to do that,
they could do it manually). Our assumptions are based on this idea, and have resulted in shared messages being dynamic
in the sense that they update whenever the original message updates (like an embed would)

 - Assume the format of shared messages: the original message is wrapped by three quotation marks, and if there is optional message 
 provided, it is on a newline and without quotation marks.

     - Example 1:

        Original:
        ```
        Hello world
        ```

        Shared:
        ```
        """
        Hello world
        """
        ```

     - Example 2:

        Original: 
        ```
        Hello world
        ```

        Additional:
        ```
        GG
        ```

        Shared: 
        ```
        """
        Hello world
        """

        GG
        ```

 - Assume that although the total length of a shared message (the og message and the comment) can exceed 1000 characters, neither should be able to do so individually.

 - Assume that when a message that has been shared gets edited, all of the shares of it will also update their quote. This is to get similar parity with the auto-updating
nature of tagging.

 - Assume that when a message that has been shared gets deleted, all of the shares of it will have their originals replaced with `[Message deleted]`.

### Tagging

 - Assume that tags can be present in any part of a message; even with no preceding whitespace, for example
_"How cool is [this video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) that I found@myfriend check it out!!!"_ would be a valid tag
even though the preceding character is a 'd'.

 - Assume that a handle used in a tag will always have whitespace (' ', '\n', '\t') after it. This is so that tagged users' handles 
can be parsed easily. If this assumption wasn't made then conflicts could be created. For example, if we had two users with the
handles `some` and `someone`, then writing `@someoneelse` could possibly refer to either of them. To avoid this confusion, we elected
that tags should end with whitespace.

 - Assume that if a user is tagged in a message, and then that user updates their handle, the tag message will also be updated to
reflect their new handle. This is to ensure that conversations don't become confusing if later a user updates their handle, leaving
an orphaned tag. If a user no-longer exists, their tag will match their handle (refer to assumptions on deleting users).

 - Assume that if a user tags themselves, they won't recieve a notification for it. Refer to assumptions on `notification.py` principle 1.

 - Assume that if a user tags a person multiple times, the user will only recieve a single notification for the action. This is to
prevent notification clogging.

 - Assume that if a user removes a message in which users are tagged, the associated notifications will also be retracted. Refer 
to assumptions on `notification.py` principle 2.

 - Assume that if a user edits a message in which users are tagged, the associated notifications will be updated to match the new
content. If a user is no-longer tagged, their notification is retracted. If a user is newly-tagged, they are sent a notification.
If a user is still tagged, their notification text is updated to include the new edited message, but they aren't sent a new
notification. Refer to assumptions on `notification.py` principle 3.

## `notification.py`

When designing the notification system, our team decided on the following principles:

1. Users cannot take action that will give themselves a notification. This is because a user shouldn't need to be notified of their
own actions.

2. Assume that notifications are retracted if their context is removed. This is to prevent orphaned notifications if the content they
are associated with is removed.

3. Assume that if the associated content of a notification is updated, the notification will be updated to match it. This is to ensure
that if content is edited, the previous state of the content isn't kept anywhere.

4. Assume that in the notification message, the sender's handle will be preceded with an `@` character. This is to help signify that
it is a handle.

## `other.py`

## `user.py`

### Handles

 - Assume that handles cannot contain whitespace or the `@` symbol. This is to ensure that they can be parsed correctly from tags

 - Assume that if a user attempts to change their handle to their current handle, nothing will happen. No exceptions will be raised

# `tests/`

## `auth_test.py`

**Testing `auth_register_v1()`**
 - As it is near impossible to conduct blackboxed tests that do anything to ensure the validity of the results, 
aside from the assertion that the `auth_user_id` is an int, we have elected to use some 
internal helper functions to ensure the validity of the data, namely, `get_user_by_email()` and `get_user_by_handle()`. 
We intend to use the proper front-facing functions in `src/user.py` as soon as they are 
implemented, but this cannot be done until iteration 2.
