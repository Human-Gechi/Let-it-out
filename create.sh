#!/bin/bash
set -euo pipefail
echo "Create backend/ inside $(pwd)"

#Directories
mkdir -p backend/app/routers
mkdir -p backend/app/services
mkdir -p backend/app/prompts
mkdir -p backend/tests

#init files
touch backend/app/__init__.py
touch backend/app/routers/__init__.py
touch backend/app/services/__init__.py


touch backend/app/main.py
touch backend/app/config.py
touch backend/app/schemas.py

touch backend/app/routers/health.py
touch backend/app/routers/prompts.py
touch backend/app/routers/reflect.py

#Services
touch backend/app/services/safety.py
touch backend/app/services/ai_client.py
touch backend/app/services/ratelimit.py

#seed dataa
touch backend/app/prompts/seed_prompts.json

#tests files
touch backend/tests/test_health.py
touch backend/tests/test_reflect.py

touch backend/.env.example
touch backend/requirements.txt

echo "Done"