import os
from flask import render_template
from flask import request
from app import app

if os.environ.get("I_AM_IN_DEV_ENV"):
  AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
  AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"

@app.route('/')
@app.route('/index')
def index():
  if request.args.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
    # Worker hasn't accepted the HIT (task) yet.
    pass
  else:
     # Worker accepted the task.
     # Run some logic here to check if the worker has already completed the task.
     pass

  worker_id = request.args.get("workerId", "")

  return render_template(
    'index.html',
    worker_id = request.args.get("workerId", ""),
    assignment_id = request.args.get("assignmentId", ""),
    amazon_host = AMAZON_HOST,
    hit_id = request.args.get("hitId", ""),
    )

@app.after_request
def apply_headers(response):
  # Without this header, our iFrame will not render in Amazon.
  response.headers['X-Frame-Options'] = 'does_not_matter_what_this_is'

  return response
