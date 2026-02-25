from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from account.models import *
from .utils import *
from forum.models import ForumQuestion
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from django.http import FileResponse
from django.db.models import Q
from django.utils import timezone
from random import choice

@login_required
def user_portal_home(request):
    forum_question_pks = ForumQuestion.objects.values_list('pk', flat=True)
    random_pk = choice(forum_question_pks)
    random_forum_question = ForumQuestion.objects.get(pk=random_pk)

    context = {
        "random_forum_question": random_forum_question,
    }

    return render(request, 'user_portal/portal_home.html', context)

@login_required
def user_portal_clients(request):
    user = request.user
    professional = Professional.objects.get(user=user)

    completed_stage_object = DealStage.objects.filter(stage_name__icontains="Completed")
    new_request_stage_object = DealStage.objects.filter(stage_name__icontains="New Service Request")


    all_deals = ClientDeal.objects.filter(professional=professional)
    all_new_service_requests = all_deals.filter(deal_stage__in=new_request_stage_object)

    try:
        for service_request in all_new_service_requests:
            service_desc = ServiceDetails.objects.get(deal=service_request)
            service_request.service_details = service_desc
            service_request.line_items = service_desc.requested_services.through.objects.filter(service_detail=service_desc)


    except:
        print(f"no service details were found! for {service_request}")



    all_current_deals = all_deals.exclude(deal_stage__in=completed_stage_object)
    all_archived_deals = all_deals.filter(deal_stage__in=completed_stage_object)

    new_service_count = 0
    pending_client_action_count = 0
    ready_for_preparation_count = 0
    awaiting_approval_count = 0

    for deal in all_current_deals:
        if deal.deal_stage.stage_name == "New Service Request":
            new_service_count += 1
        elif deal.deal_stage.stage_name == "Pending Client Action":
            pending_client_action_count += 1
        elif deal.deal_stage.stage_name == "Ready for Preparation":
            ready_for_preparation_count += 1
        elif deal.deal_stage.stage_name == "Awaiting Approval":
            awaiting_approval_count += 1


    context = {
        "all_current_deals": all_current_deals,
        "all_archived_deals": all_archived_deals,
        "all_new_service_requests": all_new_service_requests,
        "new_service_count": new_service_count,
        "pending_client_action_count": pending_client_action_count,
        "ready_for_preparation_count": ready_for_preparation_count,
        "awaiting_approval_count": awaiting_approval_count,

    }

    return render(request, 'user_portal/portal_user_clients.html', context)

@login_required
def accept_service_request(request, deal_id):
    try:
        deal = get_object_or_404(ClientDeal, id=deal_id)
        accepted_first_stage = DealStage.objects.get(stage_name="Pending Client Action")
        deal.deal_stage = accepted_first_stage
        deal.save()

        return redirect('portal_user_clients')

    except:
        return HttpResponse(f"failed to accept request")



@login_required
def user_portal_client_details(request, deal_id):

    user = request.user

    deal = get_object_or_404(ClientDeal, id=deal_id)
    is_client = False

    service_desc = ServiceDetails.objects.get(deal=deal)
    line_items = service_desc.requested_services.through.objects.filter(service_detail=service_desc)
    messages = ChatMessage.objects.filter(deal=deal).order_by('time_sent')
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
        "user": user,
        "deal": deal,
        "service_desc": service_desc,
        "line_items": line_items,
        "messages": messages,
        "client_uploaded_documents": client_uploaded_documents,
        "professional_uploaded_documents": professional_uploaded_documents,
        "is_client": is_client,
    }
    return render(request, 'user_portal/portal_user_client_details.html', context)

@login_required
def upload_files(request, deal_id):
    try:
        deal = get_object_or_404(ClientDeal, id=deal_id)
        all_files = request.FILES.getlist("uploaded_files")

        for file in all_files:
            new_document = DealDocument(deal=deal, uploader=request.user, file=file, uploaded_time=timezone.now())
            new_document.save()

        context = update_file_displays(deal, request.user)
        
        return render(request, 'user_portal/client_details_documents_partial.html', context)
    except Exception as e:
        return HttpResponse(f"Failed to upload files. Please try again. {e}")
    
@login_required
def download_deal_file(request, deal_id, requested_file_name):
    user= request.user

    deal = get_object_or_404(ClientDeal, id=deal_id)

    if deal.professional.user == user or deal.client.user == user:
        try:
            all_deal_documents = DealDocument.objects.filter(deal=deal_id)

            for document in all_deal_documents:
                document_name = document.file.name.split('/')[-1]
                if document_name == requested_file_name:
                    response = FileResponse(document.file.open("rb"), as_attachment=True)
                    return response
        except:
            return HttpResponse("Failed to download file.")
    return HttpResponse("You do not have permission to download these files.")

@login_required
def delete_deal_file(request, deal_id):
    user = request.user
    deal = get_object_or_404(ClientDeal, id=deal_id)
    requested_file_name = request.POST.get('file-to-delete-name')

    if deal.professional.user == user or deal.client.user == user:
        try:
            query = Q(deal=deal_id) & Q(uploader=user)
            all_user_uploaded_documents = DealDocument.objects.filter(query)

            for document in all_user_uploaded_documents:
                document_name = document.file.name.split('/')[-1]
                if document_name == requested_file_name:
                    document.file.delete()
                    document.delete()
                    break
            
            context = update_file_displays(deal, user)
        
            return render(request, 'user_portal/client_details_documents_partial.html', context)
        except:
            return HttpResponse(f"Failed to upload files. Please try again.")
        
    return HttpResponse("You do not have permission to delete this file.")

@login_required
def send_message(request, deal_id):
    try:
        deal = get_object_or_404(ClientDeal, id=deal_id)
        user = request.user
        message_text = request.POST.get("inputted-msg")

        new_message = ChatMessage(deal=deal, sender=user, message=message_text, time_sent=timezone.now())
        new_message.save()

        context = update_chat(deal, user)
        
        return render(request, 'user_portal/client_details_chat_partial.html', context)
    except Exception as e:
        return HttpResponse(f"Failed to send message. Please try again. {e}")

@login_required
def update_chat_messages(request, deal_id):
    try:
        deal = get_object_or_404(ClientDeal, id=deal_id)
        user = request.user

        context = update_chat(deal, user)
        
        return render(request, 'user_portal/client_details_chat_partial.html', context)
    except Exception as e:
        return HttpResponse(f"Failed to send message. Please try again. {e}")

@login_required
def update_notes(request, deal_id):
    try:
        deal = get_object_or_404(ClientDeal, id=deal_id)
        user = request.user
        notes_text = request.POST.get("deal-notes-text")
        
        deal_notes = DealNote.objects.filter(deal=deal)

        if notes_text:
            if deal_notes.exists():
                deal_notes = deal_notes.first()
                deal_notes.note = notes_text
                deal_notes.save()
            else:
                deal_notes = DealNote(deal=deal, note=notes_text)
                deal_notes.save()
        else:
            deal_notes = None

            
        
        context = {"deal": deal,
                   "deal_notes": deal_notes}
        
        return render(request, 'user_portal/client_details_notes_partial.html', context)
    except:
        return HttpResponse("Failed to update your notes. Please try again.")


@login_required
def user_portal_profile_analytics(request):
    return render(request, 'user_portal/portal_profile_analytics.html')

@login_required
def user_portal_forum(request):
    return render(request, 'user_portal/portal_forum.html')

@login_required
def user_portal_forum_question(request):
    return render(request, 'user_portal/portal_forum_question.html')

@login_required
def edit_profile(request):
    user = request.user
    professional = get_object_or_404(Professional, user=user)

    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        bio = request.POST.get('bio-input')
        bio_quote = request.POST.get('bio-input-quote')
        all_languages = request.POST.get('all-spoken-languages').split(',')
        
        professional.languages_spoken.clear()

        for language in all_languages:
            spoken_language = Languages.objects.get(language=language)
            professional.languages_spoken.add(spoken_language)

        professional.first_name = first_name
        professional.last_name = last_name
        professional.bio = bio
        professional.bio_quote = bio_quote

        professional.save()


        office_address = request.POST.get('office-address')
        office_city = request.POST.get('office-city')
        office_province = request.POST.get('office-province')
        office_postal_code = request.POST.get('office-postal-code')

        office_location = OfficeLocations.objects.filter(professional=professional)

        if office_location.exists():
            office_location = office_location.first()
        else:
            office_location = OfficeLocations(professional=professional)

        office_location.address = office_address
        office_location.city = office_city
        office_location.province = office_province
        office_location.postal_code = office_postal_code

        full_address_string = f"{office_address}, {office_city}, {office_province} {office_postal_code}"

        office_location.lat, office_location.long = get_lat_long(full_address_string)
        print(f"{office_location.lat}  {office_location.long}")

        office_location.save()
        


        
        consultation_fee = request.POST.get('consultation-fee')
        personal_tax_return_fee = request.POST.get('personal-tax-return-fee')
        business_tax_return_fee = request.POST.get('business-tax-return-fee')

        all_service_objects = {}
        all_service_objects[Service.objects.get(service_name="Consultation")] = consultation_fee
        all_service_objects[Service.objects.get(service_name="Personal Tax Return")] = personal_tax_return_fee
        all_service_objects[Service.objects.get(service_name="Business Tax Return")] = business_tax_return_fee

        all_professional_service_infos = ServiceInfo.objects.filter(professional=professional)
        
        for service in all_service_objects:
            fee = all_service_objects[service]
            if fee:
                service_info_details = all_professional_service_infos.filter(service=service)
                if service_info_details.exists():
                    service_info_details = service_info_details.first()
                    service_info_details.fee = fee
                else:
                    service_info_details = ServiceInfo(professional=professional, service=service, fee=all_service_objects[service])
                
                service_info_details.save()







    professional_services = ServiceInfo.objects.filter(professional=professional)

    all_experiences = ExperienceDetails.objects.filter(professional=professional).order_by('-start_year')

    all_languages = Languages.objects.all()

    available_services = {}

    for service in professional_services:
        service_name = service.service.service_name.replace(" ", "_")
        available_services[service_name] = service.fee


    try:
        professional_office = OfficeLocations.objects.get(professional=professional)
    except:
        professional_office = None
        print("No office location found")

    

    context = {
        "professional": professional,
        "professional_office": professional_office,
        "available_services": available_services,
        "all_languages": all_languages,
        "all_experiences": all_experiences,
    }
    return render(request, 'user_portal/portal_edit_profile.html', context)

@login_required
def update_experience(request):
    user = request.user
    professional = get_object_or_404(Professional, user=user)

    try:
        if request.method == "POST":
            experience_id = request.POST.get("experience-id")
            job_title = request.POST.get("job-title")
            company = request.POST.get("company")
            start_year = request.POST.get("start-year")
            end_year = request.POST.get("end-year")
            if not end_year:
                end_year = None
            focus = request.POST.get("work-focus")


            if experience_id:
                new_experience = ExperienceDetails.objects.get(id=experience_id)
                if new_experience.professional != professional:
                    return HttpResponse("You do not have permission to change this object.")
                new_experience.company_name = company
                new_experience.role=job_title
                new_experience.start_year=start_year
                new_experience.end_year=end_year
                new_experience.focus=focus
            else:
                new_experience = ExperienceDetails(professional=professional, 
                                                   company_name=company, 
                                                   role=job_title, 
                                                   start_year=start_year, 
                                                   end_year=end_year, 
                                                   focus=focus)
            new_experience.save()


        all_experiences = ExperienceDetails.objects.filter(professional=professional).order_by('-start_year')
    
        context = {
            "all_experiences": all_experiences,
        }

        return render(request, 'user_portal/edit_profile_experience_partial.html', context)
        
    except:
        HttpResponse("Failed to add/edit experience")

@login_required
def delete_experience(request, experience_id):

    try:
        user = request.user
        professional = Professional.objects.get(user=user)

        experience = ExperienceDetails.objects.get(id=experience_id)

        experience.delete()

        all_experiences = ExperienceDetails.objects.filter(professional=professional).order_by('-start_year')
    
        context = {
            "all_experiences": all_experiences,
        }

        return render(request, 'user_portal/edit_profile_experience_partial.html', context)
    
    except:
        HttpResponse("Failed to delete the selected experience.")

@login_required
def deal_documents(request):
    user = request.user
    professional = get_object_or_404(Professional, user=user)
    all_deals = ClientDeal.objects.filter(professional=professional)

    context = {
        "professional": professional,
        "all_deals": all_deals,
    }

    return render(request, 'user_portal/portal_all_documents.html', context)

@login_required
def get_related_deal_documents(request, deal_id):
    user = request.user
    professional = get_object_or_404(Professional, user=user)
    deal = get_object_or_404(ClientDeal, id=deal_id)
    all_documents = DealDocument.objects.filter(deal=deal)

    for document in all_documents:
        document.document_name = document.file.name.split('/')[-1]
        if (document.file.size / 1000) < 1000:
            document.file_size = f"{round(document.file.size / 1000,2)} KB"
        elif (document.file.size / 1000000) < 1000:
            document.file_size = f"{round(document.file.size / 1000000,2)} MB"
        else:
            document.file_size = f"{round(document.file.size / 1000000000,2)} GB"

    context = {
        "professional": professional,
        "deal": deal,
        "all_documents": all_documents,
    }

    return render(request, 'user_portal/all_deals_deal_documents_partial.html', context)

@login_required
def get_all_deals_folders(request):
    
    user = request.user
    professional = get_object_or_404(Professional, user=user)
    all_deals = ClientDeal.objects.filter(professional=professional)

    context = {
        "professional": professional,
        "all_deals": all_deals,
    }

    return render(request, 'user_portal/all_deals_folders_partial.html', context)


@login_required
def user_billing_and_payments(request):
    return render(request, 'user_portal/portal_billing_and_payments.html')

@login_required
def user_settings(request):
    return render(request, 'user_portal/portal_user_settings.html')

