import boto3
import json
import argparse
from datetime import datetime as dt
import time

parser = argparse.ArgumentParser(
    description='Who did create this instance?')
parser.add_argument(
    '-s','--start-time',
    action='store',
    dest='start_time',
    required=True,
    help='Specify start time the instance is supposed to be created. Format = YYYY/MM/DD HH:MM:SS(UTC)'
)
parser.add_argument(
    '-e','--end-time',
    action='store',
    dest='end_time',
    required=True,
    help='Specify end time the instance is supposed to be created. Format = YYYY/MM/DD HH:MM:SS(UTC)'
)
parser.add_argument(
    '-l','--log-group-name',
    action='store',
    dest='log_group_name',
    required=True,
    help='Specify CloudWatch Log group name that contains CloudTrail log. Usucally this is "CloudTrail/DefaultLogGroup". You can find in CloudTrail Configuration.'
)
parser.add_argument(
    '-i','--instance-id',
    action='store',
    dest='instance_id',
    required=True,
    help='Specify EC2 instance ID you want to find who create this.'
)
args = parser.parse_args()
start_time = args.start_time
end_time = args.end_time
log_group_name = args.log_group_name
instance_id = args.instance_id

def convert_time_into_unixtime(tm_str):
    # Cast time stamp text into datetime object
    tm = dt.strptime(tm_str, '%Y/%m/%d %H:%M:%S')

    # Convert into unix time, millisecond
    ts = int(time.mktime(tm.utctimetuple()) * 1000)
    return ts

if __name__ == '__main__':

    # Serch CloudWatch Logs
    cwl = boto3.client('logs')
    request = {
        "logGroupName" : log_group_name,
        "startTime" : convert_time_into_unixtime(start_time),
        "endTime" : convert_time_into_unixtime(end_time),
        "filterPattern" : '{ ( $.responseElements.instancesSet.items[0].instanceId =' + instance_id  + ') && ( $.eventName = "RunInstances" ) }'
    }
    print('Searching instance creation event in CloudWatch Logs.....')

    response = cwl.filter_log_events(**request)
    event = json.loads(response["events"][0]["message"])

    # Parse Event
    event_time = event['eventTime']
    creator_identity = event['userIdentity']['principalId']
    source_ip = event['sourceIPAddress']

    # Print header

    _format = "{0:<20} {1:<" + str(len(creator_identity) + 1) + "} {2:<20}"
    print(_format.format('Creation Date', 'Creator Identity', 'Source IP'))

    # Print Row
    print(_format.format( event_time,creator_identity,source_ip ))

    # print(json.dumps(event, indent=4))