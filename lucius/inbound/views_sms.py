from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def sms_response(request):
  # Start our TwiML response
  resp = MessagingResponse()

  # Add a text message
  #msg = resp.message("Check out this sweet owl!")

  # Add a picture message
  #msg.media("https://demo.twilio.com/owl.png")

  # cmds:
  #   "reset password"
  
  msg = resp.message("Lucius Got that")
  return HttpResponse(str(resp))
