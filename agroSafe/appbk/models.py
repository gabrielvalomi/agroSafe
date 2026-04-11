from django.db import models

class Pessoa(models.Model):
	nome = models.CharField(max_length=100)
	cpf = models.CharField(max_length=14, unique=True)
	senha = models.CharField(max_length=128)

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

class CadastroVisitantePortaria(models.Model):
    nome = models.CharField(max_length=100)
    documento = models.CharField(max_length=64)
    foto = models.ImageField(upload_to='portaria/visitantes/%Y/%m/')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'documento'], name='uniq_portaria_nome_documento'),
        ]

    def __str__(self):
        return f"{self.nome} ({self.documento})"


class RegistroAcessoPortaria(models.Model):
    cadastro = models.ForeignKey(
        CadastroVisitantePortaria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_acesso',
    )
    nome_informado = models.CharField(max_length=100)
    documento_informado = models.CharField(max_length=64)
    fluxo = models.CharField(max_length=40)
    reconhecimento_correlacao = models.FloatField(null=True, blank=True)
    reconhecimento_automatico_ok = models.BooleanField(null=True, blank=True)
    review_manual_aprovado = models.BooleanField(null=True, blank=True)
    entrada_permitida = models.BooleanField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fluxo} permitida={self.entrada_permitida}"