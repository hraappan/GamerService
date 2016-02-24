from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from src.gamer.resources import app as gamer
from gamer_admin.application import app as gamer_admin

application = DispatcherMiddleware(gamer, {
     '/gamer_admin': gamer_admin
})
if __name__ == '__main__':
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)