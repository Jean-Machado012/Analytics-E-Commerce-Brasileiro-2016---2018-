# Olist E-Commerce Brasil (2016 - 2018)

## Objetivo do projeto

Criar uma pipeline de dados utilizando Python e SQL, desde a extração e ingestão dos dados até a construção da camada analítica no Power BI utilizando DAX.

O dataset utilizado contém aproximadamente 100 mil pedidos distribuídos em 9 arquivos CSV, que representam diferentes entidades do e-commerce.

A primeira etapa consiste em realizar a extração e análise inicial dos arquivos utilizando Python e Pandas, verificando a qualidade e a estrutura dos dados.

Posteriormente, os dados serão carregados em um SGBD MySQL, onde serão realizadas as etapas de tratamento e transformação utilizando SQL.

Após o tratamento, os dados serão disponibilizados para o Power BI, onde será construída a camada analítica e os indicadores utilizando DAX.

Além dos dados disponibilizados pelo dataset, será utilizada uma API pública para enriquecer a análise e integrar uma fonte externa aos dados do e-commerce.

## Tecnologias

- Python
- Pandas
- SQL
- MySQL
- Power BI
- DAX
- API REST
- Git/GitHub

## 1ª Etapa — Extração e análise inicial dos dados

- Download do dataset Olist através do Kaggle.
- Identificação dos 9 arquivos CSV que compõem o dataset.
- Leitura dos arquivos utilizando Python e Pandas.
- Identificação da quantidade de linhas e colunas de cada arquivo.
- Verificação de linhas completamente vazias.
- Verificação de colunas completamente vazias.
- Identificação de registros duplicados.
- Análise da quantidade de valores únicos.
- Análise inicial dos tipos de dados.
- Conversão das colunas de data que estavam como "string" para o tipo "datetime".


## 2ª Etapa — Requisição à API ViaCEP

- Implementei o consumo da API ViaCEP utilizando Python e estruturei o processo de consulta dentro de uma função, permitindo que o código
  seja reutilizado e escalado para os diferentes prefixos de CEP presentes na base.
  

- Durante a implementação, identifiquei uma limitação relacionada ao volume de requisições. A documentação da ViaCEP informa que o uso
  massivo da API pode ocasionar bloqueio automático, porém não define uma quantidade específica de requisições que resulte nesse bloqueio.
  
- Como estratégia para tornar o processo mais resiliente, pretendo realizar as consultas em lotes, persistir os resultados e controlar
  quais prefixos já foram processados. Dessa forma, caso o processo seja interrompido ou o acesso seja temporariamente bloqueado, será
  possível retomar a execução a partir do último conjunto de dados processado, evitando novas requisições para os prefixos já tratados.
  
- Como lógica, primeiramente li o arquivo que possui os prefixos, realizei a limpeza das linhas em branco e eliminei os prefixos duplicados.
  Feito isso, como não vou utilizar todos os dados que a API fornce pensei em armazenar as informações que eu quero em um dicionário, e depois
  esse dicionário ele vai ser colocado dentro de uma lista

- Rrealizei a integração com a API ViaCEP para enriquecimento dos dados de localização presentes no dataset, como a base possui apenas o prefixo do CEP, foi utilizado o sufixo `000` para formar um CEP completo e realizar as consultas à API. Durante os testes, foi identificado que, após um determinado volume de requisições, a API passou a apresentar erros de conexão e indisponibilidade temporária. A documentação da ViaCEP não estabelece uma quantidade máxima de requisições por período que pudesse ser utilizada como referência.

- Diante disso, defini um limite de 400 requisições por execução. Esse valor não representa um limite oficial da ViaCEP, mas uma definição adotada para o projeto a partir dos testes realizados e considerada mais segura para evitar um volume excessivo de requisições, para garantir que nenhuma informação seja perdida durante o processo, a pipeline foi estruturada para armazenar o resultado de cada tentativa, independentemente de a consulta retornar dados, não encontrar o CEP ou apresentar algum erro.

Também foram criados dois arquivos JSON para garantir a persistência e a retomada do processo:
- **`enderecos.json`** — armazena os resultados das consultas realizadas à API, incluindo os dados encontrados e as ocorrências em que não foi possível obter informações.
- **`checkpoint.json`** — armazena o estado da execução, incluindo a posição do último prefixo consultado, a quantidade de requisições realizadas e o status da pipeline.

Dessa forma, caso a execução seja interrompida, o processo pode ser retomado posteriormente a partir da última posição registrada, sem a necessidade de realizar novamente as consultas já processadas.

## 3º Etapa - Implementando orquestração do pipeline com o Prefect

Nesta etapa, comecei a estruturar a orquestração das consultas à API ViaCEP utilizando o Prefect. O objetivo é organizar o fluxo de execução, separar as responsabilidades do código e facilitar a continuidade do processamento caso ocorram interrupções.

- Separação das responsabilidades: adaptei a função solicitar_api() para receber um prefixo por chamada e retornar um dicionário com os dados obtidos e o status da consulta. Com isso, a consulta individual ficou separada da lógica responsável por controlar o processamento em lotes.

- Criação das tasks: comecei a dividir o processo em tarefas com o Prefect, incluindo o carregamento da lista de prefixos, a consulta à API, a leitura do checkpoint e o carregamento dos endereços já armazenados.

- Retomada do processamento: implementei a lógica para ler o checkpoint.json e identificar a posição inicial da próxima execução, evitando que o fluxo comece novamente do primeiro prefixo quando já existe um progresso registrado.

- Seleção dos lotes: estruturei a seleção dos prefixos com base na posição inicial e no limite operacional de 400 requisições por execução. Esse limite foi definido para o projeto e não representa um limite oficial da API ViaCEP.

- Preparação da persistência: criei tasks específicas para salvar os resultados em `enderecos.json` e atualizar o `checkpoint.json`. A integração dessas tarefas ao processamento ainda será concluída e validada nas próximas etapas.

- Verifiquei a importação da função de consulta entre os arquivos extracao.py e orquestracao.py, desativando o bloco antigo que executava o processamento automaticamente durante a importação.

- Validei a seleção do lote a partir do checkpoint e a identificação do primeiro e do último prefixo planejados.

- Testei o percurso dos itens selecionados, preservando o índice original de cada prefixo para utilizá-lo posteriormente na atualização do checkpoint. Verifiquei o retorno da tarefa de consulta, incluindo o tratamento de erros de conexão.

- Integrei a consulta à API ao processamento completo dos lotes e adicionado cada resultado à lista de endereços e validar sua gravação no JSON.

- Atualização do checkpoint ao fluxo, registrando o progresso após cada consulta.

- Testar a retomada do processamento e o comportamento da pipeline diante de falhas.

- Validada a execução de lotes completos antes de avançar para as próximas etapas de tratamento.


### Próximas etapas

- Implementar a conexão do pipeline Python com o banco de dados MySQL.

- Realizar a carga inicial das tabelas CSV do dataset Olist no banco de dados.

- Implementar a inserção dos dados de endereços obtidos pela API ViaCEP, utilizando processamento em lotes.

- Validar a integridade dos dados carregados e a consistência entre as tabelas.

- Desenvolver consultas SQL para relacionar as tabelas e preparar os dados para análise.


### Status

- Em desenvolvimento