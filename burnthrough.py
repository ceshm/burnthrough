from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
import uvicorn

app = Starlette(debug=True)

@app.route('/')
async def homepage(request):
    return PlainTextResponse('hello world')
