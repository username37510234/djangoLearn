from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import F

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request=request, template_name='index.html', context=context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 에러 메세지와 함께 폼을 다시 디스플레이합니다.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # F() 는 데이터베이스의 원자적 연산을 지원한다
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # POST 데이터 처리를 정상적으로 마친 뒤에는 항상 HttpResponseRedirect를 리턴합니다.        
        # 이 방법을 통해 유저가 브라우저의 "뒤로가기"을 눌렀을 때
        # 데이터가 두 번 저장되는 것을 방지할 수 있습니다.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))