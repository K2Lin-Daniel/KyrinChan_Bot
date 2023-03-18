### KyrinChan Bot🌸

[![Docker Build](https://github.com/K2Lin-Daniel/KyrinChan_Bot/actions/workflows/docker-latest.yml/badge.svg)](https://github.com/K2Lin-Daniel/KyrinChan_Bot/actions/workflows/docker-latest.yml)

Kyrin Chatbot is a QQ & Telegram bot that uses OpenAI's ChatGPT & Microsoft New Bing for chatting. It adds a custom text rejection feature not included in the original branch, as well as a custom rendering style and a character who plays a cute cat girl named Kyrin Chan.

## Features 💡

- Chat with Kyrin Chan using natural language
- Enjoy her cute and funny responses
- Customize her appearance and personality
- Reject unwanted texts with a custom list
- Switch between ChatGPT and New Bing engines

## Installation 🛠️

To install Kyrin Chatbot, you need to have Python 3.6 or higher and pip installed on your system. Then follow these steps:

1. Clone this repository: `git clone https://github.com/K2Lin-Daniel/mirai-newbing-bot.git`
2. Enter the project directory: `cd mirai-newbing-bot`
3. Install the required dependencies: `pip3 install -r requirements.txt`
4. Create a config file: `cp config.example.cfg config.cfg`
5. Edit the config file with your own settings (see below)
6. Run the bot: `python3 bot.py`

## Configuration ⚙️

The config file contains several options that you can customize according to your preferences.

- `qq`: The ID of your QQ bot account
- `access_token`: The API key of your OpenAI account
- `cookie_content`: The cookie of your Microsoft Bing account

If you want to chat with ChatGPT using Telegram bot, you need to do the following steps:

- Delete the `[mirai]` block in `config.cfg`
- Add the following configuration in `config.cfg`:

```properties
[telegram]
# This token is obtained from BotFather
bot_token = "your Bot token"
# If deployed in China, fill this to set proxy
# If not filled, it will read the system proxy settings
proxy = "http://localhost:1080"
```

- Find your created bot on Telegram and send `/start` to start chatting👍


## Contributing 🙌

If you want to contribute to this project, feel free to fork it and make a pull request. You can also open an issue if you find any bugs or have any suggestions.

Please follow these guidelines when contributing:

- Use descriptive commit messages and comments
- Follow PEP 8 style guide for Python code
- Write tests for new features or bug fixes

## License 📄

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.
