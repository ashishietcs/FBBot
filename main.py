# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import requests
import logging
import json

ACCESS_TOKEN = 'EAAJtXrJBeQIBANjJrVImZCEnwA8x4k6QOPat9ms5JTZB36bpH9KA0NVI13s8H6nn1LN7NnLkdfNriGAsBYZATgeAv5ll5elR5eMhHxBk5hj14vnODM0hZBi1Er3iiqR1ZA1zUHaz02RjpZBRYz3urV8h2xsawUg8ltCqDKdiCMSQZDZD'


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    logging.info("Calling FB apis now")
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('1623295198')


class WebHook(webapp2.RequestHandler):
    def get(self):
        print self.request
        if self.request.GET["hub.mode"] == "subscribe" and self.request.GET["hub.challenge"]:
            if not self.request.GET["hub.verify_token"] == 'secret':
                self.response.set_status(403)
                return self.response.write("Verification token mismatch")
            return self.response.write(self.request.GET["hub.challenge"])
        return self.response.write("Hello World")

    def post(self):
        json_string = self.request.body
        data = json.loads(json_string)
        logging.info(data)
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']
        return reply(sender ,message)


app = webapp2.WSGIApplication([
    ('/', MainPage),('/webhook/',WebHook)
], debug=True)
