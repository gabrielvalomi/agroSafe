
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pessoa
import json

@csrf_exempt
def cadastrar_pessoa(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			nome = data.get('nome')
			cpf = data.get('cpf')
			if not nome or not cpf:
				return JsonResponse({'erro': 'Nome e CPF são obrigatórios.'}, status=400)
			if Pessoa.objects.filter(cpf=cpf).exists():
				return JsonResponse({'erro': 'CPF já cadastrado.'}, status=400)
			pessoa = Pessoa.objects.create(nome=nome, cpf=cpf)
			return JsonResponse({'id': pessoa.id, 'nome': pessoa.nome, 'cpf': pessoa.cpf}, status=201)
		except Exception as e:
			return JsonResponse({'erro': str(e)}, status=400)
	return JsonResponse({'erro': 'Método não permitido.'}, status=405)

# Create your views here.
