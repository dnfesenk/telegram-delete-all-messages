# Telegram Group Cleaner

Telegram Group Cleaner is a Python script that helps you delete all your messages in Telegram groups and supergroups.

## Features

- Deletes all your messages in specified groups and supergroups.
- Supports filtering groups by their titles.
- Handles rate limits imposed by the Telegram API.
- Can be easily deployed to serverless platforms like Yandex Cloud Functions.

## Requirements

- Python 3.7 or higher
- [Pyrogram](https://github.com/pyrogram/pyrogram) library

# Installation

1. Clone the original repository:

```
git clone https://github.com/gurland/telegram-delete-all-messages.git
cd telegram-delete-all-messages
```

2. Follow the instructions in the repository's README to set up the required environment variables and generate
   the `client.session` file.

3. Encode the `client.session` file as a base64 string:

On Linux:

```
base64 -w0 client.session > client_session_base64.txt
```

On Windows (using PowerShell):

```
[System.Convert]::ToBase64String([System.IO.File]::ReadAllBytes("client.session")) | Set-Content -Path "client_session_base64.txt"
```

4. Open the `client_session_base64.txt` file, copy the base64 string, and replace the value of the `base64_string`
   variable in the `cleaner.py` script with the copied string.

5. Proceed with the rest of the instructions in this README to use the Telegram Group Cleaner script.

## Obtain standalone telegram app API credentials

- Login to https://my.telegram.org/
- Select `API development tools` link
- Create standalone application
- Copy app_id and app_hash

## Deployment to Yandex Cloud Functions

This script can also be used as a Yandex Cloud Function. To deploy it, follow
the [official Yandex Cloud Functions documentation](https://cloud.yandex.com/en-ru/docs/functions/quickstart) and use
the `handler` function from the `cleaner.py` script as the entry point.

## Required environment variables:

```
API_ID=<your_api_id>
API_HASH=<your_api_hash>
INCLUDE=<comma_separated_list_of_group_titles>
```

Replace `<your_api_id>`, `<your_api_hash>`, and `<comma_separated_list_of_group_titles>` with your actual API ID, API
hash, and a comma-separated list of group titles you want to include, respectively.

## Disclaimer

Please be aware that using this script may result in the permanent deletion of your messages in the specified Telegram
groups and supergroups. Use this script at your own risk. We are not responsible for any loss or damage caused by the
use of this script.

This script is provided "as is" without warranty of any kind, either expressed or implied, including, but not limited
to, the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality
and performance of the script is with you. Should the script prove defective, you assume the cost of all necessary
servicing, repair, or correction.

In no event shall the author, the organization he represents, or anyone else involved in the creation, production, or
delivery of the script be liable for any damages whatsoever (including, without limitation, damages for loss of business
profits, business interruption, loss of business information, or any other pecuniary loss) arising out of the use of or
inability to use the script, even if the author has been advised of the possibility of such damages.

By using this script, you agree to assume all risks and responsibilities associated with its use. The author and any
contributors are not responsible for any loss, damage, or harm that may result from your use of the script, including
but not limited to data loss, privacy breaches, or any other negative consequences. You understand and acknowledge that
you are using this script at your own risk, and you agree to hold the author and any contributors harmless from any
claims, losses, or damages that may arise as a result of your use of the script.

### License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.