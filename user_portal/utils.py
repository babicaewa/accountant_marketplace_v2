from .models import *
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from geopy.geocoders import Nominatim

def update_file_displays(deal, user):

    if Client.objects.filter(user=user).exists():
        is_client = True
    else:
        is_client = False
    try:
        deal_documents = DealDocument.objects.filter(deal=deal)

        client_uploaded_documents = deal_documents.filter(uploader=deal.client.user)
        for document in client_uploaded_documents:
            document.name = document.file.name.split('/')[-1]
            
        professional_uploaded_documents = deal_documents.filter(uploader=deal.professional.user)
        for document in professional_uploaded_documents:
            document.name = document.file.name.split('/')[-1]


        context = {
            "deal": deal,
            "is_client": is_client,
            "client_uploaded_documents": client_uploaded_documents,
            "professional_uploaded_documents": professional_uploaded_documents,
        }
        
        return context
    except Exception as e:
        return HttpResponse(f"Failed to update Files {e}")

def update_chat(deal, user):
    try:
        messages = ChatMessage.objects.filter(deal=deal).order_by('time_sent')
        if Client.objects.filter(user=user).exists():
            is_client = True
        else:
            is_client = False

        context = {
            "deal": deal,
            "is_client": is_client,
            "messages": messages,
        }
        
        return context
    except:
        return HttpResponse("Failed to update chat")
    

def get_lat_long(address):
    geolocator = Nominatim(user_agent="office_locator")
    location = geolocator.geocode(address)
    print(f"Address: {address}")
    print(f"location: {location}")
    if location:
        return location.latitude, location.longitude
    else:
        return None