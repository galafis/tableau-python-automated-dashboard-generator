# Tableau Dashboard Automation with Python

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)

---

## 🇧🇷 Automação de Dashboards Tableau com Python

Este repositório fornece um framework para automação de tarefas no Tableau Server utilizando Python. O foco é a criação, publicação e atualização de dashboards e fontes de dados de forma programática, integrando o Tableau a pipelines de dados automatizados.

### 🎯 Objetivo

O objetivo deste projeto é demonstrar como a API do Tableau Server (através da biblioteca `tableau-api-lib` ou `tableauserverclient`) pode ser usada para gerenciar o ciclo de vida de conteúdo no Tableau, eliminando tarefas manuais e repetitivas e permitindo a implementação de DataOps.

### 📂 Conteúdo do Repositório

*   **/src**: Scripts Python para automação.
    *   `tableau_automation`: Funções para interagir com a API do Tableau Server.
    *   `data_preparation`: Scripts para preparar os dados antes de publicá-los.
    *   `extract_generation`: Geração de arquivos de extração do Tableau (.hyper).
*   **/dashboards**: Arquivos de exemplo de dashboards do Tableau (.twb).
*   **/data**: Datasets de exemplo.
*   **/tests**: Testes para os scripts de automação.
*   **/docs**: Documentação sobre a configuração e uso do framework.

### ⚙️ Funcionalidades

*   **Publicação Automatizada**: Scripts para publicar workbooks e fontes de dados no Tableau Server.
*   **Atualização de Extrações**: Automação do processo de atualização de extrações de dados.
*   **Geração de Arquivos .hyper**: Criação de extrações de alta performance do Tableau a partir de fontes de dados como Pandas DataFrames.
*   **Integração com Pipelines**: Exemplos de como integrar a automação do Tableau em pipelines de ETL/ELT.

---

## 🇬🇧 Tableau Dashboard Automation with Python

This repository provides a framework for automating tasks on Tableau Server using Python. The focus is on programmatically creating, publishing, and updating dashboards and data sources, integrating Tableau into automated data pipelines.

### 🎯 Objective

The goal of this project is to demonstrate how the Tableau Server API (via the `tableau-api-lib` or `tableauserverclient` library) can be used to manage the content lifecycle in Tableau, eliminating manual and repetitive tasks and enabling the implementation of DataOps.

### 📂 Repository Content

*   **/src**: Python scripts for automation.
    *   `tableau_automation`: Functions to interact with the Tableau Server API.
    *   `data_preparation`: Scripts to prepare data before publishing.
    *   `extract_generation`: Generation of Tableau extract files (.hyper).
*   **/dashboards**: Example Tableau dashboard files (.twb).
*   **/data**: Example datasets.
*   **/tests**: Tests for the automation scripts.
*   **/docs**: Documentation on the configuration and use of the framework.

### ⚙️ Features

*   **Automated Publishing**: Scripts to publish workbooks and data sources to Tableau Server.
*   **Extract Refreshes**: Automation of the data extract refresh process.
*   **.hyper File Generation**: Creation of high-performance Tableau extracts from data sources like Pandas DataFrames.
*   **Pipeline Integration**: Examples of how to integrate Tableau automation into ETL/ELT pipelines.

