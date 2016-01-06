import os
import datetime
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

if os.environ.get("I_AM_IN_DEV_ENV") == 'true':
  HOST = 'mechanicalturk.sandbox.amazonaws.com'
else:
  HOST = 'mechanicalturk.amazonaws.com'

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    host=HOST)

url = "https://mturk-poc.herokuapp.com/"
title = "Describe this group of people in your own words"
description = "Describe your first impressions of this group of people however you want."
keywords = ["easy"]
frame_height = 800
amount = 0.05

questionform = ExternalQuestion(url, frame_height)

all_hits = [hit for hit in connection.get_all_hits()]

if all_hits:
  for hit in all_hits:
    connection.disable_hit(hit.HITId)

create_hit_result = connection.create_hit(
  title=title,
  description=description,
  keywords=keywords,
  max_assignments=4,
  lifetime=datetime.timedelta(hours=2),
  question=questionform,
  reward=Price(amount=amount),
  response_groups=('Minimal', 'HITDetail'),
  )

all_hits = [hit for hit in connection.get_all_hits()]

for hit in all_hits:
  assignments = connection.get_assignments(hit.HITId)
  for assignment in assignments:
    # No idea why this is a 2D list.
    question_form_answers = assignment.answers[0]
    for question_form_answer in question_form_answers:
      # "user-input" is the only field we care about.
      if question_form_answer.qid == "user-input":
        user_response = question_form_answer.fields[0]
        print user_response
        print "\n"
