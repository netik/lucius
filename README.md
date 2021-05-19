# lucius

Lucius is a Concerige for human diasters.
A Twilio-based IVR and "Deadman's" switch and recovery system for at-risk humans

## Deadman

For example, you can ask lucius to call you once every N days. 
If you don't acknolwedge the call with your cdoe,  lucius can call other people and deliver your message to a contact list of humans.

## Contacts

Maybe you're an at-risk individual. 
Maybe you only get one phone call. 

What do you do? Call Lucius and get connected to your contact list.

Can't make any calls? Let Lucius deal with it for youl

## SMS / Message Blast

Lucius will keep trying until someone picks up.

## Starting

This thing runs under venv, start with

```
source venv/bin/activate
python manage.py runserver  
python manage.py migrate --run-syncdb
python manage.py createsuperuser
```

This helps...
```
python manage.py migrate --run-syncdb
```


