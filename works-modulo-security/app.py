from flask import Flask, render_template, request, make_response, redirect
import random, os
from Crypto.Util.number import getPrime

app = Flask(__name__)

MOD = getPrime(128)


def gen_id():
    return random.randint(1 << 127, 1 << 128)


def anonymize(user_id):
    return user_id + random.randint(1 << 127, 1 << 128) * MOD


def request_to_user(request):
    try:
        token = int(request.cookies["login_token"])
        return users[user_id_to_idx[token]]
    except:
        return False

admin = {"name": "admin", "id": gen_id(), "status": "administrative"}
admin['anon_id'] = anonymize(admin['id'])

user_id_to_idx = {(admin["id"]): 0}
users = [admin]


def add_user(user):
    if len(users) < 1_000:
        idx = len(users)
        users.append(user)
    else:
        # We can't handle more than 1k users.
        # They probably won't notice, right?
        idx = random.randint(500, 600)
        del user_id_to_idx[users[idx]["id"]]
        users[idx] = user
    user_id_to_idx[user["id"]] = idx

allowed_statuses = ["😃 CHUMMY", "😃 BULLY", "😃 PALSY", "😃 PEPPY", "😃 CHIPPER", "😡 RANCOROUS"]

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@app.route("/", methods=["GET", "POST"])
def index():
    user = request_to_user(request)
    err = ""
    if request.method == "POST":
        if 'status' in request.form:
            status = request.form['status']
            if status in allowed_statuses and user:
                user['status'] = status
            else:
                err = "invalid status!"
        else:
            err = "status not in form!"
    resp = make_response(
        render_template(
            "index.html", 
            users=reversed(users), 
            curr_user=user, 
            allowed_statuses=chunks(allowed_statuses,2),
            err=err
        )
    )
    return resp


@app.route("/flag")
def flag():
    # Only the admin can access the flag!
    user = request_to_user(request)
    if user and user["id"] == admin["id"]:
        return make_response(
            os.environ["FLAG"] if 'FLAG' in os.environ else "don't hardcode secrets in source code!", 
            200
        )
    else:
        return make_response("Hey! You're not allowed to be here! Scram!", 401)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = {
            "name": request.form["username"],
            "id": gen_id(),
            "status": "nothing",
        }
        user['anon_id'] = anonymize(user['id'])
        add_user(user)
        resp = make_response(redirect("/"))
        resp.set_cookie("login_token", str(user["id"]))
        return resp
    else:
        return render_template("login.html")
