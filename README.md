# lucius

Lucius is a Concerige for human diasters.
A Twilio-based IVR and "Deadman's" switch and recovery system for at-risk humans

## Deadman

For example, you can ask lucius to call you once every N days. If you don't
acknolwedge the call with your cdoe,  lucius can call other people and deliver
your message to a contact list of humans.

## Contacts

Maybe you're an at-risk individual, journalist or other person. Maybe you only get one phone call. 

What do you do? Call Lucius and get connected to your contact list.

Can't make any calls? Let Lucius deal with it for youl

## SMS / Message Blast

Lucius will keep trying until someone picks up.

# Installation
## 1. venv Setup and Module installation.

This thing runs under venv but to save space we don't check in the venv.

From the top-level directory, generate a new virtual environment and activate it.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
pip install --upgrade pip           # if need be
```

From there, we can start the server.

```
cd lucius
python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py runserver  
```

## 2. Set up a tunnel to Twilio with Ngrok

In another window, let's get ngrok running.

As this entire service depends on Twilio, we need a way to connect Twilio to your
dev instance. For this we're going to just `ngrok`.

Install ngrok from https://ngrok.com/

Sign up on their site and get an authtoken. (see https://dashboard.ngrok.com/get-started/setup)

I like to install ngrok in my ~/bin folder and then add `export PATH=$PATH:$HOME/bin` to my `.profile`. How you handle this install is up to you.

Then you can do `ngrok http 8000` in a new window, and ngrok will start forwarding.

## 3. Sign up for Twilio, buy a phone number, and connect Twilio to ngrok.

After you've purchased a phone number from Twilio, you need to connect the Voice and Messaging services to ngrok.

Click on the phone number in Twilio, Click on Voice & Fax, and set the following options in Twilio. 

"A call comes in: Webhook" to be `https://XXXXXX.ngrok.io/inbound/answer`

"A message comes in: Webhook" to be `https://XXXXXX.ngrok.io/inbound/sms`

Both options should be using HTTP POST.

The ngrok.io address should match whatever ngrok has assigned to you. 

Do not worry about any of the other settings for now.


