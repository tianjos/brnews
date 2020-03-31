# brnews
API para consulta dos feeds dos principais sites de notícias do Brasil

## requisitos para inicializar a aplicação (dev)
- export FLASK_APP=main.py
- flask create_all
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

*nota (busca é case sensitive)
