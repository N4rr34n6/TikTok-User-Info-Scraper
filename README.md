This Python script allows you to fetch detailed information about TikTok users by their username or user ID, without requiring logins or API keys. It extracts various user data such as follower counts, video counts, likes, and more.

## Features

- Fetch user information by TikTok username or user ID.
- Works without logins and without using APIs.
- Extracts:
  - User ID
  - Unique ID
  - Nickname
  - Follower count
  - Following count
  - Likes count
  - Video count
  - Biography (signature)
  - Verified status
  - SecUid
  - Comment settings
  - Private account status
  - Region
  - Heart count
  - Digg count
  - Friend count
  - Profile picture URL
- Downloads the profile picture to your local machine.

---

### TikTok User Information Scraper Bot

For user convenience, I have developed a bot that streamlines the process of retrieving TikTok user information. You can interact with this bot directly at the following link: [TikTok User Info Scraper Bot](https://t.me/TiTokUserInfoScraper_BOT).

This bot is built based on the functionalities of the Python script and eliminates the need for manual execution of the code. Simply provide a TikTok username or user ID, and the bot will retrieve detailed user information in a structured format, including follower count, likes, videos, and more. 

This solution allows seamless integration without requiring any logins, APIs, or external dependencies.

---

## Requirements

- Python 3.x
- `requests` library

You can install the required library using pip:

```bash
pip3 install requests
```

## Usage

Run the script from the command line. You can specify either a TikTok username or user ID. Use the `--by_id` flag if you are providing a user ID.

### Example

To get help and usage information, you can run:

```bash
python3 TikTok.py -h
```

This will display:

```
usage: TikTok.py [-h] [--by_id] identifier

Get TikTok user information

positional arguments:
  identifier  TikTok username or user ID

optional arguments:
  -h, --help  show this help message and exit
  --by_id     Indicates if the provided identifier is a user ID
```

To get information using a username:

```bash
python3 TikTok.py @username [or username]
```

To get information using a user ID:

```bash
python3 TikTok.py --by_id user_id 
```

### Output

The script will print the following user information to the console:

- User ID
- Username
- Nickname
- Followers
- Following
- Likes
- Videos
- Biography
- Verified status
- SecUid
- Comment setting
- Private account status
- Region
- Heart count
- Digg count
- Friend count
- Profile picture URL

Additionally, the profile picture will be downloaded and saved as `unique_id_profile_pic.jpg` in the current directory.

## Notes

- Ensure that the TikTok user account is public to access their information.
- The scraping technique relies on the current structure of the TikTok website, which may change.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for more details.

