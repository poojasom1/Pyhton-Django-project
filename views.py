# Create your views here.
from secrets import choice
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Choice, Question
from django.shortcuts import get_object_or_404
from django.urls import reverse

def index(request):
    questions = Question.objects.order_by('-pub_date')[:5]
    context = {'questions': questions}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        return render(request, 'polls/details.html' , {'question':question})
    except Question.DoesNotExist:
        return render(request, 'polls/details.html',{'message':"Data Not Found"})



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    #return HttpResponse("You're voting on question %s." %question_id)