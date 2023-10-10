from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question


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


def vote(request, question_id):
    return HttpResponse (f"Você vai votar na pergunta de número {question_id}.")

from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

class QuestionCreateView(CreateView):
    model = Question
    fields = ('question_text',)
    success_url =  reverse_lazy('question-list')
    template_name = 'polls/question_form.html'

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'

class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'

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
    success_url = reverse_lazy('question-list')
    fields = ('question_text',)
    success_message = 'Enquete atualizada com sucesso!'
    
    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando a pergunta'
        
        question_id = self.kwargs.get('pk')
        choices = Choice.objects.filter(question_pk=question_id)
        context['question_choices'] = choices
        
        return context
    
    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(QuestionUpdateView, self).form_valid(request, *args, **kwargs)
    
class ChoiceCreateView(CreateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text', )
    success_message = 'Alternativa registrada com sucesso!'
    
    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        return super(ChoiceCreateView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        
        context = super(ChoiceCreateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Alternativa para: {question.question_text}'
        
        return context
    
    def form_valid(self, form):
        form.instance.question = self.question
        messages.success(self.request, self.success_message)
        return super(ChoiceCreateView, self).form_valid(form)
    
    def get_success_url(self, *args, **kwargs):
        qustion_id = self.kwargs.get('pk')
        return reverse_lazy('poll_edit', kwargs={'pk': question_id})
    
class ChoiceUpdateView(UpdateView):
    model = Choice
    template_name = 'polls/choice_form.html'
    fields = ('choice_text', )
    success_message = 'Alternativa atualizada com sucesso!'
    
    def get_context_data(self, **kwargs):
        context = super(ChoiceUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Editando alternativa'
        
        return context
    
    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChoiceUpdateView, self).form_valid(request, *args, **kwargs)
    
    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('poll_edit', kwargs={'pk': question_id})
    
class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Choice
    template_name = 'polls/choice_confirm_delete.html'
    success_message = 'Alternativa excluída com sucesso!'
    
    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChoiceDeleteView, self).form_valid(request, *args, **kwargs)
    
    def get_success_url(self, *args, **kwargs):
        question_id = self.object.question.id
        return reverse_lazy('poll_edit', kwargs={'pk': question_id})