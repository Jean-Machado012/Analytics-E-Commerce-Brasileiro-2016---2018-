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

### Status

- Em desenvolvimento