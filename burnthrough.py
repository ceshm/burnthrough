import datetime
import json

from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from models.base import TaskTree

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='statics'), name='static')


@app.route("/")
class Homepage(HTTPEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)
        return templates.TemplateResponse('index.html', {'request': request })

    async def post(self, request):

        return templates.TemplateResponse('index.html', {'request': request })



@app.route("/diary/{date}")
class Homepage(HTTPEndpoint):
    async def get(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])
        #today = datetime.date(2019, 4, 16)
        try:
            tree = TaskTree.get(TaskTree.date == date)
            print("Tree found!")
        except TaskTree.DoesNotExist:
            print("tree does not exist...")
            tree = None

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date })

    async def post(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])
        form = await request.form()
        json_nodes = json.loads(form["nodes"])

        try:
            tree = TaskTree.get(TaskTree.date == date)
        except TaskTree.DoesNotExist:
            print("tree does not exist...")
            tree = TaskTree()
            tree.date = date
            tree.name = "awdawd"
        tree.nodes = json_nodes
        tree.save()

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date})