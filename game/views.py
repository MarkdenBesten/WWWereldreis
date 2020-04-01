import datetime

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Question, Answer, TeamProfile
from .forms import AnswerForm
from django.conf import settings


# Create your views here.
def index(request):
    """View function for home page of site"""
    return render(request, 'index.html')


def reisgids(request):
    """View function for 'reisgids'."""
    return render(request, 'reisgids.html')


def correctanswer(request):
    """View function for correct answer."""
    return render(request, 'game/correct_answer.html')


class QuestionsListView(LoginRequiredMixin, ListView):
    model = Question


class TeamListView(ListView):
    model = TeamProfile
    queryset = TeamProfile.objects.all().order_by('points', '-jokers')


@login_required()
def get_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user = request.user

    if settings.MIN_TIME > datetime.datetime.now().time():
        context ={
        'tijd': settings.MIN_TIME,
        }
        return render(request, 'game/too_early.html', context)

    if settings.MAX_TIME < datetime.datetime.now().time():
        context ={
        'tijd': settings.MIN_TIME,
        }
        return render(request, 'game/too_late.html', context)


    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnswerForm(request.POST)
        # check whether it's valid:
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
                if team.timeJoker.time() > (datetime.datetime.now() - datetime.timedelta(hours=2)).time():
                    # mag nog niet inleveren want jokertijd is nog niet om

                    context = {
                        'form': AnswerForm(),
                        'question': question,
                        'error': "Je moet 15 minuten wachten voordat je een joker kunt gebruiken, dit kan pas na: ",
                        'tijd': (team.timeJoker + datetime.timedelta(hours=2)).time()
                    }
                    return render(request, 'question_ask.html', context)
                else:
                    # Joker
                    answer.result = 'j'
                    answer.save()
                    team.jokers = team.jokers + 1
                    team.timeJoker = datetime.datetime.now() + datetime.timedelta(minutes=15)
                    team.save()
                    return HttpResponseRedirect('/joker/')
            else:
                if team.timeWrong.time() > (datetime.datetime.now() - datetime.timedelta(hours=2)).time():
                    # Mag nog niet inleveren want fout-tijd is nog niet om

                    context = {
                        'form': AnswerForm(),
                        'question': question,
                        'gebruiker': user,
                        'error': "Je moet 5 minuten nadat je een fout antwoord hebt gegeven, wacht tot na: ",
                        'tijd': (team.timeWrong + datetime.timedelta(hours=2)).time()
                    }
                    return render(request, 'question_ask.html', context)
                else:
                    answer.latitude = form.cleaned_data['latitude']
                    answer.longitude = form.cleaned_data['longitude']

                    def pointarea():
                        # latitude = y, longitude = x
                        # Add triangles ABP, BCP, CDP, DAP together to get area
                        def triangleArea(Ax, Ay, Bx, By, Cx, Cy):
                            triangle = (
                                               (Ax * (By - Cy)) +
                                               (Bx * (Cy - Ay)) +
                                               (Cx * (Ay - By))
                                       ) / 2
                            return abs(triangle)

                        poly = (
                            triangleArea(question.Alon, question.Alat, question.Blon, question.Blat, form.cleaned_data['longitude'], form.cleaned_data['latitude']) +
                            triangleArea(question.Blon, question.Blat, question.Clon, question.Clat, form.cleaned_data['longitude'], form.cleaned_data['latitude']) +
                            triangleArea(question.Clon, question.Clat, question.Dlon, question.Dlat, form.cleaned_data['longitude'], form.cleaned_data['latitude']) +
                            triangleArea(question.Dlon, question.Dlat, question.Alon, question.Alat, form.cleaned_data['longitude'], form.cleaned_data['latitude'])
                        )
                        return poly

                    if pointarea() > question.area + 0.00001:
                        # answer is wrong
                        # area cannot be smaller
                        answer.result = 'f'
                        answer.save()
                        team.timeWrong = datetime.datetime.now() + datetime.timedelta(minutes=5)
                        team.save()

                        context = {
                            'form': AnswerForm(),
                            'question': question,
                            'gebruiker': user,
                            'error': "Helaas! dat antwoord is fout. Probeer het opniew na  ",
                            'tijd': (team.timeWrong).time()
                        }
                        return render(request, 'question_ask.html', context)
                    elif pointarea() < question.area - 0.0001:
                        return HttpResponseRedirect('/rare-area-error/')
                    else:
                        # answer is right
                        answer.result = 'g'
                        answer.save()
                        team.points = team.points + 1
                        team.timeJoker = datetime.datetime.now() + datetime.timedelta(minutes=15)
                        team.save()
                        return HttpResponseRedirect('/game/questions/correct')
        else:
            return HttpResponseRedirect('/huh/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnswerForm()

        context = {
            'form': form,
            'question': question,
            'gebruiker': user
        }

        return render(request, 'question_ask.html', context)


class QuestionDetailAnswerView(PermissionRequiredMixin, DetailView):
    permission_required = 'game.can_view_answer'
    model = Question
    template_name = 'game/question_detail_answer.html'


class QuestionCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'game.can_edit'
    model = Question
    fields = ['nr', 'title', 'content', 'explanation', 'Alat', 'Alon', 'Blat', 'Blon', 'Clat', 'Clon', 'Dlat', 'Dlon']

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/game/questions/')


class QuestionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'game.can_edit'
    model = Question
    fields = ['nr', 'title', 'content', 'explanation', 'Alat', 'Alon', 'Blat', 'Blon', 'Clat', 'Clon', 'Dlat', 'Dlon']

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/game/questions/')


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('questions')
