# BestBot

This was I bot I created in December of 2020 to buy one of the Xbox Series Xs from bestbuy.com when they were very limited. This only works in FireFox and uses the webdriver directory on your computer. But this bot isn't only limited to the Xbox, it allows for any URL to be put into a config.ini file. I used the Twilio API (https://www.twilio.com/) to send text message updates to my phone so I would know when the item I was looking for was purchased for was found to be out of stock. I don't expect this code to be very efficient considering that it was my first semi-large Python project.

## Features
- Uses internal 'saved password' from FireFox so the only thing you have to input in the program is your credit card CVV
- Uses Twilio so you can receive text message updates about the product
- Refreshes your provided Best Buy search link to check for multiple products for the 'add to cart' element on the web-page
- Automates checkout so you don't have to buy it manually


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install BestBot.

```bash
pip install -r requirements.txt
```


## Dependencies

- [Python 3.8](https://www.python.org/downloads/release/python-386/)
- [FireFox](https://www.mozilla.org/en-US/firefox/new/)
- Your Best Buy account signed in, with your billing information saved on the account overview (you can only have one card on the account for this to work)
- The password saved (it's the notification the browser sends when you sign in)

![alt text](https://i.imgur.com/fjgXFZd.jpg)

### Webdriver
In Firefox you will find the webdriver path directy in about:profiles in the search bar of the browser. Make sure to copy the default-release.

### Batch

If you would like to endlessly run the script even when it crashes, then you should use the included .bat file. It's just a simple anti-crash script to keep it running when there is an error or when something has been closed.

### Commands
```bash
python bot.py
```

### Optional

Create your Twilio account to receive text messages from the bot, you must include the SID and the auth token.

![alt text](https://i.imgur.com/JWuxPPp.jpg)

Add the phone number given to you from Twilio in the format +1xxx-xxx-xxxx on lines 148 and 217 (it should go in from_ = ' ').

Example: (from_ = '+12138953638')
