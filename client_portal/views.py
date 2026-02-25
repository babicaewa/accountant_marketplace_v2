from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from account.models import Client, Professional
from user_portal.models import ClientDeal, DealStage
from user_portal.views import *

@login_required
def client_portal_requests(request):
    user = request.user
    client = Client.objects.get(user=user)

    completed_stage_object = DealStage.objects.filter(stage_name__icontains="Completed")

    client_deals = ClientDeal.objects.filter(client=client)
    
    all_current_client_deals = client_deals.exclude(deal_stage__in=completed_stage_object)
    all_archived_client_deals = client_deals.filter(deal_stage__in=completed_stage_object)
    

    context = {
        "client": client,
        "all_current_client_deals": all_current_client_deals,
        "all_archived_client_deals": all_archived_client_deals,
    }
    return render(request, 'client_portal/client_portal_requests.html', context)

@login_required
def client_portal_request_details(request, deal_id):
    deal = get_object_or_404(ClientDeal, id=deal_id)
    is_client = True

    service_desc = ServiceDetails.objects.get(deal=deal)
    line_items = service_desc.requested_services.through.objects.filter(service_detail=service_desc)
    messages = ChatMessage.objects.filter(deal=deal).order_by('time_sent')
    deal_notes = DealNote.objects.filter(deal=deal).first()
    deal_documents = DealDocument.objects.filter(deal=deal)

    if request.method == "POST":
        if "change_stage_confirm_button" in request.POST:
            stage = request.POST.get("stage-option")
            if stage == "pending_client_action":
                deal.deal_stage = DealStage.objects.get(stage_name="Pending Client Action")
            elif stage == "ready_for_preparation":
                deal.deal_stage = DealStage.objects.get(stage_name="Ready for Preparation")
            elif stage == "awaiting_approval":
                deal.deal_stage = DealStage.objects.get(stage_name="Awaiting Approval")
            
            deal.save()

    client_uploaded_documents = deal_documents.filter(uploader=deal.client.user)
    for document in client_uploaded_documents:
        document.name = document.file.name.split('/')[-1]
        
    professional_uploaded_documents = deal_documents.filter(uploader=deal.professional.user)
    for document in professional_uploaded_documents:
        document.name = document.file.name.split('/')[-1]



    context = {
        "deal": deal,
        "service_desc": service_desc,
        "line_items": line_items,
        "messages": messages,
        "deal_notes": deal_notes,
        "client_uploaded_documents": client_uploaded_documents,
        "professional_uploaded_documents": professional_uploaded_documents,
        "is_client": is_client,
    }

    return render(request, 'client_portal/client_portal_request_details.html', context)


@login_required
def client_portal_billing_and_payments(request):
    return render(request, 'client_portal/client_portal_billing_and_payments.html')
