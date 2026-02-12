# Tableau Dashboard Automation with Python

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Automation](https://img.shields.io/badge/Automation-00C853?style=for-the-badge)

---

## 🇧🇷 Automação de Dashboards Tableau com Python

Este repositório fornece um framework para automação de tarefas no **Tableau Server** utilizando Python. A solução permite criar, publicar, atualizar e gerenciar dashboards e fontes de dados de forma programática, integrando o Tableau em pipelines de **DataOps** e **Analytics Engineering**.

### 🎯 Objetivo

Demonstrar como a **Tableau Server REST API** pode ser usada para reduzir tarefas manuais repetitivas, permitindo que equipes de dados implementem workflows automatizados e versionamento de dashboards.

### 🌟 Por que Automatizar o Tableau?

A automação do Tableau traz benefícios significativos para equipes de dados:

| Benefício | Impacto |
|-----------|---------|
| **Economia de Tempo** | Reduz tempo gasto em tarefas manuais de publicação |
| **Consistência** | Diminui erros humanos em publicações |
| **Escalabilidade** | Gerencia múltiplos dashboards simultaneamente |
| **Versionamento** | Controle de versão via Git para dashboards |
| **Monitoramento** | Alertas automáticos para falhas de refresh |

### 📊 Casos de Uso Reais

1. **BI Automation**: Publicar dashboards de forma programática em horários definidos
2. **Data Refresh**: Atualizar extracts após conclusão de pipelines ETL
3. **Multi-Environment**: Promover dashboards de DEV → QA → PROD
4. **Backup & Recovery**: Fazer backup de workbooks
5. **Bulk Operations**: Atualizar permissões de múltiplos dashboards de uma vez

### 🏗️ Arquitetura do Framework

```
┌──────────────┐
│ Data Sources │ (SQL, CSV, APIs)
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Python ETL Pipeline  │
│  - Extract data      │
│  - Transform data    │
│  - Generate .hyper   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Tableau Automation Framework │
│  - Authenticate              │
│  - Publish workbooks         │
│  - Refresh extracts          │
│  - Manage permissions        │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────┐
│ Tableau Server   │
│  - Dashboards    │
│  - Data Sources  │
└──────────────────┘
```

### 📂 Estrutura do Repositório

```
tableau-python-automated-dashboard-generator/
├── src/
│   └── tableau_automation/
│       └── tableau_publisher.py       # Framework principal
├── examples/
│   ├── publish_workbook.py           # Exemplo de publicação
│   ├── refresh_extract.py            # Exemplo de refresh
│   ├── etl_pipeline.py              # Pipeline ETL completo
│   └── bulk_operations.py            # Operações em lote
├── tests/
│   └── test_tableau_publisher.py     # Testes unitários
├── config/
│   └── tableau_config.example.yaml   # Template de configuração
├── requirements.txt                  # Dependências Python
└── README.md
```

### 🚀 Instalação e Configuração

#### 1. Instalar Dependências

```bash
# Clone o repositório
git clone https://github.com/galafis/tableau-python-automated-dashboard-generator.git
cd tableau-python-automated-dashboard-generator

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

#### 2. Configurar Credenciais do Tableau Server

```python
# config/tableau_config.yaml
server:
  url: "https://tableau.yourcompany.com"
  site_id: "your-site"
  api_version: "3.19"

credentials:
  username: "your-username"
  password: "your-password"  # Ou use Personal Access Token
  # token_name: "your-token-name"
  # token_value: "your-token-value"

projects:
  dev: "Development"
  qa: "Quality Assurance"
  prod: "Production"
```

#### 3. Executar Exemplo Básico

```bash
# Publicar um workbook
python examples/publish_workbook.py

# Atualizar um extract
python examples/refresh_extract.py
```

### 💻 Código Principal: TableauPublisher

O módulo principal está em `src/tableau_automation/tableau_publisher.py`. Abaixo, um resumo da API:

```python
from tableau_automation import TableauPublisher

# Inicializar
publisher = TableauPublisher(
    server_url="https://tableau.example.com",
    username="admin",
    password="password",
    site_id="analytics"
)

# Conectar ao servidor
publisher.connect()

# Criar extract a partir de um DataFrame
publisher.create_hyper_extract(df, "output/data.hyper", table_name="Sales")

# Publicar workbook
result = publisher.publish_workbook("dashboard.twbx", project_name="Production")

# Publicar data source
result = publisher.publish_datasource("data.tdsx", project_name="Analytics")

# Refresh de extract
publisher.refresh_extract(datasource_id="ds-123")

# Listar workbooks
workbooks = publisher.list_workbooks(project_name="Analytics")

# Desconectar
publisher.disconnect()
```

> **Nota:** Este é um framework de demonstração que ilustra os padrões de automação do Tableau Server. Para uso em produção, integre com [tableauserverclient](https://tableau.github.io/server-client-python/) (TSC) e [pantab](https://pantab.readthedocs.io/) / [tableauhyperapi](https://help.tableau.com/current/api/hyper_api/en-us/index.html) para operações reais.

### 📝 Exemplos de Uso

#### Exemplo 1: Publicar Workbook Simples

```python
from src.tableau_automation.tableau_publisher import TableauPublisher

# Conectar ao Tableau Server
publisher = TableauPublisher(
    server_url="https://tableau.company.com",
    site_id="analytics",
    username="admin",
    password="secure_password"
)
publisher.connect()

# Publicar workbook
result = publisher.publish_workbook(
    workbook_path="dashboards/sales_dashboard.twbx",
    project_name="Production",
    workbook_name="Sales Dashboard"
)

print(f"Published: {result['workbook_name']}")

publisher.disconnect()
```

#### Exemplo 2: Pipeline Completo (ETL → Hyper → Publish)

```python
import pandas as pd
from datetime import datetime

# 1. Extrair dados do banco
df = pd.read_sql("""
    SELECT 
        order_date,
        product_category,
        SUM(sales) as total_sales,
        COUNT(*) as order_count
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY order_date, product_category
""", connection)

# 2. Transformar dados
df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.strftime('%Y-%m')

# 3. Criar extract Hyper
publisher = TableauPublisher(...)
publisher.connect()

hyper_path = f"extracts/sales_data_{datetime.now():%Y%m%d}.hyper"
publisher.create_hyper_extract(df, hyper_path, table_name="SalesData")

# 4. Publicar data source
datasource = publisher.publish_datasource(
    datasource_path=hyper_path,
    project_name="Production",
    datasource_name="Sales Data - Last 30 Days"
)

print(f"✓ Pipeline completed! Data source ID: {datasource.id}")
```

#### Exemplo 3: Operações em Lote

```python
# Atualizar todos os extracts de um projeto
def refresh_all_project_extracts(publisher, project_name):
    # Listar todas as data sources do projeto
    all_datasources, _ = publisher.server.datasources.get()
    
    project_datasources = [
        ds for ds in all_datasources 
        if ds.project_name == project_name
    ]
    
    print(f"Found {len(project_datasources)} data sources in {project_name}")
    
    # Refresh cada uma
    for ds in project_datasources:
        try:
            publisher.refresh_extract(ds.id)
            print(f"✓ Refreshed: {ds.name}")
        except Exception as e:
            print(f"✗ Failed to refresh {ds.name}: {e}")

# Executar
publisher = TableauPublisher(...)
publisher.connect()
refresh_all_project_extracts(publisher, "Production")
```

#### Exemplo 4: Integração com Airflow

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def publish_tableau_dashboard(**context):
    """Task do Airflow para publicar dashboard."""
    publisher = TableauPublisher(
        server_url=Variable.get("tableau_server_url"),
        site_id=Variable.get("tableau_site_id"),
        username=Variable.get("tableau_username"),
        password=Variable.get("tableau_password")
    )
    
    publisher.connect()
    
    # Publicar workbook
    workbook = publisher.publish_workbook(
        workbook_path="/opt/airflow/dashboards/daily_report.twbx",
        project_name="Production"
    )
    
    # Armazenar ID no XCom para próximas tasks
    context['task_instance'].xcom_push(key='workbook_id', value=workbook.id)
    
    publisher.disconnect()

# Definir DAG
with DAG(
    'tableau_dashboard_publish',
    default_args={'owner': 'data-team'},
    schedule_interval='0 6 * * *',  # Todo dia às 6h
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:
    
    publish_task = PythonOperator(
        task_id='publish_dashboard',
        python_callable=publish_tableau_dashboard
    )
```

### 🧪 Testes

```bash
# Executar todos os testes
pytest tests/

# Executar com cobertura
pytest --cov=src tests/

# Testar conexão com Tableau Server
python -c "from src.tableau_automation.tableau_publisher import TableauPublisher; \
           p = TableauPublisher('https://tableau.company.com', 'user', 'pass', 'site'); \
           p.connect(); print('Connection successful')"
```

### 📊 Funcionalidades Avançadas

> Os exemplos abaixo usam a biblioteca `tableauserverclient` (TSC) diretamente. Servem como referência para quando você integrar o framework com uma instalação real do Tableau Server.

#### 1. Gerenciamento de Permissões

```python
def set_workbook_permissions(publisher, workbook_id, group_name, permissions):
    """Configurar permissões de um workbook."""
    # Buscar grupo
    groups, _ = publisher.server.groups.get()
    group = next((g for g in groups if g.name == group_name), None)
    
    # Criar regras de permissão
    rules = [
        TSC.PermissionsRule(
            grantee=group,
            capabilities={
                TSC.Permission.Capability.Read: TSC.Permission.Mode.Allow,
                TSC.Permission.Capability.ExportImage: TSC.Permission.Mode.Allow,
                TSC.Permission.Capability.ViewComments: TSC.Permission.Mode.Allow
            }
        )
    ]
    
    # Aplicar permissões
    publisher.server.workbooks.update_permissions(workbook_id, rules)
    print(f"✓ Permissions updated for workbook {workbook_id}")
```

#### 2. Versionamento de Dashboards

```python
def backup_all_workbooks(publisher, backup_dir):
    """Fazer backup de todos os workbooks."""
    import os
    from datetime import datetime
    
    # Criar diretório de backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, timestamp)
    os.makedirs(backup_path, exist_ok=True)
    
    # Listar todos os workbooks
    all_workbooks, _ = publisher.server.workbooks.get()
    
    print(f"Backing up {len(all_workbooks)} workbooks...")
    
    for wb in all_workbooks:
        try:
            filename = f"{wb.project_name}_{wb.name}.twbx".replace(" ", "_")
            output_path = os.path.join(backup_path, filename)
            publisher.download_workbook(wb.id, output_path)
            print(f"✓ Backed up: {wb.name}")
        except Exception as e:
            print(f"✗ Failed to backup {wb.name}: {e}")
    
    print(f"✓ Backup completed: {backup_path}")
```

### 🎓 Conceitos Técnicos

#### Tableau Server REST API

A API REST do Tableau permite operações programáticas:

- **Authentication**: Sign in/out, tokens
- **Workbooks**: Publish, download, update, delete
- **Data Sources**: Publish, refresh, update connections
- **Projects**: Create, list, permissions
- **Users & Groups**: Manage access control

#### Hyper API

O Hyper é o motor de dados do Tableau:

- **Performance**: Significativamente mais rápido que o antigo formato TDE
- **Compression**: Reduz o tamanho dos extracts em relação ao TDE
- **Scalability**: Suporta datasets grandes
- **Python Integration**: Criar extracts programaticamente

### 💡 Melhores Práticas

1. **Use Personal Access Tokens** ao invés de senhas
2. **Implemente retry logic** para operações de rede
3. **Valide dados** antes de criar extracts
4. **Use projetos** para organizar dashboards
5. **Configure alertas** para falhas de refresh
6. **Documente** conexões de data sources
7. **Teste em DEV** antes de publicar em PROD

### 🔗 Recursos Adicionais

- [Tableau Server REST API Documentation](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm)
- [tableauserverclient Documentation](https://tableau.github.io/server-client-python/)
- [Hyper API Documentation](https://help.tableau.com/current/api/hyper_api/en-us/index.html)

### 🧪 Testes e Qualidade

Este projeto inclui uma suíte completa de testes e ferramentas de qualidade de código:

```bash
# Executar todos os testes
pytest tests/ -v

# Executar testes com relatório de cobertura
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Verificar qualidade do código
black src tests  # Formatação
flake8 src tests  # Linting
pylint src  # Análise estática
```

Para verificar o estado dos testes e a qualidade do código, execute os comandos acima.

### 🤝 Como Contribuir

Contribuições são bem-vindas! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) para detalhes sobre:

- Como configurar o ambiente de desenvolvimento
- Padrões de código e estilo
- Como executar testes
- Processo de submissão de Pull Requests

**Passos rápidos:**

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 🎯 Próximos Passos

- [x] Adicionar suíte de testes
- [ ] Adicionar suporte para Tableau Online
- [ ] Implementar logging estruturado
- [ ] Criar CLI para operações comuns
- [ ] Adicionar testes de integração com Tableau Server real
- [ ] Implementar cache de autenticação

---

## 🇬🇧 Tableau Dashboard Automation with Python

This repository provides a framework for automating tasks on **Tableau Server** using Python. The solution enables creating, publishing, updating, and managing dashboards and data sources programmatically, integrating Tableau into **DataOps** and **Analytics Engineering** pipelines.

### 🚀 Quick Start

```bash
git clone https://github.com/galafis/tableau-python-automated-dashboard-generator.git
cd tableau-python-automated-dashboard-generator
pip install -r requirements.txt
python examples/publish_workbook.py
```

### 🎓 Key Learnings

- Automate Tableau Server operations with Python
- Create Hyper extracts from Pandas DataFrames
- Integrate Tableau with data pipelines
- Manage permissions programmatically
- Build DataOps workflows

### 🧪 Testing & Quality

Run the commands below to verify tests and code quality locally.

```bash
# Run tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Code quality checks
black src tests && flake8 src tests && pylint src
```

### 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Development environment setup
- Code style and standards
- Testing requirements
- Pull request process

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Author:** Gabriel Demetrios Lafis  
**License:** MIT  
**Last Updated:** February 2026
