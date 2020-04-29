# brnews
API para consulta dos feeds dos principais sites de notícias do Brasil

## requisitos para inicializar a aplicação (dev)
- export FLASK_APP=main.py
- export DB_NAME="brnews"
- export DB_USER="postgres"
- export DB_PASS="changeme"
- export DB_HOST="172.23.0.2"
- export DATABASE_URL="postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}/${DB_NAME}"
- flask db init
- flask db migrate -m 'Initial commit'
- flask db upgrade
- flask run

## Estado atual
- É possível realizar consumir as notícias, fontes(sites) e categorias das notícias
  

    ### Todo:
    - Adicionar indexador de busca
  
## Rotas
- /v1/news/ -> retorna todas as notícias
- /v1/news/{id} -> retorna notícia pelo id
- /v1/news/search/ -> busca por notícias com palavras-chaves no título, sumário ou ambos
- /v1/categories/ -> retorna todas as categorias
- /v1/categories/{id} -> retorna categoria pelo id
- /v1/sources/ -> retorna todas as fontes (sites)
- /v1/sources/{id} -> retorna a fonte pelo id

    ### Todo:
    - melhorar endpoints para retornar filtro da notícia por data, descrição e título

## Busca
- /v1/news/search/?title=Brasil
- /v1/news/search/?summary=Brasil
- /v1/news/search/?title=Brasil&summary=Brasil
- /v1/news/search/?publication_date=01-01-2020,31-01-2020
