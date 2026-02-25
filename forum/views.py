from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from account.models import Professional
from django.db.models import F

# Create your views here.

def forum_home(request):

    forum_questions = ForumQuestion.objects.all()
    forum_questions_count = forum_questions.count()
    forum_answers_count = ForumAnswer.objects.all().count()
    forum_tags = QuestionTags.objects.all()

    total_professionals_count = Professional.objects.all().count()


    context = {"forum_questions": forum_questions,
               "forum_tags": forum_tags,
               "forum_questions_count": forum_questions_count,
               "forum_answers_count": forum_answers_count,
               "total_professionals_count": total_professionals_count,}

    return render(request, "forum/forum_home.html", context)

def forum_post(request, question_title, id):
    question = get_object_or_404(ForumQuestion, id=id)
    question.post_views += 1
    question.save()
    question_responses = ForumAnswer.objects.filter(question=question).order_by('time_responded')
    question_responses_count = question_responses.count()
    other_questions = ForumQuestion.objects.all().exclude(id=question.id).order_by('?')[:3]

    context = {
        "question": question,
        "question_responses": question_responses,
        "question_responses_count":question_responses_count,
        "other_questions":other_questions,
    }

    return render(request, "forum/forum_post.html", context)
