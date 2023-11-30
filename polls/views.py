from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.core.exceptions import ValidationError
from .models import Question, Choice

from django.contrib.auth import get_user_model
User = get_user_model()


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = f"Resultados da pergunta de número {question_id}."
    return HttpResponse(response % question_id)


from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView 
from django.urls import reverse_lazy
from django.forms.models import BaseModelForm
from django.contrib import messages

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ('question_text', 'pub_date', )
    success_url =  reverse_lazy('question-list')
    template_name = 'polls/question_form.html'
    success_message = 'Pergunta criada com sucesso!'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, self.success_message)
        return super(QuestionCreateView, self).form_valid(form)

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'

class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        votes = Choice.objects.filter(question=context['question']).aggregate(total=Sum('votes')) or 0
        context['total_votes'] = votes.get('total')

        return context

from django.contrib import messages

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('question-list')
    success_message = 'Enquete excluída com sucesso.'

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'polls/question_form.html'
    fields = ('question_text', 'pub_date', )
    success_url = reverse_lazy('question-list')
    success_message = 'Pergunta atualizada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando a pergunta'

        question_id = self.kwargs.get('pk')
        choices = Choice.objects.filter(question__pk=question_id)
        context['question_choices'] = choices

        return context

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(QuestionUpdateView, self).form_valid(request, *args, **kwargs)

    #cadastro de opção de voto

class ChoiceCreateView(CreateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text', )
    success_message = 'Pergunta criada com sucesso!'

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        return super(ChoiceCreateView, self).dispatch(request,  *args, **kwargs)

    def get_context_data(self, **kwargs):
        # question = get_object_or_404(Question,  pk=self.kwargs.get('pk'))
        context = super(ChoiceCreateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Alternativa para:{self.question.question_text}'

        return context

    def form_valid(self, form):
        form.instance.question = self.question
        messages.success(self.request, self.success_message)
        return super(ChoiceCreateView, self).form_valid(form)
    
    def get_success_url(self, *args, **kwargs):
        question_id = self.kwargs.get('pk')
        return reverse_lazy('question-update', kwargs={'pk': question_id})

class ChoiceUpdateView(UpdateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text', )
    success_message = 'Alternativa atualizada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super(ChoiceUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando a alternativa...'

        return context

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChoiceUpdateView, self).form_valid(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('question-update', kwargs={'pk': question_id})

class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Choice
    template_name = 'polls/choice_confirm_delete.html'
    success_message = 'Alternativa excluída com sucesso!'

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChoiceDeleteView, self).form_valid(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        print(question_id)
        return reverse_lazy('question-update', kwargs={'pk': question_id})


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
            selected_choice.votes += 1
            session_user = get_object_or_404(User, id=request.user.id)
            selected_choice.save(user=session_user)
    
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, 'Selecione uma alternativa para votar')
        
        except (ValidationError) as error:
            messages.error(request, error.message)

        else:
            messages.success(request, 'Seu voto foi registrado com sucesso')
            return redirect(reverse_lazy("poll_results", args=(question.id,)))

    context = {'question': question}
    return render(request, 'polls/question_detail.html', context)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    votes = Choice.objects.filter(question=question).aggregate(total=Sum('votes')) or 0
    total_votes = votes.get('total')
    context = {"question": question}

    context['votes'] = []
    for choice in question.choice_set.all():
        percentage = 0
        if choice.votes > 0 and total_votes > 0:
            percentage = choice.votes / total_votes * 100

        context['votes'].append(
            {
                'text': choice.choice_text,
                'votes': choice.votes,
                'percentage': round(percentage, 2)
            }
        )

    return render(request, "polls/results.html", context)
    