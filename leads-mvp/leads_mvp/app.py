#!/usr/bin/env python3

from fastapi import FastAPI

server = FastAPI()


server.get("/status")
async def status():
    return {"status": "OK"}
