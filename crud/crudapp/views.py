from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Entries
import json

# Create your views here.
def home(request):
    return render(request, "home.html")

def takeData(request):
    data = json.loads(request.body.decode("utf-8"))

    #Fetch and Create entry
    Entries.objects.create(
        name = data.get("name"),
        phone = int(data.get("phone")),
        email = data.get("email"),
        city = data.get("city"),
        state = data.get("state"),
        country = data.get("country"),
        pin = int(data.get("pincode")),
    )

    return JsonResponse({"resp":"got it"})

def gallery(request):
    all_data = Entries.objects.all()
    return render(request, "gallery.html", {"entries":all_data})

def userAction(request):
    req = json.loads(request.body.decode("utf-8"))
    action = req.get("action")
    id = req.get("id")

    match(action):
        case "create":
            pass

            return JsonResponse({"resp":"Done"})
        case "view":
            entry = Entries.objects.filter(id=id)

            return JsonResponse({"resp":"Done"})
        case "edit":
            pass
        case "delete":
            obj = Entries.objects.filter(id=id)
            obj.delete()

            return JsonResponse({"resp":"Done"})
        case default:
            return JsonResponse({"resp":"Wrong choice"})