# Python-Wallet-Tracker-Telegram-bot

---
### Calculation of expenses and income

---
I have tried many similar applications but they all are uncomfortable to use, so I created my own. The bot has Main Menu with seven buttons. You can create your own categories of income and expenses and add title and amount of income/expense to these categories. Also you can put on display the current amount of expenses/income separately for each category and the total current amount of expenses/income of all categories, by one command. Every 1st day of a new month, the bot sends a general report of expenses/income. I also implemented the ability to switch between three languages (en, uk, ru). Every day at 15:00 a reminder is sent to all users to fill in new expenses/income.

---
To install requirements run:

`pip install -r requirements.txt`

---

Copy file `example.env` into `.env` and replace `TOKEN` with your token from the Telegram

---

To run:

`python main.py`

---
Tables schema:

![tables](docs/pics/Telegram_bot_diagram.png)

---
Telegram bot link

https://t.me/Pocket_manage_bot
