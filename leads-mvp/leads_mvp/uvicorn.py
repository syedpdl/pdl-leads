#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uvicorn
import app


if __name__=="__main__":
    uvicorn.run(app.server, host="127.0.0.1", port=8000, debug=True, log_level="info")
