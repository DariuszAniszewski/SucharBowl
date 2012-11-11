from django.http import HttpResponse
import simplejson
from django.views.decorators.http import require_POST
from suchar.models import Organisation
from django.core.mail import send_mail
from django.db import settings
@require_POST
def addOrganisation(request):
    name = request.POST.get("name",None)
    if name is None:
        return HttpResponse(status=400,content=simplejson.dumps({"error":"no name provided"}))
    email = request.POST.get("email",None)
    if email is None:
        return HttpResponse(status=400,content=simplejson.dumps({"error":"no email provided"}))

    if Organisation.objects.filter(name=name).exists():
        return HttpResponse(status=400,content=simplejson.dumps({"error":"Organisation already exists"}))



    organisation = Organisation()
    organisation.name = name
    organisation.email = email
    organisation.save()

    send_mail('Welcome to SucharBowl', 'Welcome to SucharBowl !', "sucharbowl@gmail.com",
    [email], fail_silently=False)


    response = {
        "id":organisation.id,
        "name":organisation.name,
        "api_key":organisation.api_key
    }
    return HttpResponse(status=200,content=simplejson.dumps(response))