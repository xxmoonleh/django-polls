from django.urls import path
from polls import views

urlpatterns = [

#     function based views

#     ex: 127.0.0.1:8000/polls/
#     path("", views.index, name="index"),

#   ex: 127.0.0.1:8000/polls/5/
 #path("<int:question_id>/", views.detail, name="detail"),

#  ex: 127.0.0.1:8000/polls/5/results/
#     path("<int:question_id>/results/", views.results, name="results"),

#  ex: 127.0.0.1:8000/polls/5/vote/
#     path("<int:question_id>/vote/", views.vote, name="vote"),

    #class based views
    # ex: localhost:8000/enquetes/listar
    path('listar', views.QuestionListView.as_view(), name="question-list"),
# página de cadastro de nova enquete
    path('cadastrar', views.QuestionCreateView.as_view(), name="question-create"),
    path('<int:pk>', views.QuestionDetailView.as_view(), name="question-detail"),
    path('<int:pk>/deletar', views.QuestionDeleteView.as_view(), name="question-delete"),
    path('<int:pk>/atualizar', views.QuestionUpdateView.as_view(), name="question-update"),
    path('pergunta/<int:pk>/alternativa/add', views.ChoiceCreateView.as_view(), name="choice_create"),
    path('alternativa/<int:pk>/delete', views.ChoiceDeleteView.as_view(), name="choice_delete"),
    path('alternativa/<int:pk>/edit', views.ChoiceUpdateView.as_view(), name="choice_add"),
    path('pergunta/<int:question_id>/vote', views.vote, name="poll_vote"),
    path('pergunta/<int:question_id>/results', views.results, name="poll_results"),
]
