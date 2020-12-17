#!/bin/bash

gunicorn --log-level warning --bind 0.0.0.0:5042 --reuse-port --workers $(nproc) --worker-class uvicorn.workers.UvicornWorker src.main:app



