[python-download]: https://www.python.org/downloads/
[telegram-bot-tutorial]: https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064

![Python Badge](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Workflow branch master](https://github.com/amssdias/telegram-bot/actions/workflows/testing.yml/badge.svg?branch=master)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)

<h1 align=center>Telegram Bot</h1>

This is a bot where will show different images to the user, asking if the rocket has taken off yet (which you can know by looking at the countdown on the top-right corner of the video). Based on the answers, it will use a bisection algorithm to find the first image where the rocket launches, helping to pinpoint its occurrence date. There are 61696 frames in the video but you can find the interesting frame in only 16 steps.

## :hammer: Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Pre requisites

- [Python][python-download] - 3.9
- [Docker](https://www.docker.com/) (Optional)

### Installing


1. Clone this repository to your local machine
2. Navigate to the project directory


```
git clone https://github.com/amssdias/telegram-bot.git
cd telegram-bot
```

3. You should create a bot easily on telegram. You can see a tutorial on how to create a bot and get the token in [here][telegram-bot-tutorial].
   
4. On the ".env" file you should write your bot token like the following:

```
BOT_TOKEN=<YOUR_BOT_TOKEN>
```

#### Run with Docker

1. Build the Docker image:

```
docker build -t telegram-bot .
```

2. Run the Docker container:

```
docker run -it telegram-bot
```

#### Run without Docker


1. Install requirements with pip:

```python
pip install -r requirements.txt
```

2. Run program:

```python
python main.py
```


## :mag_right: Usage

Just follow the chat conversation on telegram.

Have fun :smile:
