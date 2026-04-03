from django.db import models

class Pessoa(models.Model):
	nome = models.CharField(max_length=100)
	cpf = models.CharField(max_length=14, unique=True)

	def __str__(self):
		return f"{self.nome} ({self.cpf})"


# Modelo para armazenar dados de visitantes
class Visitante(models.Model):
	nome = models.CharField(max_length=100)
	cpf = models.CharField(max_length=14)
	email = models.EmailField()
	horario_entrada = models.DateTimeField()
	horario_saida = models.DateTimeField()

	def __str__(self):
		return f"{self.nome} - {self.cpf}"
