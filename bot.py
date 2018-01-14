import os
import random
import time
import pandas as pd
from slackclient import SlackClient


BOT_ID = os.environ.get('BOT_ID')

AT_BOT = "<@"  + BOT_ID + ">"

math = 'math'
gratitude = 'thanks!'
alan = 'trap'
greeting = 'hello'
predict = 'predict'
columns = ['index','text','ts','type','user']
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
   #print('Here')
   #response = slack_client.api_call('channels.history', channel='C3QS3EEV7')
   if predict in command:
      num = random.randint(0,3)
      if num == 0:
         response = "It is unlikely"
      if num == 1:
         response = "Sounds probable to me"
      if num == 2:
         response = "It is unclear"
   if greeting in command:
      response = "Howdy."
   if alan in command:
      response = "That's fucking gay."
   if gratitude in command:
      response = "No problamo!"
   if command.startswith(math):
      token = command.split()
      if token[2] is '+':
         response = token[1] + token[3]
   slack_client.api_call("chat.postMessage", channel=channel, text=response,as_user=True)


def parse_slack(slack_rtm_output):
   output_list = slack_rtm_output
   if output_list and len(output_list) > 0:
      for output in output_list:
         if output and 'text' in output and AT_BOT in output['text']:
            return output['text'].split(AT_BOT)[1].strip().lower() , output['channel']
   return None, None

if __name__ == "__main__":
   raw_json = slack_client.api_call('channels.history', channel = 'C3QS3EEV7')['messages']
   df = pd.DataFrame(raw_json)
   df.columns = columns
   df.set_index('index', inplace=True)
   df.to_csv('C:\\Users\\Nguyen\\Desktop\\SlackBots\\JacobBot\\Data\\historical_data.csv')
   READ_WEBSOCKET_DELAY = 1
   print('Started bot')
   if slack_client.rtm_connect():
      #print("started bot")
      #df = df.append(slack_client.api_call('channels.history', channel='C3QS3EEV7'))
      while True:
         #print(slack_client.api_call('history',channel='general'))
         command, channel = parse_slack(slack_client.rtm_read())
         if command and channel:
            handle_command(command, channel)
         time.sleep(READ_WEBSOCKET_DELAY)
   else:
      print("Fail")
