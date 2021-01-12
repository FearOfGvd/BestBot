# BestBot

This was I bot I created in December of 2020 to buy one of the Xbox Series Xs from bestbuy.com when they were very limited. This only works in FireFox and uses the webdriver directory on your computer. But this bot isn't only limited to the Xbox, it allows for any URL to be put into a config.ini file. I used the Twilio API (https://www.twilio.com/) to send text message updates to my phone so I would know when the item I was looking for was purchased for was found to be out of stock. I don't expect this code to be very efficient considering that it was my first semi-large Python project.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install BestBot.

```bash
pip install -r requirements.txt
```


## Usage

Login to your Best Buy account on FireFox, but make sure you click 'save password' because this requires you to have the email and password saved so the bot can login every time it needs to create a new tab.

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

Then add the phone number given to you from Twilio in the format of +1xxx-xxx-xxxx on lines 148 and 217 (put the number where it says from_ = ' ').

Example: (from_ = '+12138953638')
