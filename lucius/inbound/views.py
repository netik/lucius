import sys

from django.shortcuts import render

# Create your views here.

# movies/views.py
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse

@csrf_exempt
def answer(request: HttpRequest) -> HttpResponse:
  vr = VoiceResponse()
  vr.say('I am Lucius. Here to help.')

  with vr.gather(
      action=reverse('login'),
      input='dtmf speech',
      speechTimeout='auto',
      timeout=10,
  ) as gather:
      gather.say('Please enter or say your PIN')

  vr.say('I did not receive your selection. Try Again.')
  vr.pause(1)
  vr.redirect('')

  return HttpResponse(str(vr), content_type='text/xml')

@csrf_exempt
def login(request: HttpRequest) -> HttpResponse:
  vr = VoiceResponse()

  digits = request.POST.get('Digits')
  speech = request.POST.get('SpeechResult')

  # Deal with this later.
  print ('DTMF entered: %s' % digits, sys.stderr)
  print ('SPEECH entered: %s' % speech, sys.stderr)

  vr.say('Authenticated.')
  vr.pause(1)
  vr.say('Hello, John')

  vr.redirect(reverse('main_menu'))

  return HttpResponse(str(vr), content_type='text/xml') 

@csrf_exempt
def main_menu(request: HttpRequest) -> HttpResponse:
  vr = VoiceResponse()
  vr.say('Main Menu')

  # if in emergency mode, say something
  vr.say('You are in emergency mode. Press 0 to hear the current delivery status.')
  vr.pause(1)

  vr.say('Please choose from the following options')
  vr.say('Press 1 for Check in')
  vr.say('2 to list or call Emergency Contacts')
  vr.say('3 for Add Contact')
  vr.say('4 for Remove Contact')

  # let us record a message and then send the message to everyone, should ask
  # for an SMS message and a voice message if we can do both at same time great.
  vr.say('9 to Activate Emergency Protocol')
  
  with vr.gather(
      action=reverse('main_menu_select'),
      input='dtmf speech',
      speechTimeout='auto',
      timeout=s,
  ) as gather:
      gather.say('Choose now')

  vr.say('I did not receive your selection. Try Again.')
  vr.pause(1)
  vr.redirect('')

  return HttpResponse(str(vr), content_type='text/xml')

@csrf_exempt
def main_menu_select(request: HttpRequest) -> HttpResponse:
  vr = VoiceResponse()

  digits = request.POST.get('Digits')
  speech = request.POST.get('SpeechResult')

  # Deal with this later.
  print ('DTMF entered: %s' % digits, sys.stderr)
  print ('SPEECH entered: %s' % speech, sys.stderr)

  vr.say('Got it.')
  vr.redirect(reverse('main_menu'))

  return HttpResponse(str(vr), content_type='text/xml') 
