"""
URL configuration for avoca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import core.views
import search.views
import account.views
import user_portal.views
import forum.views
import client_portal.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core.views.home, name="home"),
    path('search/', search.views.search_results, name="search_results"),
    path('profile/<str:first_name>_<str:last_name>_<int:id>/', search.views.profile, name='profile'),
    path('profile/<str:first_name>_<str:last_name>_<int:id>/send_service_request/', search.views.send_service_request, name='send_service_request'),
    path('login/', account.views.account_login, name='login'),
    path('logout/', account.views.logout_user, name='logout'),
    path('visit_portal/', core.views.visit_portal, name='visit_portal'),
    #path('user_portal/home/', user_portal.views.user_portal_home, name='portal_home'),
    path('user_portal/clients/', user_portal.views.user_portal_clients, name='portal_user_clients'),
    path('user_portal/clients/accept_service_request=<int:deal_id>/', user_portal.views.accept_service_request, name='accept_service_request'),
    path('user_portal/clients/deal/deal_id=<int:deal_id>/', user_portal.views.user_portal_client_details, name='portal_user_client_details'),
    path('user_portal/clients/upload_files=<int:deal_id>/', user_portal.views.upload_files, name='upload_files'),
    path('user_portal/clients/deal/deal_id=<int:deal_id>/download_file_file_name=<str:requested_file_name>/', user_portal.views.download_deal_file, name='download_deal_file'),
    path('user_portal/clients/deal/deal_id=<int:deal_id>/delete_file/', user_portal.views.delete_deal_file, name='delete_deal_file'),
    path('user_portal/clients/deal/deal_id=<int:deal_id>/send_msg', user_portal.views.send_message, name='send_message'),
    path('user_portal/clients/deal/deal_id=<int:deal_id>/update_msgs', user_portal.views.update_chat_messages, name='update_chat_messages'),
    path('user_portal/clients/deal/deal_id=<int:deal_id>/edit_notes', user_portal.views.update_notes, name='update_notes'),
    #path('user_portal/profile_analytics/', user_portal.views.user_portal_profile_analytics, name='portal_profile_analytics'),
    #path('user_portal/portal_forum/', user_portal.views.user_portal_forum, name='portal_forum'),
    #path('user_portal/portal_forum/question1', user_portal.views.user_portal_forum_question, name='portal_forum_question'),
    path('user_portal/edit_profile/', user_portal.views.edit_profile, name='edit_profile'),
    path('user_portal/edit_profile/update_experience_section/', user_portal.views.update_experience, name='update_experience'),
    path('user_portal/edit_profile/delete_experience=<int:experience_id>/', user_portal.views.delete_experience, name='delete_experience'),
    path('user_portal/documents/', user_portal.views.deal_documents, name='deal_documents'),
    path('user_portal/documents/<int:deal_id>/', user_portal.views.get_related_deal_documents, name='get_related_deal_documents'),
    path('user_portal/documents/get_all_folders', user_portal.views.get_all_deals_folders, name='get_all_deals_folders'),
    path('user_portal/billing_and_payments/', user_portal.views.user_billing_and_payments, name='user_billing_and_payments'),
    path('user_portal/settings/', user_portal.views.user_settings, name='user_settings'),
    path('client_portal/requests/', client_portal.views.client_portal_requests, name='client_portal_requests'),
    path('client_portal/requests/deal_id=<int:deal_id>', client_portal.views.client_portal_request_details, name='client_portal_request_details'),
    path('client_portal/billing_and_payments/201020304', client_portal.views.client_portal_billing_and_payments, name='client_portal_billing_and_payments'),
    path('forum/', forum.views.forum_home, name='forum_home'),
    path('forum_post/<str:question_title>_<int:id>/', forum.views.forum_post, name='forum_post'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
