
import os
from flask import Flask, request

from threading import Timer

from datetime import datetime, timezone
import dateutil.parser

import logging

from apns2.client import APNsClient
from apns2.payload import Payload
from apns2.credentials import TokenCredentials


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

pusher = None
app = Flask("ChillzieServer")


@app.route("/alarm", methods=['POST', 'GET'])
def alarm():
    error = None
    if request.method == 'POST':
        token_hex = request.form["token_hex"]
        alarm_str = request.form["alarm"]

        logging.debug("Received request: TOKEN=%s, ALARM=%s", token_hex, alarm_str)

        now = datetime.now(timezone.utc)
        alarm = dateutil.parser.parse(alarm_str)

        if alarm < now:
            logging.info("Alarm has passed; ignore request")
            return "<html><body><p>Alarm has passed</p></body></html>"

        interval = alarm - now
        logging.debug("Starting timer: TOKEN=%s, INTERVAL=%r", token_hex, interval)
        Timer(
            interval.seconds,
            push_notification,
            args=[token_hex]
        ).start()

        return "<html><body><p>Alarm set</p></body></html>"

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return "<html><body><p>Sorry wrong page</p></body></html>"


@app.route("/temps", methods=['GET'])
def temps():
    with open('temps.csv', 'r') as t:
        return t.read()


def push_notification(token_hex):
    global pusher

    if pusher is None:
        auth_key_path = os.getenv("APN_KEYSTORE_P8")
        logging.info(f"Building Pusher: {auth_key_path}")
        pusher = NotificationPusher(
            topic="com.chillzie.Chillzie",
            auth_key_path=auth_key_path,
            auth_key_id=os.getenv("APN_AUTH_KEY_ID"),
            team_id=os.getenv("APN_TEAM_ID"),
            use_sandbox=True
        )

    logging.debug("Pushing notification: TOKEN=%s", token_hex)
    pusher.push(token_hex)


class NotificationPusher(object):

    def __init__(self, topic, auth_key_path, auth_key_id, team_id, use_sandbox=False):
        self.topic = topic

        self.client = APNsClient(
            TokenCredentials(auth_key_path, auth_key_id, team_id),
            use_sandbox=use_sandbox,
            use_alternative_port=False
        )

    def push(self, token_hex):
        payload = Payload(alert="Hello World!", sound="default", badge=1)
        self.client.send_notification(token_hex, payload, self.topic)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Starts Flask server and configures the server.')

    parser.add_argument('--p8', required=True, type=str, help='p8 keystore from Apple')
    parser.add_argument('--key-id', required=True, type=str, help='auth key id required for Apple push notification')
    parser.add_argument('--team-id', required=True, type=str, help='auth key id required for Apple push notification')

    args = parser.parse_args()

    logging.info("Init push notifier.")
    pusher = NotificationPusher(
        topic="com.chillzie.Chillzie",
        auth_key_path=args.p8,
        auth_key_id=args.key_id,
        team_id=args.team_id,
        use_sandbox=True
    )

    app.run(host='0.0.0.0')
