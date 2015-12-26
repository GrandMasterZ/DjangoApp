from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Question, Choice
from django.template import RequestContext, loader
from django.utils import timezone
from django.db.models import F

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'main/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.views = question.views +1
    question.save
    return render(request, 'main/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'main/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'main/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('main:results', args=(question.id,)))

def add_question(request):
    return render(request, 'main/add_question.html')

def addingQuestion(request):
    if request.method == 'POST':
        question = request.POST.get('text')
        date = timezone.now()
        u = Question(question_text=question,pub_date=date)
        u.save()
        for x in range (1,7):
            string = str(x)
            choice = request.POST.get(string)
            if(choice!=""):
                new = Choice(question=u,choice_text=choice)
                new.save()
    return HttpResponseRedirect(reverse('main:index'))