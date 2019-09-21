from starlette.authentication import AuthenticationBackend, SimpleUser, AuthCredentials
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse

from models.base import UserSession


class AuthEndpoint(HTTPEndpoint):

    async def dispatch(self, *args, **kwargs):
        request = Request(self.scope, receive=self.receive)
        print(request.user)
        if not request.user.is_authenticated:
            response = RedirectResponse(url='/login')
            await response(self.scope, self.receive, self.send)
        else:
            self.user = request.user.instance
            return await super(AuthEndpoint, self).dispatch(*args, **kwargs)


class CookieBasedAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        session_id = request.cookies.get("sessionid",None)
        print(session_id)
        if session_id:
            try:
                session = UserSession.get(UserSession.sessionid == session_id)
            except UserSession.DoesNotExist:
                print("no sesh found")
                session = None
            if session:
                print(session.user)
                simpleuser = SimpleUser(session.user.username)
                simpleuser.instance = session.user
                return AuthCredentials(["authenticated"]), simpleuser

        return