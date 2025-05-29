# KokosBotPot

A general-purpose discord bot. It provides a variety of commands to interact with the bot such as reminders, image resizing, conversation with gemini and much more...

## Commands List

<details>
<!-- <summary></summary> -->

|       Commands | Description                                                   |
| -------------: | ------------------------------------------------------------- |
|           ping | Pings the bot and returns the latency                         |
|           send | Bot sends the text in the provided channel                    |
|            tag | Displays info and the avatar of the given user                |
|           time | Returns the time                                              |
|          timer | Sets a timer (reminder)(text command)                         |
|       reminder | Set reminder using slash command                              |
|    delreminder | Deletes a reminder using slash command                        |
| delallreminder | Deletes all reminders using slash command                     |
|   getreminders | Gets all of your pending reminders using slash command        |
|         gemini | get answered to your question using google's gemini pro model |
|         github | Get info of any repository from github                        |
|         invert | Invert the color of the image                                 |
|     pingalinga | Spam pings any member of the server                           |
|      advertise | Advertise your image                                          |
|          clown | Make yourself a clown                                         |
|   doublestruck | Sends the message with doublestruck font                      |
|          embed | Send an embed                                                 |
|    imageresize | Resize your image by height width and aspect ratio            |
|           jail | Put someone behind the jail bar 👿                            |
|        uncover | uncover yourself                                              |

</details>

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/leeh-nix/kokoPotBot.git
   cd kokoPotBot
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment variables

```sh
TOKEN=your-discord-bot-token
MONGODB_URI=your-mongodb-uri
GEMINI_API_KEY=your-gemini-api-key
URL_ENDPOINT=your-imagekit-url-endpoint
```

## Contributing

Contributions are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
