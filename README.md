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

If you need to get out of the virtual environment, type `deactivate` or just close the Terminal window.

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

## 4. Simple Tests

Going to `https://XXX.ngrok.io/` should get you to the login page if all is working correctly, and `https://XXX.ngrok.io/inbound/answer` should get you the 1st page of TwiML, for the voice IVR. That page should come back something like:

```
<Response>
<Say>I am Lucius. Here to help.</Say>
<Gather action="/login/" input="dtmf speech" speechTimeout="auto" timeout="10">
<Say>Please enter or say your PIN</Say>
</Gather>
<Say>I did not receive your selection. Try Again.</Say>
<Pause length="1"/>
<Redirect/>
</Response>
```

# Database Backend

By default lucius uses a sqlite database. You are welcome to move Django over to use Postgres, MySQL, or any other supported database backend. There's hundreds of tutorials out there for doing so, and this one is decent:  `https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django`


# Costs


# Security

In a production site you should enable `SECURE_SSL_REDIRECT = True` in settings.py and force users to use HTTPS. Enabling this with ngrok creates an infinite 301 redirect loop. 

Unforunately when using ngrok trying to have HTTPS redirects working is very hard right now, I haven't figured this out (yet) and will come up with a solution at some point.
