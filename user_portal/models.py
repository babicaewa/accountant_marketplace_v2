from django.db import models
from django.contrib.auth.models import User
from account.models import Client, Professional

class DealStage(models.Model):
    stage_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.stage_name}"

class ServicesType(models.Model):
    service_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.service_name}"

class ClientDeal(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_initiated = models.DateTimeField()
    completion_date = models.DateTimeField(null=True, blank=True)
    deal_stage = models.ForeignKey(DealStage, on_delete=models.CASCADE)

    def __str__(self):
        return f"deal: {self.id} {self.date_initiated} {self.professional.first_name} {self.professional.last_name} {self.client.first_name} {self.client.last_name}"

class ServiceDetails(models.Model):
    deal = models.ForeignKey(ClientDeal, on_delete=models.CASCADE)
    requested_services = models.ManyToManyField(
        ServicesType,
        through='RequestedService',
        related_name="service_details"
    )
    request_description = models.TextField()

    def __str__(self):
        return f"details for {self.deal}"

class RequestedService(models.Model):
    service_detail = models.ForeignKey(ServiceDetails, on_delete=models.CASCADE, related_name="requested_service_items")
    service_type = models.ForeignKey(ServicesType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.service_type.service_name}"

class DealDocument(models.Model):
    deal = models.ForeignKey(ClientDeal, on_delete=models.CASCADE)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='deal_documents/')
    uploaded_time = models.DateTimeField()

    def __str__(self):
        return f"document {self.file} for deal: {self.deal}"

class ChatMessage(models.Model):
    deal = models.ForeignKey(ClientDeal, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    time_sent = models.DateTimeField()

    def __str__(self):
        return f"{self.deal} message from {self.sender.username} at {self.time_sent}"

class DealNote(models.Model):
    deal = models.ForeignKey(ClientDeal, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return f"Note for deal_id: {self.deal}"



# Create your models here.
