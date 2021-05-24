# views_ivr.py
#
# these views produce Twilio XML for the IVR response system.

import sys
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth import login
from django.utils import timezone, dateformat
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from twilio.twiml.voice_response import VoiceResponse

from .models import Profile
from django.core.exceptions import ObjectDoesNotExist

MAX_BAD_LOGINS=3

LONG_DATE_FMT="%a, %B %d, %Y %I:%M %p"

# make this "dtmf speech" if you want to pay for speech recognition, it's
# expensive at 0.02 USD / second
ACCEPTED_TEL_INPUTS="dtmf"

# utility functions go here --------------------------------------------
def parse_digits_or_speech(digits, speech):
  # if we have digits from Twilio, they take prececendce. 
  if digits:
    if len(digits) > 0:
      return digits.strip()

  if speech:
    if len(speech) > 0:
      # Twilio sends random responses here
      # there might be a better way to do this but I can't find it.
      str = speech
      str = str.replace("Zero" ,"0")
      str = str.replace("One"  ,"1")
      str = str.replace("Two"  ,"2")
      str = str.replace("Three","3")
      str = str.replace("Four" ,"4")
      str = str.replace("Five" ,"5")
      str = str.replace("Six"  ,"6")
      str = str.replace("Seven","7")
      str = str.replace("Eight","8")
      str = str.replace("Nine" ,"9")
      str = str.replace("-","").strip()
      str = str.replace("-","").strip()
      str = str.replace(".","").strip()
      return str

  return False

def check_in(profile):
  # everything's okay, check us in...
  profile.in_emergency = False
  profile.emergency_started = None
  profile.last_check_in = timezone.now()
  profile.checked_in_until = timezone.now() + timezone.timedelta(minutes=profile.check_interval)
  profile.save()

def set_emergency(profile, state):
  profile.in_emergency = state
  if not state:
    profile.emergency_started = None
  else:
    profile.emergency_started = timezone.now()
  profile.save()

def get_profile(request):
  # returns or loads the active user profile
  if request.user:
    return request.user.profile
  return False

# (END) utility functions go here ----------------------------------------

# Start Views ------------------------------------------------------------
@csrf_exempt
def answer(request: HttpRequest) -> HttpResponse:
  # 10 minutes max, this is a call after all.
  request.session.set_expiry(600)

  vr = VoiceResponse()
  vr.say('I am Lucius. Here to help.')

  # TODO: Frontend this with an account number request/store into session
  # A pin by itself is just insecure
  with vr.gather(
      action=reverse('pin_login'),
      input=ACCEPTED_TEL_INPUTS,
      speechTimeout='auto',
      timeout=10,
  ) as gather:
      gather.say('Please enter or say your PIN')

  vr.say('I did not receive your selection. Try Again.')
  vr.pause(1)
  vr.redirect('')

  return HttpResponse(str(vr), content_type='text/xml')

@csrf_exempt
@login_required
def start_set_check_interval(request: HttpRequest, vr=None) -> HttpResponse:
  # we're either getting called after a bad entry and reusing vr, or we're a
  # fresh request
  if not vr:
    vr = VoiceResponse()

  with vr.gather(
      action=reverse('set_check_interval'),
      input=ACCEPTED_TEL_INPUTS,
      speechTimeout='auto',
      timeout=10
  ) as gather:
      gather.say('Enter the number of minutes between checks followed by pound.')
  return HttpResponse(str(vr), content_type='text/xml')

@csrf_exempt
@login_required
def set_check_interval(request: HttpRequest) -> HttpResponse:
  vr = VoiceResponse()

  digits = request.POST.get('Digits')
  speech = request.POST.get('SpeechResult')

  print ('%s' % (request.session.session_key), file=sys.stderr)
  print ('DTMF entered: %s' % digits, file=sys.stderr)
  print ('SPEECH entered: %s' % speech, file=sys.stderr)

  parsed_time = parse_digits_or_speech(digits, speech)
  new_interval = int(parsed_time)

  if parsed_time <= 60:
    vr.say("Invalid time. Time must be at least 60 minutes.")
    vr.redirect(reverse('start_set_check_interval'))

  request.user.profile.check_interval = int(parsed_time)
  request.user.profile.save()

  vr.say('Check interval set to %d minutes. You are checked in.' % int(parsed_time))
  check_in(request.user.profile)
  vr.pause(1)
  vr.redirect(reverse('main_menu'))
  return HttpResponse(str(vr), content_type='text/xml') 

@csrf_exempt
@login_required
def finish_recording(request: HttpRequest, vr=None) -> HttpResponse:
  active_profile = get_profile(request)
  
  if not vr:
    vr = VoiceResponse()

  if request.POST.get('RecordingSid'):
    active_profile.message_url = request.POST.get('RecordingUrl')
    active_profile.message_sid = request.POST.get('RecordingSid')
    active_profile.save()
    
    vr.say('recording updated')
    check_in(request.user.profile)
  else:
    vr.say('recording failed, try again')
  vr.pause(1)
  vr.redirect(reverse('main_menu'))

  return HttpResponse(str(vr), content_type='text/xml') 

@csrf_exempt
@login_required
def record_message(request: HttpRequest, vr=None) -> HttpResponse:
  # we're either getting called after a bad entry and reusing vr, or we're a
  # fresh request
  if not vr:
    vr = VoiceResponse()
  
  vr.say("set your outgoing message now, then press pound")
  vr.record(max_length="30", 
            action=reverse('finish_recording'), 
            finish_on_key='#',
            play_beep=True)

  return HttpResponse(str(vr), content_type='text/xml') 

@csrf_exempt
def pin_login(request: HttpRequest) -> HttpResponse:
  vr = VoiceResponse()

  digits = request.POST.get('Digits')
  speech = request.POST.get('SpeechResult')

  # Deal with this later.
  print ('%s' % (request.session.session_key), file=sys.stderr)
  print ('DTMF entered: %s' % digits, file=sys.stderr)
  print ('SPEECH entered: %s' % speech, file=sys.stderr)

  parsed_pin = parse_digits_or_speech(digits, speech)
  print ('Find user with pin %s' % speech, file=sys.stderr)

  # find the user and log them in -------------------------------
  active_profile = None
  duress_profile = None
  duress = False

  try:
    active_profile = Profile.objects.get(pin=parsed_pin)
  except ObjectDoesNotExist:
    print ('Pin not found %s' % parsed_pin, file=sys.stderr)

  if not active_profile:
    try:
      duress_profile = Profile.objects.get(duress_code=parsed_pin)
    except ObjectDoesNotExist:
      print ('(optional) Duress code not found %s' % parsed_pin, file=sys.stderr)

    # handle duress
    if duress_profile:
      print ('Duress code found %s' % parsed_pin, file=sys.stderr)
      active_profile = duress_profile
      duress = True
    
  if not active_profile:
    bad_logins = request.session.get('bad_logins', 0)
    request.session['bad_logins'] = int(bad_logins) + 1
    request.session.modified = True

    # handle excessive login attempts here. 
    if (request.session['bad_logins'] >= MAX_BAD_LOGINS):
      vr.say('Too many attempts. Goodbye.')
      vr.pause(1)
      vr.hangup()
      return HttpResponse(str(vr), content_type='text/xml') 

    print ('Invalid Login %s (#%d)' % (parsed_pin, bad_logins), file=sys.stderr)
    vr.say('I could not find you. Try Again.')
    vr.pause(1)
    vr.redirect(reverse('answer'))
    return HttpResponse(str(vr), content_type='text/xml') 

  # we're good now. 
  login(user=active_profile.user, request=request)

  if active_profile.user.first_name:
    vr.say("Authenticated! Hello, %s" % active_profile.user.first_name)
  else:
    vr.say("Authenticated! Hello there.")

  if duress:
    vr.say('Duress code entered. Starting Emergency Procedure')
    set_emergency(active_profile, True)

  vr.redirect(reverse('main_menu'))

  return HttpResponse(str(vr), content_type='text/xml') 


@csrf_exempt
@login_required
def ivr_help(request: HttpRequest) -> HttpResponse:
  vr = VoiceResponse()
  active_profile = get_profile(request)
  
  vr.say('Please choose from the following options')

  vr.say('Press 1 for Check in,') #done
  vr.say('2 to Set check interval,') #done
  
  vr.say('3 to Play current Outgoing Message,')
  vr.say('4 to Replace Outgoing Message,') 

  vr.say('5 to List and call Emergency Contacts,')
  vr.say('6 to Add a Contact,')
  vr.say('7 to Remove a Contact.')

  # 9 emergency
  # 0 delivery status

  if active_profile and not active_profile.in_emergency:
    vr.say('9 to Activate Emergency Protocol')
  else:
    vr.say('9 to Cancel Emergency Protocol')

  vr.redirect(reverse('main_menu'))

  return HttpResponse(str(vr), content_type='text/xml') 

@csrf_exempt
@login_required
def main_menu(request: HttpRequest) -> HttpResponse:
  # this should always return something
  active_profile = get_profile(request)
  
  vr = VoiceResponse()
  vr.say('Main Menu')

  # status report goes here.
  # if in emergency mode, say something about that...
  if active_profile and active_profile.in_emergency:
    vr.say('You are in emergency mode. Press 0 to hear the current delivery status.')
    # n of m of your contacts have been reached... etc...
    vr.pause(1)
  else:
    vr.say("There is no Emergency right now.")

  with vr.gather(
      action=reverse('main_menu_select'),
      input=ACCEPTED_TEL_INPUTS,
      speechTimeout='auto',
      timeout=10,
      numDigits=1
  ) as gather:
      gather.say('Select option or star for help:')

  vr.say('I did not receive your selection. Try Again.')
  vr.redirect('')

  return HttpResponse(str(vr), content_type='text/xml')

@csrf_exempt
@login_required
def main_menu_select(request: HttpRequest) -> HttpResponse:
  active_profile = get_profile(request)
  vr = VoiceResponse()

  digits = request.POST.get('Digits')
  speech = request.POST.get('SpeechResult')

  # Deal with this later.
  print ('DTMF entered: %s' % digits, sys.stderr)
  print ('SPEECH entered: %s' % speech, sys.stderr)

  parsed_choice = parse_digits_or_speech(digits, speech)

  # menu options
  valid_opt = False

  # handle options
  # list / connect contacts
  # add contacts
  # remove contacts

  if (parsed_choice == "1"):
    valid_opt = True
    check_in(active_profile)
    date_string = datetime.strftime(timezone.now(),LONG_DATE_FMT)
    vr.say("You have checked in at %s" % date_string)

  if (parsed_choice == "2"):
    valid_opt = True
    return start_set_check_interval(request, vr)

  if (parsed_choice == "4"):
    valid_opt = True
    return record_message(request, vr)

  if (parsed_choice == "*"):
    valid_opt = True
    vr.redirect(reverse('ivr_help'))

  if parsed_choice == "9":
    valid_opt = True
    set_emergency(active_profile, not active_profile.in_emergency)
    if active_profile.in_emergency:
      vr.say('Emergency Protocol is now On.')
    else:
      vr.say('Emergency Protocol is now Off.')

  if not valid_opt:
    vr.say("Invalid menu selection.")
    vr.redirect(reverse('main_menu'))

  return HttpResponse(str(vr), content_type='text/xml') 
