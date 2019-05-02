import datetime
import json

from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from models.base import UserNotes, UserTaskTree
from tree_stuff import traverse_json_tree, traverse_json_tree_list

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


@app.route("/diary")
class DiaryView(HTTPEndpoint):

    async def get(self, request):
        today = datetime.datetime.now()
        return RedirectResponse(url="/diary/{0:02d}-{1:02d}-{2:02d}".format(today.year,today.month,today.day))

@app.route("/diary/{date}")
class DiaryView(HTTPEndpoint):

    async def get(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])
        prev_date = date - datetime.timedelta(days=1)
        next_date = date + datetime.timedelta(days=1)

        #today = datetime.date(2019, 4, 16)
        try:
            tree = UserTaskTree.get(UserTaskTree.date == date)
            traverse_json_tree_list(tree.nodes)
            #print("Tree found!")
        except UserTaskTree.DoesNotExist:
            #print("tree does not exist...")
            tree = None
        try:
            notes = UserNotes.get(UserNotes.user == 2)
            #print("Notes found!")
        except UserNotes.DoesNotExist:
            #print("Notes not exist...")
            notes = None

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date, "notes": notes, "prev_date": prev_date,  "next_date": next_date})

    async def post(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])
        prev_date = date - datetime.timedelta(days=1)
        next_date = date + datetime.timedelta(days=1)
        form = await request.form()

        json_nodes = json.loads(form["nodes"])
        try:
            tree = UserTaskTree.get(UserTaskTree.date == date)
        except UserTaskTree.DoesNotExist:
            #print("tree does not exist...")
            tree = UserTaskTree()
            tree.user = 2
            tree.date = date
            tree.name = "awdawd"
        tree.nodes = json_nodes
        traverse_json_tree_list(tree.nodes)
        if "expanded_nodes" in form:
            tree.expanded_nodes = json.loads(form["expanded_nodes"])
        tree.save()

        json_notes = json.loads(form["notes"])
        try:
            notes = UserNotes.get(UserNotes.user == 2)
            #print("Notes found!")
        except UserNotes.DoesNotExist:
            #print("Notes not exist...")
            notes = UserNotes()
            notes.user = 2
        notes.notes = json_notes
        notes.save()

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date, "notes": notes, "prev_date": prev_date,  "next_date": next_date })


@app.route("/throughput")
class ThroughputView(HTTPEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)
        return templates.TemplateResponse('throughput.html', {'request': request })

    async def post(self, request):

        return templates.TemplateResponse('throughput.html', {'request': request })


@app.route("/burn-down")
class ThroughputView(HTTPEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)
        return templates.TemplateResponse('burn-down.html', {'request': request })

    async def post(self, request):

        return templates.TemplateResponse('burn-down.html', {'request': request })