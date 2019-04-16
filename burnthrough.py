from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='statics'), name='static')


@app.route("/")
class Homepage(HTTPEndpoint):
    async def get(self, request):

        return templates.TemplateResponse('index.html', {'request': request})
