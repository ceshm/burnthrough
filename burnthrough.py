import datetime
import json
import random
import string
from functools import reduce

import uvicorn
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from auth import AuthEndpoint, CookieBasedAuthBackend
from models.base import UserNotes, UserTaskTree, UserDailyData, User, UserSession
from throughput import get_burndown_data
from tree_stuff import traverse_json_tree_list


app = Starlette(debug=True)
app.add_middleware(AuthenticationMiddleware, backend=CookieBasedAuthBackend())

templates = Jinja2Templates(directory='templates')
import socket
if ".local" not in socket.gethostname():
    #app.add_middleware(HTTPSRedirectMiddleware)
    pass
app.mount('/static', StaticFiles(directory='statics'), name='static')


@app.route("/")
class HomepageView(AuthEndpoint):
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

    async def post(self, request, **kwargs):
        form = await request.form()
        print(form["username"])
        print(form["password"])
        try:
            user = User.get(User.username==form["username"], User.password==form["password"])
        except User.DoesNotExist:
            user = None
        if user:
            try:
                usesh = UserSession.get(UserSession.user == user)
            except UserSession.DoesNotExist:
                usesh = UserSession()
                usesh.user = user
                usesh.sessionid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                usesh.device = "device"
                usesh.save()
            response = RedirectResponse(url='/')
            response.set_cookie("sessionid", usesh.sessionid)
            return response
        else:
            return templates.TemplateResponse('login.html', {'request': request, 'error': "bad credentials" })


@app.route("/register")
class RegisterView(HTTPEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)

        return templates.TemplateResponse('register.html', {'request': request })

    async def post(self, request, **kwargs):
        form = await request.form()
        print(form["username"])
        print(form["password"])
        print(form["password_confirm"])


        try:
            user = User.get(User.username==form["username"])
        except User.DoesNotExist:
            user = None
        if user:
            return templates.TemplateResponse('register.html', {'request': request, 'error': "username already exists"})

        if form["password"] != form["password_confirm"]:
            return templates.TemplateResponse('register.html', {'request': request, 'error': "passwords do not match"})
        else:
            user = User()
            user.username = form["username"]
            user.password = form["password"]
            user.data = []
            user.save()
            try:
                usesh = UserSession.get(UserSession.user == user)
            except UserSession.DoesNotExist:
                usesh = UserSession()
                usesh.user = user
                usesh.sessionid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                usesh.device = "device"
                usesh.save()
            response = RedirectResponse(url='/')
            response.set_cookie("sessionid", usesh.sessionid)
            return response


@app.route("/diary")
class DiaryView(AuthEndpoint):

    async def get(self, request):
        today = datetime.datetime.now()
        return RedirectResponse(url="/diary/{0:02d}-{1:02d}-{2:02d}".format(today.year,today.month,today.day))


@app.route("/diary/{date}")
class DiarySpecificView(AuthEndpoint):

    async def get(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])
        prev_date = date - datetime.timedelta(days=1)
        next_date = date + datetime.timedelta(days=1)

        #today = datetime.date(2019, 4, 16)
        try:
            tree = UserTaskTree.get(UserTaskTree.date == date, UserTaskTree.user == self.user)
            traverse_json_tree_list(tree.nodes)
        except UserTaskTree.DoesNotExist:
            tree = None
        try:
            notes = UserNotes.get(UserNotes.user == self.user)
        except UserNotes.DoesNotExist:
            notes = None

        try:
            daily_data = UserDailyData.get(UserDailyData.user == self.user, UserDailyData.date == date)
        except UserDailyData.DoesNotExist:
            daily_data = None

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date, "notes": notes, "prev_date": prev_date,  "next_date": next_date, "daily_data": daily_data})

    async def post(self, request):
        date = datetime.date.fromisoformat(request.path_params["date"])
        prev_date = date - datetime.timedelta(days=1)
        next_date = date + datetime.timedelta(days=1)
        form = await request.form()

        json_nodes = json.loads(form["nodes"])
        pre_actions = []
        if "transfer" in form and form["transfer"]!="":
            json_transfer = json.loads(form["transfer"])
            def transfer(node, path):
                selected_node = None
                if json_transfer["node_id"] == node["id"]:
                    selected_node = ( node, path )
                return selected_node
            pre_actions.append(transfer)

        try:
            tree = UserTaskTree.get(UserTaskTree.date == date,  UserTaskTree.user == self.user)
        except UserTaskTree.DoesNotExist:
            #print("tree does not exist...")
            tree = UserTaskTree()
            tree.user = self.user
            tree.date = date
            tree.name = "awdawd"
        if tree.nodes:
            try:
                pre_results = traverse_json_tree_list(tree.nodes, actions=pre_actions)
            except:
                pass
        else:
            pre_results = []
        for result in pre_results:
            print(result)
            if result["key"] == "transfer":
                transfer_result = result["value"]
                print(transfer_result[0])
                print(transfer_result[1])

                path_list = transfer_result[1].split("/")[1:-1]
                path_list.append(transfer_result[0])

                transfer_tree = reduce(lambda x, y: {
                    "id": ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9)),
                    "label": y,
                    "time_spent": [None, None],
                    "children": [x]
                }, reversed(path_list))

                if json_transfer["date"]:
                    to_tree_date = datetime.date.fromisoformat(json_transfer["date"])
                else:
                    to_tree_date = date + datetime.timedelta(days=1)
                try:
                    to_tree = UserTaskTree.get(UserTaskTree.date == to_tree_date)
                except UserTaskTree.DoesNotExist:
                    to_tree = UserTaskTree()
                    to_tree.user = self.user
                    to_tree.name = "awdawd"
                    to_tree.date = to_tree_date
                if to_tree:
                    if to_tree.nodes:
                        to_tree.nodes.append(transfer_tree)
                    else:
                        to_tree.nodes = [transfer_tree]
                    to_tree.save()

            # ==== Node UPDATE ====
        tree.nodes = json_nodes
        post_results = traverse_json_tree_list(tree.nodes, actions=())

        if "expanded_nodes" in form:
            tree.expanded_nodes = json.loads(form["expanded_nodes"])
        tree.save()

        json_notes = json.loads(form["notes"])
        try:
            notes = UserNotes.get(UserNotes.user == self.user)
            #print("Notes found!")
        except UserNotes.DoesNotExist:
            #print("Notes not exist...")
            notes = UserNotes()
            notes.user = self.user
        notes.notes = json_notes
        notes.save()

        try:
            daily_data = UserDailyData.get(UserDailyData.user == self.user, UserDailyData.date == date)
            # print("Notes found!")
        except UserDailyData.DoesNotExist:
            daily_data = None
        if "levels" in form and form["levels"]!="":
            json_levels = json.loads(form["levels"])
            if not daily_data:
                # print("Notes not exist...")
                daily_data = UserDailyData()
                daily_data.user = self.user
                daily_data.date = date
                daily_data.data = {}
            daily_data.data["levels"] = json_levels
            daily_data.save()

        return templates.TemplateResponse('diary.html', {'request': request, "tree": tree, "date": date, "notes": notes, "prev_date": prev_date,  "next_date": next_date, "daily_data": daily_data })


@app.route("/throughput")
class ThroughputView(AuthEndpoint):
    async def get(self, request):
        #today = datetime.date(2019, 4, 16)
        return templates.TemplateResponse('throughput.html', {'request': request })

    async def post(self, request):

        return templates.TemplateResponse('throughput.html', {'request': request })


@app.route("/burn-down")
class BurnDownView(AuthEndpoint):
    async def get(self, request):
        daily_tp, ptp_ratio, projects = get_burndown_data(2)

        return templates.TemplateResponse('burn-down.html', {'request': request, "projects": projects, "daily_tp": daily_tp, "ptp_ratio": ptp_ratio })

    async def post(self, request):

        return templates.TemplateResponse('burn-down.html', {'request': request })


@app.route('/logout')
async def logout(request):
    response = RedirectResponse(url='/login')
    response.delete_cookie("sessionid")
    return response



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")