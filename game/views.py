import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Question, Answer, TeamProfile
from .forms import AnswerForm
from django.conf import settings

wrongDelta = datetime.timedelta(hours=0, minutes=5)
jokerDelta = datetime.timedelta(hours=0, minutes=15)
tzDelta = datetime.timedelta(hours=2)


# Create your views here.
def index(request):
    """View function for home page of site"""
    context = {
        'start': settings.MIN_TIME,
        'einde': settings.MAX_TIME,
    }
    return render(request, 'index.html', context)


def reisgids(request):
    """View function for 'reisgids'."""
    context = {
        'start': settings.MIN_TIME,
        'einde': settings.MAX_TIME,
    }
    return render(request, 'reisgids.html', context)


def correctanswer(request):
    """View function for correct answer."""
    return render(request, 'game/correct_answer.html')


def joker(request):
    """View function for handed in joker"""
    return render(request, 'game/joker.html')


class QuestionsListView(LoginRequiredMixin, ListView):
    model = Question


class TeamListView(ListView):
    model = TeamProfile
    queryset = TeamProfile.objects.all().order_by('-points', 'jokers', '-timeLastCorrect')
    template_name = 'game/tussenstand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['num_questions'] = Question.objects.count()
        if settings.MAX_TIME > datetime.datetime.now().time():
            # spel is afgelopen
            context['title'] = 'Tussenstand'
        else:
            context['title'] = 'Uitslag'
        return context


@login_required()
def question_page(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user = request.user

    # functions for when the time is up
    if settings.MIN_TIME > datetime.datetime.now().time():
        context = {
            'tijd': settings.MIN_TIME,
        }
        return render(request, 'game/too_early.html', context)

    if settings.MAX_TIME < datetime.datetime.now().time():
        context = {
            'tijd': settings.MIN_TIME,
        }
        return render(request, 'game/too_late.html', context)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnswerForm(request.POST)
        # check whether the form is valid:
        if form.is_valid():
            team = user.teamprofile
            answer = Answer()
            answer.question = question
            answer.time = datetime.datetime.now()
            answer.team = user.teamprofile
            # process the data in form.cleaned_data as required
            if team.current_question != question.nr:
                return HttpResponseRedirect('/game/questions/')
            if form.cleaned_data['Joker'] == 'Joker':
                if team.timeJoker > timezone.now():
                    # mag nog niet inleveren want jokertijd is nog niet om

                    context = {
                        'form': AnswerForm(),
                        'gebruiker': user,
                        'question': question,
                        'error': "Je moet 15 minuten wachten voordat je een joker kunt gebruiken, dit kan pas na: ",
                        'tijd': (team.timeJoker + tzDelta).time()
                    }
                    return render(request, 'question_ask.html', context)
                else:
                    # Zet Joker in
                    answer.result = 'j'
                    answer.save()
                    team.jokers = team.jokers + 1
                    team.timeJoker = datetime.datetime.now() + jokerDelta
                    team.save()
                    return HttpResponseRedirect('/game/questions/joker/')
            else:
                if team.timeWrong > timezone.now():
                    # Mag nog niet inleveren want fout-tijd is nog niet om

                    context = {
                        'form': AnswerForm(),
                        'question': question,
                        'gebruiker': user,
                        'error': "Je moet 5 minuten nadat je een fout antwoord hebt gegeven, wacht tot na: ",
                        'tijd': (team.timeWrong.time()),
                    }
                    return render(request, 'question_ask.html', context)
                else:
                    answer.latitude = form.cleaned_data['latitude']
                    answer.longitude = form.cleaned_data['longitude']

                    # Function for calculating the area in relation of the answer.
                    def point_area():
                        # latitude = y, longitude = x
                        # Add triangles ABP, BCP, CDP, DAP together to get area
                        def triangle_area(ax, ay, bx, by, cx, cy):
                            triangle = (
                                               (ax * (by - cy)) +
                                               (bx * (cy - ay)) +
                                               (cx * (ay - by))
                                       ) / 2
                            return abs(triangle)

                        poly = (
                            triangle_area(question.Alon, question.Alat, question.Blon, question.Blat,
                                          form.cleaned_data['longitude'], form.cleaned_data['latitude']) +
                            triangle_area(question.Blon, question.Blat, question.Clon, question.Clat,
                                          form.cleaned_data['longitude'], form.cleaned_data['latitude']) +
                            triangle_area(question.Clon, question.Clat, question.Dlon, question.Dlat,
                                          form.cleaned_data['longitude'], form.cleaned_data['latitude']) +
                            triangle_area(question.Dlon, question.Dlat, question.Alon, question.Alat,
                                          form.cleaned_data['longitude'], form.cleaned_data['latitude'])
                        )
                        return poly

                    # Checking the answer.
                    if point_area() > question.area + 0.000001:
                        # answer is wrong
                        # area cannot be smaller
                        answer.result = 'f'
                        answer.save()
                        team.timeWrong = timezone.now() + wrongDelta
                        team.save()

                        context = {
                            'question': question,
                            'gebruiker': user,
                            'tijd': (team.timeWrong + tzDelta).time()
                        }
                        return render(request, 'game/wrong_answer.html', context)

                    elif point_area() < question.area - 0.0001:
                        # Dit hoort niet te kunnen
                        return HttpResponseRedirect('/rare-area-error/')
                    else:
                        # answer is correct
                        answer.result = 'g'
                        answer.save()
                        team.points = team.points + 1
                        team.timeJoker = timezone.now() + jokerDelta
                        team.timeLastCorrect = timezone.now()
                        team.save()
                        return HttpResponseRedirect('/game/questions/correct')
        else:
            return HttpResponseRedirect('/huh/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnswerForm()
        num_questions = Question.objects.count()

        context = {
            'form': form,
            'question': question,
            'gebruiker': user,
            'num_questions': num_questions,
        }

        return render(request, 'question_ask.html', context)


@permission_required('game.can_view_answer')
def answer_page(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user = request.user
    team = user.teamprofile

    answers = Answer.objects.filter(question=question, team=team).exclude(result='j')
    list_of_answers = []
    for answer in answers:
        time = str(answer.time.time())[0:5]
        answer_list = [time, answer.latitude, answer.longitude]
        list_of_answers.append(answer_list)

    num_questions = Question.objects.count()
    context = {
        'question': question,
        'answers': list_of_answers,
        'num_questions': num_questions,
    }
    return render(request, 'game/answer_page.html', context)


class QuestionCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'game.can_edit'
    model = Question
    fields = [
        'nr',
        'title',
        'content',
        'fileUrl',
        'explanation',
        'Alat', 'Alon', 'Blat', 'Blon', 'Clat', 'Clon', 'Dlat', 'Dlon'
    ]

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/game/questions/')


class QuestionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'game.can_edit'
    model = Question
    fields = [
        'nr',
        'title',
        'content',
        'fileUrl',
        'explanation',
        'Alat', 'Alon', 'Blat', 'Blon', 'Clat', 'Clon', 'Dlat', 'Dlon'
    ]

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/game/questions/')


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('question-list')
