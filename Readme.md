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

### Próxima etapa

Implementar um mecanismo de **orquestração da pipeline**, permitindo que o processo seja executado novamente de forma controlada até que todos os **19.015 prefixos únicos de CEP** sejam processados, utilizando o `checkpoint.json` para determinar automaticamente o ponto de retomada.


### Status

- Em desenvolvimento