# Tour Tracker

Tour Tracker is a Python project that tracks upcoming concerts by selected music artists and sends Telegram notifications when new events are announced.

## How it works

Each artist or music venue has a website where upcoming events are published. Tour Tracker uses custom parsers to collect concert information from these websites.

The process works as follows:

- On the first run, the project collects all currently announced events and saves them to the database.
- Every day, it checks the websites for updates.
- If new events are found, they are added to the database.
- A Telegram message is sent for each new event.

## Project scripts

The project has three main scripts:

- **`initial_load.py`** — First-time setup. Collects all current events, creates the database table, and fills it with events. It also adds a special event called a *heartbeat event*, used to check that the system is working.

- **`main.py`** — Collects current events, checks for new ones, saves them to the database, sends Telegram notifications.

- **`heartbeat.py`** — Retrieves the special heartbeat event from the database and sends it to Telegram. This helps check that the main services are working, even when no new concerts are announced.

All script logs are saved in the `logs` directory.

## Getting started

### Configure event sources

The `config` directory contains [`sources_dummy.py`](https://github.com/TAbramovskaya/tour-tracker/blob/main/config/sources_dummy.py). It is an example configuration with one source.

To add your own sources, rename `sources_dummy.py` to `sources.py` and follow the existing source dictionary structure. Each source requires: artist's name, a unique parser name, the base URL of the website, URL suffix — the remaining part of the URL.

The URL is split into two parts because event links in the HTML response are often relative paths. This makes it easier to build full URLs for event pages and gives you more flexibility when parsing different parts of the website.

### Build a parser

Each parser must return a list of `Event` objects. The `Event` model is defined in `models/event.py` and contains the following fields:

- `artist` — artist or performer name
- `title` — event title
- `date` — event date
- `location` — concert venue or location
- `url` — link to the event page

All fields are stored as text in the database. There are no specific format requirements or restrictions on their content, except that they must not be empty. Feel free to use any text format or include any additional details you find useful. 

You can use your browser's Inspect tool to find the CSS selectors you need.

### Example source and parser

[`parcer_3.py`](https://github.com/TAbramovskaya/tour-tracker/blob/main/parsers/parser_3.py) is written for the Rotterdam Philharmonic Orchestra website. It collects concerts featuring Rachmaninoff's music from the [concert agenda](https://www.rotterdamsphilharmonisch.nl/agenda).

### Configure Telegram

To send notifications, you need a Telegram bot.

- Create a bot using [@BotFather](https://t.me/BotFather).
- Get your bot token (`BOT_TOKEN`).
- Find the chat ID where the bot should send messages (`CHAT_ID`).

For more information, see the [Telegram Bot API documentation](https://core.telegram.org/bots/api).

The repository contains an example environment file named [`.env_dummy`](https://github.com/TAbramovskaya/tour-tracker/blob/main/.env_dummy). Add your bot token and chat ID to this file, and rename it to `.env`.

### Run the initial setup

Before starting the daily checks, run `initial_load.py`. This will collect the currently announced events and populate the SQLite database.

You only need to do this once when setting up the project. 

You can then run `heartbeat.py` to check that Telegram notifications are working.

### Automation

I use `cron` to run the project scripts automatically:

- `main.py` runs once a day to check for new concerts.
- `heartbeat.py` runs once a week to make sure everything is working.

You can use other task schedulers depending on your operating system.

Happy concert hunting! 

### Tech stack

- Python — main programming language
- SQLite — stores all collected events
- Telegram Bot API — sends notifications
- `cron` — automates scheduled runs
