import json, os
from pathlib import Path
from prefect import flow, task
from extracao import solicitar_api
from prefect.client.schemas.schedules import CronSchedule

base_dir = Path(__file__).resolve().parent
caminho_prefixo = base_dir / 'prefixos.json'
caminho_enderecos = base_dir / 'Enderecos' / 'enderecos.json'
caminho_checkpoint = base_dir / 'Enderecos' / 'checkpoint.json'

limite_requisicoes = 400



def salva_temp_json(caminho, dados):
    # Criando a pasta caso não exista, e se caso existir prossegue normalmente
    caminho.parents.mkdir(parents = True, exist_ok = True)
    # Criando arquivo temporário
    caminho_temporario = caminho.with_suffix(caminho.suffix + '.tmp')

    # Abrindo arquivo temporário e salvando as informações nele
    with open(caminho_temporario, 'w', encoding = 'utf-8') as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii = False,
            indent = 4
        )

    # Substituindo dados do arquivo temporário e adcionando no arquivo original
    os.replace(caminho_temporario, caminho)


# Esta lendo a lista dentro do json para os prefixos
@task
def task_carregar_prefixos():
    with open(caminho_prefixo, 'r', encoding = 'utf-8') as arquivo:
        lista_prefixos = json.load(arquivo)

    return lista_prefixos

@task
def task_consultar_prefixo(prefixo):
    return solicitar_api(prefixo)

@task
def task_checkpoint():
    if not caminho_checkpoint.exists():
        return None

    with open(caminho_checkpoint, 'r', encoding = 'utf-8') as arquivo:
        checkpoint = json.load(arquivo)

    return checkpoint

@task
def task_inicio_checkpoint(checkpoint):
    if checkpoint is None:
        return 0

    return checkpoint['posicao'] + 1

@task
def task_enderecos():
    if not caminho_enderecos.exists():
        return []

    with open(caminho_enderecos, 'r', encoding = 'utf-8') as arquivo:
        enderecos = json.load(arquivo)

    return enderecos

@task
def task_salva_enderecos(enderecos):
    with open(caminho_enderecos, 'w', encoding = 'utf-8') as arquivo:
        json.dump(
            enderecos,
            arquivo,
            ensure_ascii = False,
            indent = 4
        )

@task
def task_salva_checkpoint(checkpoint):
    with open(caminho_checkpoint, 'w', encoding = 'utf-8') as arquivo:
        json.dump(
            checkpoint,
            arquivo,
            ensure_ascii = False,
            indent = 4
        )

@flow
def pipeline_cep():
    lista_prefixos = task_carregar_prefixos()
    checkpoint = task_checkpoint()

    inicio = task_inicio_checkpoint(checkpoint)
    fim = min(inicio + limite_requisicoes, len(lista_prefixos))

    enderecos = task_enderecos()

    cont_rq = (
        checkpoint['requisicoes_realizadas']
        if checkpoint is not None
        else 0
    )

    # Aqui será realizado o processamento dos prefixos e a atualização do checkpoint

    lote_requisicoes = lista_prefixos[inicio : fim]


    print(f'Total de prefixos: {len(lista_prefixos)}')
    print(f'Índice inicial planejado: {inicio}')
    print(f'Índice final planejado: {fim - 1}')
    print(f'Qtd de endereços armazenados: {len(enderecos)}')
    print(f'Prefixos selecionados para requisição: {len(lote_requisicoes)}')

    if inicio < fim:
        print(f"Primeiro prefixo: {lista_prefixos[inicio]['prefixo']}")
        print(f"Último prefixo: {lista_prefixos[fim - 1]['prefixo']}")

    for i in lote_requisicoes:
        prefixo = i['prefixo']
        posicao = i['indice']

        print(f'Prefixo planejado para consulta: {prefixo}')
        print(f'Posição na lista: {posicao}')

        resultado = task_consultar_prefixo(prefixo)

        enderecos.append(resultado)
        print(f'Total de endereços em memória: {len(enderecos)}')

        task_salva_enderecos(enderecos)

        checkpoint = {
            'ultimo_prefixo': prefixo,
            'posicao' : posicao,
            'requisicoes_realizadas' : cont_rq + 1,
            'status' : 'em_andamento'
        }

        task_salva_checkpoint(checkpoint)
        cont_rq += 1

        print(f'Resultado da consulta: {resultado}')

        

if __name__ == '__main__':
    pipeline_cep.serve(
        name = 'agendamento-viacep',
        schedule = CronSchedule(
            cron = '0 9 * * *',
            timezone = 'America/Sao_Paulo'
        ),
        pause_on_shutdown = False
    )
