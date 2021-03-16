# Activate virtual env
source venv/bin/activate

# Run uvicorn app on specified port
uvicorn burnthrough:app --port 3000
