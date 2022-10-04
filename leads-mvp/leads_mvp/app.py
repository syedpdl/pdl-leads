#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from leads_mvp.api_client import pdl_company_search

server = FastAPI()


@server.get("/status")
async def status():
    return {"status": "OK"}


@server.post("/generate/profiles", status_code=201, tags=["profiles"])
async def company_search(request: Request):
    params = await request.json()
    try:
        industry = params['industry']
        company_size = params['company_size']
        num_records = params['num_records']
        title_level = params['title_level']
        title_role = params['title_role']

        return pdl_company_search(industry, company_size, num_records, title_level, title_role)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@server.get("/autocomplete", status_code=200, tags=["search"])
async def autocomplete_api(request: Request):
    pass
