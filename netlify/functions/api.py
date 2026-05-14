from backend.app import create_app
from serverless_wsgi import handle_request

app = create_app()

def handler(event, context):
    # This replaces app.run()
    return handle_request(app, event, context)
