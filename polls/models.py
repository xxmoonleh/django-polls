from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    nickname = models.CharField(max_length=100, unique=True)
    avatar = models.CharField(max_length=225, null=True)

class Questionario(models.Model):
    nome = models.CharField(max_length=45)
    descricao = models.CharField(max_length=500, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Hashtag(models.Model):
    tag = models.CharField(max_length=100)

class HashtagHasQuestionario(models.Model):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
