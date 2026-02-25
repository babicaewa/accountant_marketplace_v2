from django.shortcuts import render
from account.models import *
from .utils import *
from django.db.models import Avg, Count, Min
from django.db.models import Q
from django.shortcuts import get_object_or_404
import numpy as np

# Create your views here.
def search_results(request):
    
    service_type = request.GET.get("serviceType")
    language = request.GET.get("language")
    location = request.GET.get("location")

    location_radius = request.GET.get("location-radius")
    if location_radius:
        location_radius = int(location_radius)

    maximum_rate = request.GET.get("rate")
    if maximum_rate:
        maximum_rate = int(maximum_rate)

    filter_query = Q()

    if service_type and service_type != "Any Service":
        filter_query &= Q(services_available__service_name=service_type)

    if maximum_rate:
        filter_query &= Q(professional_services__fee__lte=maximum_rate)

    if language:
        filter_query &= Q(languages_spoken__language=language)

    filtered_professionals = Professional.objects.filter(filter_query)

    if location:
        searched_location = CITIES_COORDINATES[location]
        professionals_within_radius = []
        for professional in filtered_professionals:
            professional_office = OfficeLocations.objects.get(professional=professional)
            office_coords = (professional_office.lat, professional_office.long)
            if within_radius(office_coords, searched_location, location_radius):
                professionals_within_radius.append(professional.id)

        filtered_professionals = filtered_professionals.filter(id__in=professionals_within_radius)

    all_searched_professionals = filtered_professionals.annotate(
        avg_review_score = Avg('reviews__review_rating'),
        reviews_count = Count('reviews'),
    )

    service_type = Service.objects.filter(service_name=service_type).first()

    for p in all_searched_professionals:
        if service_type and service_type != "Any Service":
            p.search_service_fee = ServiceInfo.objects.get(professional=p, service=service_type)
        most_recent_employment = ExperienceDetails.objects.filter(professional=p).order_by("start_year").last()
        print(f"waa: {most_recent_employment}")
        p.professional_title = most_recent_employment.role
        p.professional_company = most_recent_employment.company_name

        if p.avg_review_score:
            if p.avg_review_score % 1 >= 0.5:
                p.half_star_index = (p.avg_review_score // 1) + 1
            else:
                p.half_star_index = -1
        else:
            p.avg_review_score = -1

    all_langauges = Languages.objects.all().order_by('language')
    print(all_langauges)

    

    context = {'professionals': all_searched_professionals,
               'all_languages': all_langauges,
               "service_name": service_type,}

    return render(request, "search/search_results.html", context)

def profile(request, first_name, last_name, id):

    professional = get_object_or_404(Professional, id=id)

    professional_experience = ExperienceDetails.objects.filter(professional=professional).order_by("-start_year")
    most_recent_experience = professional_experience.first()

    professional_services = ServiceInfo.objects.filter(professional=professional)

    try:
        office_location = OfficeLocations.objects.get(professional=professional)
        office_location_string = f"{office_location.address}, {office_location.city} {office_location.province} {office_location.postal_code}"
        location_lat, location_long = office_location.lat, office_location.long
    except:
        office_location = None
        office_location_string = None
        location_lat = None
        location_long = None

    professional_reviews = Reviews.objects.filter(professional=professional)

    reviews_count = professional_reviews.count()

    if reviews_count > 0:
        review_rating_counts = np.zeros(5, dtype=int)    #array to hold total of each rating (i.e. 2 of 1 star, 3 of 2 star, etc.), going from 1-5 stars
        avg_review_rating = 0
        for review in professional_reviews:
            review_rating_counts[review.review_rating-1] += 1
            avg_review_rating += review.review_rating

        avg_review_rating = avg_review_rating / reviews_count
        if avg_review_rating % 1 >= 0.5:
            half_star_index = (avg_review_rating // 1) + 1
        else:
            half_star_index = -1

        review_rating_counts_percentages = np.round(review_rating_counts / reviews_count*100)
        review_rating_counts_percentages = review_rating_counts_percentages.astype(np.int32)

    else:
        avg_review_rating = None
        half_star_index = None
        review_rating_counts_percentages = None

    context = {"professional": professional,
               "professional_experience": professional_experience,
               "professional_services": professional_services,
               "most_recent_experience": most_recent_experience,
               "location_address": office_location_string,
               "location_lat": location_lat,
               "location_long": location_long,
               "professional_reviews": professional_reviews,
               "total_professional_reviews_count": reviews_count,
               "avg_review_rating": avg_review_rating,
               "half_star_index": half_star_index,
               "review_rating_counts_percentages": review_rating_counts_percentages,
               }
    return render(request, "search/profile.html", context)

def send_service_request(request, first_name, last_name, id):

    if request.method == "POST":
        for key, value in request.POST.items():
            print(f"{key} -> {value}")
    return

