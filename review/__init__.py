from flask import Flask
from flask.ext.restless import APIManager
from review.authn import login_manager, auth_func
from review.config import config
from review.database import Base, db_session, engine
from review.models import Collection, Decision, Entry, Review, User

app = Flask(__name__)
app.secret_key = config.get('secrets', 'SECRET')

# Flask-Login and authn code
login_manager.init_app(app)

def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, GET, POST, PATCH, PUT, OPTIONS, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Flask-Restless API endpoints
# note: GET preprocessors pulled in via review.authn.auth_func
manager = APIManager(app, session=db_session, preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]))
collection_blueprint = manager.create_api(Collection, methods=['GET', 'DELETE', 'PATCH', 'POST', 'PUT'], collection_name='collection', url_prefix='/v1')
decision_blueprint = manager.create_api(Decision, methods=['GET', 'DELETE', 'PATCH', 'POST', 'PUT'], collection_name='decision', url_prefix='/v1')
entry_blueprint = manager.create_api(Entry, methods=['GET', 'DELETE', 'PATCH', 'POST', 'PUT'], collection_name='entry', url_prefix='/v1')
review_blueprint = manager.create_api(Review, methods=['GET', 'DELETE', 'PATCH', 'POST', 'PUT'], collection_name='review', url_prefix='/v1')

app.after_request(add_cors_header)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
