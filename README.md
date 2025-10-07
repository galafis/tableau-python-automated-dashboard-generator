# Tableau Dashboard Automation with Python

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![Automation](https://img.shields.io/badge/Automation-00C853?style=for-the-badge)

---

## 🇧🇷 Automação de Dashboards Tableau com Python

Este repositório fornece um **framework completo e profissional** para automação de tarefas no **Tableau Server** utilizando Python. A solução permite criar, publicar, atualizar e gerenciar dashboards e fontes de dados de forma programática, integrando o Tableau em pipelines modernos de **DataOps** e **Analytics Engineering**.

### 🎯 Objetivo

Demonstrar como a **Tableau Server REST API** pode ser usada para eliminar tarefas manuais repetitivas, permitindo que equipes de dados implementem workflows automatizados, versionamento de dashboards e integração contínua (CI/CD) para analytics.

### 🌟 Por que Automatizar o Tableau?

A automação do Tableau traz benefícios significativos para equipes de dados:

| Benefício | Impacto |
|-----------|---------|
| **Economia de Tempo** | Reduz 80%+ do tempo gasto em tarefas manuais |
| **Consistência** | Elimina erros humanos em publicações |
| **Escalabilidade** | Gerencia centenas de dashboards simultaneamente |
| **Versionamento** | Controle de versão via Git para dashboards |
| **CI/CD** | Deploy automatizado de dashboards em produção |
| **Monitoramento** | Alertas automáticos para falhas de refresh |

### 📊 Casos de Uso Reais

1. **BI Automation**: Publicar automaticamente 50+ dashboards toda segunda-feira às 6h
2. **Data Refresh**: Atualizar extracts após conclusão de pipelines ETL
3. **Multi-Environment**: Promover dashboards de DEV → QA → PROD automaticamente
4. **Backup & Recovery**: Fazer backup diário de todos os workbooks
5. **Bulk Operations**: Atualizar permissões de 100+ dashboards em segundos

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
│   └── bulk_operations.py            # Operações em lote
├── tests/
│   └── test_tableau_api.py           # Testes unitários
├── config/
│   └── tableau_config.yaml           # Configuração do servidor
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

```python
import tableauserverclient as TSC
import pandas as pd
from pathlib import Path

class TableauPublisher:
    """
    Framework para automação do Tableau Server.
    
    Funcionalidades:
    - Autenticação com Tableau Server
    - Publicação de workbooks e data sources
    - Refresh de extracts
    - Gerenciamento de permissões
    """
    
    def __init__(self, server_url, site_id, username, password):
        self.server_url = server_url
        self.site_id = site_id
        self.username = username
        self.password = password
        self.server = None
        self.auth = None
    
    def connect(self):
        """Conectar ao Tableau Server."""
        self.server = TSC.Server(self.server_url, use_server_version=True)
        self.auth = TSC.TableauAuth(
            self.username, 
            self.password, 
            site_id=self.site_id
        )
        self.server.auth.sign_in(self.auth)
        print(f"✓ Connected to {self.server_url}")
    
    def publish_workbook(self, workbook_path, project_name, 
                        overwrite=True, show_tabs=True):
        """
        Publicar workbook no Tableau Server.
        
        Args:
            workbook_path: Caminho para o arquivo .twb ou .twbx
            project_name: Nome do projeto no Tableau
            overwrite: Se deve sobrescrever workbook existente
            show_tabs: Se deve mostrar as tabs do workbook
        
        Returns:
            workbook_item: Objeto do workbook publicado
        """
        # Encontrar projeto
        all_projects, _ = self.server.projects.get()
        project = next((p for p in all_projects if p.name == project_name), None)
        
        if not project:
            raise ValueError(f"Project '{project_name}' not found")
        
        # Configurar opções de publicação
        publish_mode = TSC.Server.PublishMode.Overwrite if overwrite else TSC.Server.PublishMode.CreateNew
        
        # Criar workbook item
        workbook_item = TSC.WorkbookItem(project.id)
        workbook_item.show_tabs = show_tabs
        
        # Publicar
        print(f"Publishing {workbook_path} to {project_name}...")
        workbook_item = self.server.workbooks.publish(
            workbook_item,
            workbook_path,
            publish_mode
        )
        
        print(f"✓ Workbook published: {workbook_item.name} (ID: {workbook_item.id})")
        return workbook_item
    
    def create_hyper_extract(self, df, output_path, table_name="Extract"):
        """
        Criar arquivo .hyper (Tableau extract) a partir de DataFrame.
        
        Args:
            df: Pandas DataFrame
            output_path: Caminho para salvar o arquivo .hyper
            table_name: Nome da tabela no extract
        """
        from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, \
            NOT_NULLABLE, NULLABLE, SqlType, TableDefinition, Inserter, escape_name, escape_string_literal
        
        # Mapear tipos Pandas → Hyper
        type_mapping = {
            'int64': SqlType.big_int(),
            'float64': SqlType.double(),
            'object': SqlType.text(),
            'datetime64[ns]': SqlType.timestamp(),
            'bool': SqlType.bool()
        }
        
        # Criar definição da tabela
        columns = []
        for col_name, dtype in df.dtypes.items():
            sql_type = type_mapping.get(str(dtype), SqlType.text())
            columns.append(TableDefinition.Column(col_name, sql_type, NULLABLE))
        
        table_def = TableDefinition(
            table_name=table_name,
            columns=columns
        )
        
        # Criar arquivo .hyper
        with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(
                endpoint=hyper.endpoint,
                database=output_path,
                create_mode=CreateMode.CREATE_AND_REPLACE
            ) as connection:
                
                connection.catalog.create_table(table_def)
                
                # Inserir dados
                with Inserter(connection, table_def) as inserter:
                    for row in df.itertuples(index=False):
                        inserter.add_row(row)
                    inserter.execute()
        
        print(f"✓ Hyper extract created: {output_path}")
    
    def refresh_extract(self, datasource_id):
        """
        Atualizar extract de uma data source.
        
        Args:
            datasource_id: ID da data source no Tableau
        """
        print(f"Refreshing extract for datasource {datasource_id}...")
        self.server.datasources.refresh(datasource_id)
        print(f"✓ Extract refresh initiated")
    
    def download_workbook(self, workbook_id, output_path):
        """
        Fazer download de um workbook do Tableau Server.
        
        Args:
            workbook_id: ID do workbook
            output_path: Caminho para salvar o arquivo
        """
        print(f"Downloading workbook {workbook_id}...")
        file_path = self.server.workbooks.download(workbook_id, filepath=output_path)
        print(f"✓ Workbook downloaded: {file_path}")
        return file_path
    
    def disconnect(self):
        """Desconectar do Tableau Server."""
        if self.server:
            self.server.auth.sign_out()
            print("✓ Disconnected from Tableau Server")
```

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
workbook = publisher.publish_workbook(
    workbook_path="dashboards/sales_dashboard.twbx",
    project_name="Production",
    overwrite=True
)

print(f"Dashboard URL: {publisher.server_url}/views/{workbook.name}")

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
           p = TableauPublisher('https://tableau.company.com', 'site', 'user', 'pass'); \
           p.connect(); print('✓ Connection successful')"
```

### 📊 Funcionalidades Avançadas

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

- **Performance**: 10-100x mais rápido que TDE
- **Compression**: Reduz tamanho dos extracts em 50-70%
- **Scalability**: Suporta bilhões de linhas
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

### 🎯 Próximos Passos

- [ ] Adicionar suporte para Tableau Online
- [ ] Implementar logging estruturado
- [ ] Criar CLI para operações comuns
- [ ] Adicionar testes de integração
- [ ] Implementar cache de autenticação

---

## 🇬🇧 Tableau Dashboard Automation with Python

This repository provides a **complete and professional framework** for automating tasks on **Tableau Server** using Python. The solution enables creating, publishing, updating, and managing dashboards and data sources programmatically, integrating Tableau into modern **DataOps** and **Analytics Engineering** pipelines.

### 🚀 Quick Start

```bash
git clone https://github.com/galafis/tableau-python-automated-dashboard-generator.git
cd tableau-python-automated-dashboard-generator
pip install -r requirements.txt
python examples/publish_workbook.py
```

### 🎓 Key Learnings

- ✅ Automate Tableau Server operations with Python
- ✅ Create Hyper extracts from Pandas DataFrames
- ✅ Implement CI/CD for analytics dashboards
- ✅ Integrate Tableau with data pipelines
- ✅ Manage permissions programmatically
- ✅ Build DataOps workflows

---

**Author:** Gabriel Demetrios Lafis  
**License:** MIT  
**Last Updated:** October 2025
