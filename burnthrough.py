import datetime
import json

from starlette.applications import Starlette
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from models.base import UserNotes, UserTaskTree

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
import socket
if ".local" not in socket.gethostname():
    #app.add_middleware(HTTPSRedirectMiddleware)
    pass
app.mount('/static', StaticFiles(directory='statics'), name='static')


@app.route("/")
class HomepageView(HTTPEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)
        return templates.TemplateResponse('index.html', {'request': request })

    async def post(self, request):

        return templates.TemplateResponse('index.html', {'request': request })


@app.route("/login")
class LoginView(HTTPEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)
        return templates.TemplateResponse('login.html', {'request': request })

    async def post(self, request):

        return templates.TemplateResponse('index.html', {'request': request })


@app.route("/diary/{date}")
class DiaryView(HTTPEndpoint):

    async def get(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])

        #today = datetime.date(2019, 4, 16)
        try:
            tree = UserTaskTree.get(UserTaskTree.date == date)
            print("Tree found!")
        except UserTaskTree.DoesNotExist:
            print("tree does not exist...")
            tree = None
        except:
            tree = None

        try:
            notes = UserNotes.get(UserNotes.user == 2)
            print("Notes found!")
        except UserNotes.DoesNotExist:
            print("Notes not exist...")
            notes = None

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date, "notes": notes })

    async def post(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])
        form = await request.form()

        json_nodes = json.loads(form["nodes"])
        try:
            tree = UserTaskTree.get(UserTaskTree.date == date)
        except UserTaskTree.DoesNotExist:
            print("tree does not exist...")
            tree = UserTaskTree()
            tree.user = 2
            tree.date = date
            tree.name = "awdawd"
        tree.nodes = json_nodes
        tree.save()

        json_notes = json.loads(form["notes"])
        print(form["notes"])

        try:
            notes = UserNotes.get(UserNotes.user == 2)
            print("Notes found!")
        except UserNotes.DoesNotExist:
            print("Notes not exist...")
            notes = UserNotes()
            notes.user = 2
        notes.notes = json_notes
        notes.save()

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date, "notes": notes})


@app.route("/throughput")
class ThroughputView(HTTPEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)
        return templates.TemplateResponse('throughput.html', {'request': request })

    async def post(self, request):

        return templates.TemplateResponse('throughput.html', {'request': request })