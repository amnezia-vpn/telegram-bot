import telebot
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from server.apps.core.bot import bot


@csrf_exempt
def bot_view(request):
    if request.META["CONTENT_TYPE"] == "application/json":
        json_data = request.body.decode("utf-8")
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse(status=200)
    else:
        raise PermissionDenied
