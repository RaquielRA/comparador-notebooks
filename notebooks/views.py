from django.shortcuts import render, redirect
from .services import LaptopService
from .models import Comentario
from asgiref.sync import sync_to_async
from django.db.models import Avg

async def lista_notebooks(request):
    """
    View principal do TechHub: Gerencia filtros de hardware, 
    cálculo de médias e lógica de exibição condicional.
    """

    # 1. Captura de Parâmetros da URL
    filtros = {
        'nome': request.GET.get('nome', '').strip(),
        'p_min': request.GET.get('p_min', '0'),
        'p_max': request.GET.get('p_max', '20000'),
        'ram': request.GET.get('ram', ''),
        'ssd': request.GET.get('ssd', ''),
        'cpu': request.GET.get('cpu', ''),
        'gpu': request.GET.get('gpu', ''),
        'min_estrelas': request.GET.get('min_estrelas', ''), # Novo filtro TechHub
    }

    if request.method == "POST":
        notebook_id = request.POST.get('notebook_id')
        # O nome dentro do get() DEVE ser igual ao 'name' do textarea no HTML
        texto_comentario = request.POST.get('comentario', '').strip() 
        estrelas = request.POST.get('estrelas')

        # Log para você ver no terminal (prompt de comando)
        print(f"DEBUG: Recebido ID={notebook_id}, Estrelas={estrelas}, Texto={texto_comentario}")

        if texto_comentario and notebook_id and estrelas:
            await sync_to_async(Comentario.objects.create)(
                notebook_id=notebook_id,
                texto=texto_comentario,  # Certifique-se que seu Model tem o campo 'texto'
                estrelas=int(estrelas),
                usuario_nome="Usuário TechHub"
            )
        return redirect(request.get_full_path())

    try:
        produtos_brutos = await LaptopService.buscar_notebooks(
            query=filtros['nome'],
            p_min=filtros['p_min'],
            p_max=filtros['p_max'],
            ram=filtros['ram'],
            ssd=filtros['ssd'],
            cpu=filtros['cpu'],
            gpu=filtros['gpu']
        )

        produtos_finais = []

        # 4. Cruzamento com Banco de Dados e Lógica de Estrelas
        for p in produtos_brutos:
            
            # Função síncrona para agregar dados do SQLite
            def obter_dados_avaliacao(nid):
                queryset = Comentario.objects.filter(notebook_id=nid).order_by('-data_criacao')
                media = queryset.aggregate(Avg('estrelas'))['estrelas__avg']
                return list(queryset), round(float(media), 1) if media else None

            comentarios, media_calculada = await sync_to_async(obter_dados_avaliacao)(p['id'])
            
            p['comentarios_salvos'] = comentarios
            p['total_comentarios'] = len(comentarios)
            p['media_estrelas'] = media_calculada # Pode ser None se não houver notas

            # 5. REGRA DE FILTRAGEM TECHHUB:
            # Se não houver filtro de estrelas, todos passam.
            # Se houver filtro: 
            #    - Notebooks SEM avaliação (None) SEMPRE passam.
            #    - Notebooks COM avaliação só passam se media >= filtro.
            passou_filtro_estrelas = True
            if filtros['min_estrelas'] and p['media_estrelas'] is not None:
                if p['media_estrelas'] < float(filtros['min_estrelas']):
                    passou_filtro_estrelas = False

            if passou_filtro_estrelas:
                produtos_finais.append(p)

    except Exception as e:
        print(f"--- ERRO TECHHUB VIEW ---: {e}")
        produtos_finais = []

    # 6. Contexto Final
    context = {
        'produtos': produtos_finais,
        'filtros': filtros,
        'total_encontrados': len(produtos_finais),
        'mensagem_vazio': "Nenhum notebook encontrado para os critérios do TechHub."
    }

    return render(request, 'notebooks/index.html', context)

