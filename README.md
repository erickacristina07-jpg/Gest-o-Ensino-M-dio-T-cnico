# Gestão de Dados — Ensino Médio Técnico Senac

Aplicação web para registrar, organizar e acompanhar indicadores de gestão do Ensino Médio Técnico Senac, com formulário de entrada, persistência SQLite, validação de dados, filtros e dashboard interativo.

## Objetivos

- Substituir o preenchimento disperso de indicadores por uma interface centralizada.
- Acompanhar indicadores das unidades Zona Norte e Mossoró.
- Consultar tendências e comparar indicadores ao longo do tempo.
- Exportar os registros para CSV.
- Criar uma base de código organizada para evolução e publicação.

## Indicadores contemplados

A estrutura inicial foi desenhada com base nas abas da planilha `GESTÃO DE DADOS 2026.xlsx`:

- Clubes
- NOA
- NPS
- Evasão
- Atendimentos psicopedagógicos
- Rendimento
- Geekie — estudantes
- Geekie — docentes
- Ocorrências
- Inclusão / PEI
- Formações
- Olimpíadas

O aplicativo normaliza os dados em uma tabela de registros. Campos como unidade, série, categoria, data, status, valor, unidade de medida e fonte permitem analisar diferentes indicadores sem criar uma tabela separada para cada aba.

> **Importante:** esta versão não importa automaticamente os valores da planilha original. Ela utiliza a planilha como referência estrutural e permite cadastrar novos registros. Antes de migrar dados existentes, é necessário definir o mapeamento de cada aba e validar a semântica dos valores.

## Estrutura do repositório

```text
gestao-dados-ensino-medio-senac/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── processing.py
│   └── validation.py
└── tests/
    └── test_processing.py
```

## Requisitos

- Python 3.10 ou superior (recomenda-se Python 3.11 ou 3.12).
- Git, caso deseje clonar e publicar o repositório.
- Navegador atualizado.

## Rodar localmente

### 1. Baixar o projeto

Depois de criar o repositório no GitHub:

```bash
git clone https://github.com/SEU-USUARIO/gestao-dados-ensino-medio-senac.git
cd gestao-dados-ensino-medio-senac
```

Ou baixe o ZIP do projeto e extraia a pasta.

### 2. Criar e ativar um ambiente virtual

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows (Prompt de Comando):

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Executar o aplicativo

```bash
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador, normalmente em `http://localhost:8501`.

Na primeira execução, a aplicação cria a pasta `data/` se necessário e inicializa o banco SQLite.

## Como utilizar

1. Abra **Cadastrar registro**.
2. Informe data, unidade/CEP, indicador, categoria, série (quando aplicável), status, valor, unidade de medida e fonte.
3. Salve o registro.
4. Abra **Dashboard** para consultar KPIs, evolução temporal, comparação entre unidades e distribuição por status.
5. Utilize os filtros laterais para delimitar período, unidade, indicador e status.
6. Em **Consultar e editar**, localize, corrija ou exclua registros.
7. Em **Exportar dados**, baixe um CSV para análise complementar.

### Como interpretar os KPIs

- **Registros:** número de observações cadastradas no recorte selecionado.
- **Unidades:** quantidade de unidades representadas.
- **Indicadores:** quantidade de tipos de indicadores representados.
- **Valor acumulado:** soma numérica dos valores filtrados.
- **Média dos valores:** média numérica dos valores filtrados.

A soma e a média são métricas descritivas gerais. Não devem ser interpretadas como resultado institucional quando misturam unidades de medida diferentes (por exemplo, quantidade de atendimentos, percentual de evasão e pontuação NPS). Para decisões gerenciais, filtre um indicador específico e valide sua regra de cálculo.

## Publicar no GitHub

1. Crie um repositório no GitHub, por exemplo `gestao-dados-ensino-medio-senac`.
2. Não inclua informações pessoais, dados identificáveis de estudantes, planilhas restritas, arquivos `.db`, senhas ou tokens.
3. Na pasta do projeto, execute:

```bash
git init
git add .
git commit -m "Cria aplicativo de gestão de dados do Ensino Médio Técnico"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/gestao-dados-ensino-medio-senac.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário ou organização do GitHub.

## Publicar gratuitamente no Streamlit Community Cloud

1. Envie o projeto ao GitHub.
2. Acesse https://share.streamlit.io/ e entre com sua conta GitHub.
3. Selecione **Create app**.
4. Escolha o repositório, a branch `main` e o arquivo principal `app.py`.
5. Clique em **Deploy**.

O `requirements.txt` permite que o ambiente instale as dependências.

### Limitação importante sobre persistência na nuvem

O SQLite local é apropriado para desenvolvimento, demonstração e uso em uma máquina controlada. Em ambientes de hospedagem gratuita, o sistema de arquivos pode não ser persistente entre reinicializações ou novas implantações. Portanto, não considere o banco SQLite local como armazenamento de produção confiável no Streamlit Community Cloud.

Para uso institucional contínuo, multiusuário e com dados reais, recomenda-se migrar a persistência para um banco gerenciado (por exemplo, PostgreSQL) e configurar autenticação, controle de acesso, backups e monitoramento antes da publicação.

## Segurança e privacidade

- Não publique a planilha original em repositório público sem autorização formal.
- Não insira nomes, CPF, dados de saúde ou detalhes que identifiquem estudantes em campos livres.
- Registros de inclusão/PEI e atendimentos psicopedagógicos podem envolver dados sensíveis. Para esses processos, armazene apenas indicadores agregados e anonimizados, com acesso restrito.
- A aplicação de demonstração não implementa login, perfis de acesso, trilha de auditoria ou criptografia de banco.
- Antes do uso institucional, alinhe a solução com as áreas responsáveis por TI, segurança da informação, jurídico e proteção de dados.

## Arquitetura técnica

- **Streamlit:** interface, formulários, navegação e filtros.
- **Pandas:** padronização e agregações.
- **Plotly Express:** gráficos interativos.
- **Pydantic:** validação dos campos recebidos.
- **SQLite:** armazenamento local.
- **pytest:** testes básicos da camada de processamento.

## Testes

Instale o pytest e execute:

```bash
pip install pytest
pytest
```

## Próximas evoluções recomendadas

1. Importador controlado para cada aba da planilha e relatório de inconsistências.
2. Indicadores calculados com fórmulas próprias (por exemplo, taxa de evasão, adesão ao NOA e NPS), sem misturar medidas incompatíveis.
3. Login institucional e permissões por perfil/unidade.
4. PostgreSQL gerenciado, backups e trilha de auditoria.
5. Exportação de relatórios gerenciais em Excel/PDF.
6. Testes automatizados de validação, importação e regras de negócio.

## Licença e uso institucional

Defina uma licença e a visibilidade do repositório conforme as políticas do Senac. Em caso de dúvida, mantenha o repositório privado até a aprovação institucional.
