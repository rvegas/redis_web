from redis import StrictRedis
from flask import Flask, request

r = StrictRedis()
app = Flask(__name__)

r.set('visits', 1000)
user_id = None
login_result = b"FAIL"


def get_page(key):
    return r.get('pages:' + key)


def get_user_name(user_id):
    return r.hget('users:' + str(user_id), 'name')


def get_visits():
    return r.get('visits')


def process_login(username, password):
    global user_id, login_result
    user_id = r.hget('userids', username)
    if password == r.hget(b'users:' + user_id, 'password').decode():
        login_result = b"SUCCESS"
    else:
        login_result = b"FAIL"


def get_data(user_id):
    global login_result
    user_name = get_user_name(user_id)
    if user_name is None:
        user_name = b""
    return {
        'user_name': user_name,
        'login_result': login_result,
        'visits': get_visits(),
    }


def enrich(content, data):
    enriched_content = content.replace(b"USER_NAME", bytearray(data.get('user_name', b"").capitalize()))
    enriched_content = enriched_content.replace(b"USER_ID", bytearray(data.get('user_id', b"")))
    enriched_content = enriched_content.replace(b"USER_LASTNAME", bytearray(data.get('user_lastname', b"")))
    enriched_content = enriched_content.replace(b"VISITS", bytearray(data.get('visits', b"0")))
    enriched_content = enriched_content.replace(b"LOGIN_RESULT", bytearray(data.get('login_result', b"")))
    return enriched_content


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handle(path):
    if path == '':
        path = 'index.html'
    if path == 'login_process':
        process_login(request.args.get('username', ""), request.args.get('password', ""))
    content = get_page(key=path.split('.')[0])
    if content is None:
        return ""
    r.incr('visits')
    data = get_data(1000)
    content = enrich(content, data)
    return content


