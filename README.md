# PrimeNow available windows checker

Bot to check if there are available windows on amazon prime now.

#### Requirements

- PrimeNow account.
- Docker.
- Python >= 3.7 (if you don't use docker).

#### Instructions

- Copy environment file example .env.example to .env and fill it:
    - Telegram vars:
        - `TELEGRAM_BOT_ACTIVE`: Indicate if telegram notifications active (0 or 1)
        - `TELEGRAM_BOT_TOKEN`: Telegram bot token (view telegram instructions)
        - `TELEGRAM_BOT_ID`: Telegram bot id (view telegram instructions)
    
    - Cookies vars: until login will be developed, you must provide these cookie values (you cant get it making a request and inspect it on chrome network tab):
        - `COOKIE_UBID`
        - `COOKIE_X_ACBES`
        - `COOKIE_AT_ACBES`
        - `COOKIE_SESS_AT_ACBES`
        
- Set merchant variables on `merchants.json` if there ins't your merchant.

*Docker usage instructions*
- Build docker image: `docker image build -t primenow_checker .`

*Python command line usage instructions*
- Install dependencies: `pip install -r requirements.txt`

#### Telegram instructions

To get telegram notifications, you must follow create your own bot following this instructions:

- Search @BotFather on Telegram.
- Send `/start` to join it.
- Send `/newbot` to create your own bot.
- Enter a bot name.
- Enter a unique bot username (it has to end with `_bot`).
- Copy the `token` and join to it with your account (search it by username).
- To get the `id`, join to it and on same session (browser), navigate to `https://api.telegram.org/bot<token>/getUpdates` and search the `id` on json.

#### Usage

- Using docker: `docker container run -it primenow_checker`.
- Using python command line: `python app.py`.
- Follow the instructions.

#### Additional info

- If you don't want to put your credentials on .env file, you can pass it on docker run execution:

```
docker container run -e ENV_VAR=xxxx -e ENV_VAR=xxxx -e ... -it primenow_checker
```

#### TODO

- Login with username/password instead cookies.
- Specify product when is unavailable on notification.

#### Disclaimers

- This script works only on spanish prime now version.
- Use only for study purposes.
- Use under your own risk.