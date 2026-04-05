
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pessoa, Visitante
from django.contrib.auth.hashers import make_password
import json
from django.utils import timezone
from datetime import timedelta

# cadastro da empresa, apenas para fins de teste.
@csrf_exempt
def cadastrar_pessoa(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			nome = data.get('nome')
			cpf = data.get('cpf')
			senha = data.get('senha')
			if not nome or not cpf or not senha:
				return JsonResponse({'erro': 'Nome, CPF e senha são obrigatórios.'}, status=400)
			if Pessoa.objects.filter(cpf=cpf).exists():
				return JsonResponse({'erro': 'CPF já cadastrado.'}, status=400)
			senha_hash = make_password(senha)

			pessoa = Pessoa.objects.create(
				nome=nome,
				cpf=cpf,
				senha=senha_hash
			)
			return JsonResponse({'mensagem': 'Usuário cadastrado com sucesso!', 'id': pessoa.id, 'nome': pessoa.nome, 'cpf': pessoa.cpf}, status=201)
		except Exception as e:
			return JsonResponse({'erro': str(e)}, status=400)
	return JsonResponse({'erro': 'Método não permitido.'}, status=405)

#Cadastro de visitantes
@csrf_exempt
def cadastrar_visitante(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			nome = data.get('nome')
			cpf = data.get('cpf')
			email = data.get('email')
			horario_entrada = data.get('horario_entrada')
			horario_saida = data.get('horario_saida')
			if not nome or not cpf or not email or not horario_entrada or not horario_saida:
				return JsonResponse({'erro': 'Todos os campos são obrigatórios.'}, status=400)
			visitante = Visitante.objects.create(
				nome=nome,
				cpf=cpf,
				email=email,
				horario_entrada=horario_entrada,
				horario_saida=horario_saida
			)
			return JsonResponse({'mensagem': 'Visitante cadastrado com sucesso!', 'id': visitante.id}, status=201)
		except (TypeError, ValueError) as e:
			return JsonResponse({'erro': str(e)}, status=400)
	return JsonResponse({'erro': 'Método não permitido.'}, status=405)

# Verifica se o visitante está autorizado a entrar (48h desde a última visita)
@csrf_exempt
def verificar_autorizacao_visitante(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			cpf = data.get('cpf')
			if not cpf:
				return JsonResponse({'erro': 'CPF é obrigatório.'}, status=400)
			# Busca a última visita desse CPF
			ultima_visita = Visitante.objects.filter(cpf=cpf).order_by('-horario_saida').first()
			if not ultima_visita:
				return JsonResponse({'autorizado': True, 'mensagem': 'Primeira visita, entrada autorizada.'})
			agora = timezone.now()
			diff = agora - ultima_visita.horario_saida
			if diff >= timedelta(hours=48):
				return JsonResponse({'autorizado': True, 'mensagem': 'Entrada autorizada.'})
			else:
				horas_restantes = 48 - (diff.total_seconds() // 3600)
				return JsonResponse({'autorizado': False, 'mensagem': f'Entrada não autorizada. Faltam {int(horas_restantes)} horas para nova entrada.'})
		except Exception as e:
			return JsonResponse({'erro': str(e)}, status=400)
	return JsonResponse({'erro': 'Método não permitido.'}, status=405)


# Lista nomes e CPFs das últimas 10 visitas
@csrf_exempt
def listar_ultimas_visitas(request):
	if request.method == 'GET':
		visitas = Visitante.objects.order_by('-horario_saida')[:10]
		dados = [
			{'nome': v.nome, 'cpf': v.cpf, 'horario_saida': v.horario_saida}
			for v in visitas
		]
		return JsonResponse({'ultimas_visitas': dados}, status=200)
	return JsonResponse({'erro': 'Método não permitido.'}, status=405)



