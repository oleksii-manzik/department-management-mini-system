from dmms.rest.app import app as app_rest
from dmms.views.app import app as app_views


if __name__ == '__main__':
    app_rest.run()
    app_views.run()
