from flask import (
  Flask,
  render_template,
  request as flask_req
)
import requests

app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:5000/tasks"

@app.get("/")
def home():
  return render_template("index.html")

@app.get("/about")
def about():
  return render_template("about.html")

@app.get("/tasks")
def task_list():
  response = requests.get(BACKEND_URL)
  if response.status_code == 200:
    task_list = response.json().get("tasks")
    return render_template("list.html", tasks=task_list)
  return (
    render_template("error.html", err_code=response.status_code),
    response.status_code
  )

@app.get("/tasks/new")
def new_task():
  return render_template("new.html")

@app.post("/tasks/new")
def post_task():
  task_data = flask_req.form
  response = requests.post(BACKEND_URL, json=task_data)
  if response.status_code == 204:
    return render_template("success.html", msg="Task created successfully")
  return (
    render_template("error.html", err_code=response.status_code),
    response.status_code
  )

@app.get("/tasks/<int:pk>")
def task_detail(pk):
  url = "%s/%s" % (BACKEND_URL, pk)
  response = requests.get(url)
  if response.status_code == 200:
    single_task = response.json().get("task")
    if single_task == {}:
      return (
        render_template("error.html", err_code=404), 404)
    return render_template("detail.html", task=single_task)
  return (
    render_template("error.html", err_code=response.status_code),
    response.status_code
  )

@app.get("/tasks/<int:pk>/edit")
def edit_task(pk):
  url = "%s/%s" % (BACKEND_URL, pk)
  response = requests.get(url)
  if response.status_code == 200:
    single_task = response.json().get("task")
    if single_task == {}:
      return (
        render_template("error.html", err_code=404), 404)
    return render_template("edit.html", task=single_task)
  return (
    render_template("error.html", err_code=response.status_code),
    response.status_code
  )

@app.post("/tasks/<int:pk>/edit")
def edit_task_request(pk):
  url = "%s/%s" % (BACKEND_URL, pk)
  task_data = flask_req.form
  response = requests.put(url, json=task_data)
  if response.status_code == 204:
    return render_template("success.html", msg="Task updated successfully")
  return (
    render_template("error.html", err_code=response.status_code),
    response.status_code
  )

@app.get("/tasks/<int:pk>/delete")
def delete_task(pk):
  url = "%s/%s" % (BACKEND_URL, pk)
  response = requests.get(url)
  if response.status_code == 200:
    single_task = response.json().get("task")
    if single_task == {}:
      return (
        render_template("error.html", err_code=404), 404)
    return render_template("delete.html", task=single_task)
  return (
    render_template("error.html", err_code=response.status_code),
    response.status_code
  )

@app.post("/tasks/<int:pk>/delete")
def delete_task_request(pk):
  url = "%s/%s" % (BACKEND_URL, pk)
  response = requests.delete(url)
  if response.status_code == 204:
    return render_template("success.html", msg="Task deleted successfully")
  return (
    render_template("error.html", err_code=response.status_code),
    response.status_code
  )

# For testing purposes
@app.get("/error")
def error():
  return render_template("error.html")

@app.get("/success")
def success():
  return render_template("success.html")