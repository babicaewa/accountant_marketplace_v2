from django.contrib import admin
from .models import *

admin.site.register(ClientDeal)
admin.site.register(DealStage)
admin.site.register(ServicesType)
admin.site.register(ServiceDetails)
admin.site.register(DealDocument)
admin.site.register(ChatMessage)
admin.site.register(DealNote)
admin.site.register(RequestedService)

