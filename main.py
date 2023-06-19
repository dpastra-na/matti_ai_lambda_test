import os
import logging
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt import App

from src.aux_functions import get_agent

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

slack_app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])
handler = SlackRequestHandler(slack_app)

@slack_app.event("message")
def listen_to_messages(event: dict, say: callable) -> None:
    try:
        say(f"Dame un momento, estoy procesando tu consulta...")
        agent = get_agent()
        result = agent.run(event["text"])
        say(f"<@{event['user']}> tu consulta está lista!")
        say(result)
    except Exception as e:
        logger.error(f"Error occurred while processing message: {str(e)}") # logging the exception

def lambda_handler(event, context):
    return handler.handle(event, context)