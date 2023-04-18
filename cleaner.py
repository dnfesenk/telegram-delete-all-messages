import base64
import os
import tempfile
from time import sleep

from pyrogram import Client
from pyrogram.errors import FloodWait, UnknownError
from pyrogram.raw.functions.messages import Search
from pyrogram.raw.types import InputPeerSelf, InputMessagesFilterEmpty

# Retrieve API_ID and API_HASH from environment variables or user input
API_ID = os.getenv('API_ID', None)
API_HASH = os.getenv('API_HASH', None)

# Check if API_ID and API_HASH are defined, if not print error message and exit
if not API_ID or not API_HASH:
    print("Error: API_ID or API_HASH is not defined. Please provide valid values.")
    exit(-1)

# Retrieve the list of chats to exclude from the environment variable or use an empty set
# EXCLUDE = set(os.getenv("EXCLUDE", "").split(",")) if os.getenv("EXCLUDE") else set()

# Retrieve the list of chats to include from the environment variable or use an empty set
INCLUDE = set(os.getenv("INCLUDE", "").split(",")) if os.getenv("INCLUDE") else set()

# Base64 encoded session file string
base64_string = ""


# Function to write the base64 decoded session file to a temporary directory
def write_base64_to_temp_file():
    tmp_dir = tempfile.mkdtemp()
    file_path = os.path.join(tmp_dir, 'client.session')

    # Decode the base64 string and write it to the file
    with open(file_path, 'wb') as file:
        decoded_data = base64.b64decode(base64_string)
        file.write(decoded_data)

    print(f"Temporary file created at {tmp_dir}")
    return tmp_dir


# Create a temporary directory and write the decoded session file
temp_dir = write_base64_to_temp_file()

# Create a Pyrogram Client instance with the temporary session file
app = Client("client", api_id=API_ID, api_hash=API_HASH, workdir=temp_dir)
app.start()


# Cleaner class definition
class Cleaner:
    # Initialize the cleaner with optional chat list and chunk sizes
    def __init__(self, chats=None, search_chunk_size=100, delete_chunk_size=100):
        self.chats = chats or []
        if search_chunk_size > 100:
            # https://github.com/gurland/telegram-delete-all-messages/issues/31
            #
            # The issue is that pyrogram.raw.functions.messages.Search uses
            # pagination with chunks of 100 messages. Might consider switching
            # to search_messages, which handles pagination transparently.
            raise ValueError('search_chunk_size > 100 not supported')
        self.search_chunk_size = search_chunk_size
        self.delete_chunk_size = delete_chunk_size

        # Get all chats and exclude the ones specified in the EXCLUDE set
        self.chats = self.get_all_chats()
        groups_str = ', '.join(c.title for c in self.chats)
        print(f'\nSelected {groups_str}.\n')

    # Function to divide a list into n-sized chunks
    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l.
        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks#answer-312464"""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    # Function to get all chats of type 'group' and 'supergroup' that are not in the EXCLUDE set
    @staticmethod
    def get_all_chats():
        dialogs = app.get_dialogs(pinned_only=True)

        dialog_chunk = app.get_dialogs()
        while len(dialog_chunk) > 0:
            dialogs.extend(dialog_chunk)
            dialog_chunk = app.get_dialogs(offset_date=dialogs[-1].top_message.date - 1)

        # Return chats of type 'group' or 'supergroup' with titles not in the EXCLUDE set
        # return [d.chat for d in dialogs if d.chat.type in ('group', 'supergroup') and d.chat.title not in EXCLUDE]

        # Return chats of type 'group' or 'supergroup' with titles in the INCLUDE set
        return [d.chat for d in dialogs if d.chat.type in ('group', 'supergroup') and d.chat.title in INCLUDE]

    # Main function to run the cleaner
    def run(self):
        for chat in self.chats:
            peer = app.resolve_peer(chat.id)
            message_ids = []
            add_offset = 0

            # Search for messages in the current chat
            while True:
                q = self.search_messages(peer, add_offset)
                message_ids.extend(msg.id for msg in q['messages'])
                messages_count = len(q['messages'])
                print(f'Found {messages_count} of your messages in "{chat.title}"')
                if messages_count < self.search_chunk_size:
                    break
                add_offset += self.search_chunk_size

            # Delete the found messages
            self.delete_messages(chat.id, message_ids)

    # Function to delete messages in a chat using the message IDs
    def delete_messages(self, chat_id, message_ids):
        print(f'Deleting {len(message_ids)} messages with message IDs:')
        print(message_ids)
        for chunk in self.chunks(message_ids, self.delete_chunk_size):
            try:
                app.delete_messages(chat_id=chat_id, message_ids=chunk)
            except FloodWait as flood_exception:
                sleep(flood_exception.x)

    # Function to search for messages in a chat using the Pyrogram Search method
    def search_messages(self, peer, add_offset):
        print(f'Searching messages. OFFSET: {add_offset}')
        return app.send(
            Search(
                peer=peer,
                q='',
                filter=InputMessagesFilterEmpty(),
                min_date=0,
                max_date=0,
                offset_id=0,
                add_offset=add_offset,
                limit=self.search_chunk_size,
                max_id=0,
                min_id=0,
                hash=0,
                from_id=InputPeerSelf()
            ),
            sleep_threshold=60
        )


# Function to handle the execution of the Cleaner class
def handler(event, context):
    try:
        deleter = Cleaner()
        deleter.run()
    except UnknownError as e:
        print(f'UnknownError occurred: {e}')
        print('Probably API has changed, ask developers to update this utility')
    finally:
        app.stop()
