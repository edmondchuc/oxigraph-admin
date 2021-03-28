from typing import Optional, List

import httpx
from fastapi import Request, Response, Header, Query
from fastapi.routing import APIRouter

from oxigraph_admin import settings

router = APIRouter()


@router.get('/query')
async def sparql_query_get(
        request: Request,
        query: str = Query(..., alias='query', title='Query', description='SPARQL 1.1 Query.'),
        default_graph_uri: Optional[List[str]] = Query(None, alias='default-graph-uri', title='Default Graph URI', description='The graph to be included in the default graph.'),
        named_graph_uri: Optional[List[str]] = Query(None, alias='named-graph-uri', title='Named Graph URI', description='The graph to be included in the named graph'),
        accept: str = Header(..., description="""SELECT and ASK queries:
- application/sparql-results+json
- application/sparql-results+xml

CONSTRUCT queries:
- text/turtle
- application/n-triples
- application/rdf+xml""")
):
    url = f'{settings.OXIGRAPH_SERVER_URL}/query'

    headers = dict(request.headers)

    params = dict()
    params.update({'query': query})
    if default_graph_uri:
        params.update({'default-graph-uri': default_graph_uri})
    if named_graph_uri:
        params.update({'named-graph-uri': named_graph_uri})

    async with httpx.AsyncClient() as client:
        r: httpx.Response
        client: httpx.AsyncClient
        r = await client.get(url=url, headers=headers, params=params)

        return Response(
            content=r.content,
            status_code=r.status_code,
            headers=r.headers,
            media_type=r.headers.get('content-type')
        )


@router.post('/query')
async def sparql_query_post(request: Request):
    url = f'{settings.OXIGRAPH_SERVER_URL}/query'
    headers = request.headers.items()
    body = await request.body()
    params = dict(request.query_params)

    async with httpx.AsyncClient() as client:
        r: httpx.Response
        client: httpx.AsyncClient
        r = await client.post(url=url, headers=headers, content=body, params=params)

        return Response(
            content=r.content,
            status_code=r.status_code,
            headers=r.headers,
            media_type=r.headers.get('content-type')
        )
