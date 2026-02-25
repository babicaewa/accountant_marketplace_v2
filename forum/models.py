from django.db import models
from account.models import Client, Professional

class QuestionTags(models.Model):
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tag_name}"

class ForumQuestion(models.Model):
    asker = models.ForeignKey(Client, on_delete=models.CASCADE)
    time_posted = models.DateTimeField()
    post_title = models.CharField(max_length=1000)
    post_content = models.TextField()
    post_views = models.IntegerField()
    post_tags = models.ManyToManyField('QuestionTags', related_name='tag_names')

    def __str__(self): 
         return f"{self.post_title} - {self.asker.first_name} {self.asker.last_name}"

class ForumAnswer(models.Model):
    question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE)
    responder = models.ForeignKey(Professional, on_delete=models.CASCADE)
    time_responded = models.DateTimeField()
    answer_content = models.TextField()

    def __str__(self): 
        return f"{self.responder} - {self.question}"


