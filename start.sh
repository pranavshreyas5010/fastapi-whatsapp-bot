#!/bin/bash
uvicorn whatsapp_webhook:app --host 0.0.0.0 --port 10000
