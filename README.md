# Find your EC2 instance creator
## What is this used for?
It's used for find who create the EC2 instance.

## What is good for?
Suppose someone on your team creates an EC2 instance without notifying you.  
Three months later the person who created the instance retired.  
Four months later, you were called by you boss to remove EC2 instances that is not in use.  
You would like to ask your team mates, "Hey are you still using this?"

How do you find the EC2 instance creator?  
Unfortunalty, it's not that easy.  
(Or it might be easy if all your teammates are really, really kind and honest)

## Prerequest
Needless to say... you have to have AWS account and credential.  

1. You have to have python runtime, and AWS python SDK, called boto.  
https://aws.amazon.com/sdk-for-python/?nc1=h_ls

2. AWS Credentials and permissions.  
You have to have aws CLI and credentials settings.  
https://docs.aws.amazon.com/streams/latest/dev/kinesis-tutorial-cli-installation.html  
IAM Permission you need to run this is `logs:FilterLogEvents`. 

3. CloudTrail and CloudWatch Logs  
Before using this script, you must enable CloudTrail and set it to output the results to CloudWatch Logs.  
https://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html


## Usage
You can find the creator from the **creation time range**, **instance ID**, and the **Log Group name** in CloudWatch Logs.  
  
**Example**:  

```
python find_instance_creator.py \
-s "2018/08/01 00:00:00" \
-e "2018/08/03 00:00:00" \
-l "CloudTrail/DefaultLogGroup “ \
-i i-020a92a6d9933e212
```

**Sample Output**  
```
Creation Date        Creator Identity                                Source IP           
2018-08-01T06:05:41Z XXXXXXXXXXXXXXXXX:iamcreator@sso.example.local  100.10.0.10
```

## Parameter list
| Full |Short hand|Description|
----|---- |---- 
|--start-time |-s|Log search start time|
|--end-time |-s|Log search end time|
|--log-group-name |-l|Log group name of CloudWatch Logs containing CloudTrail log|
|--instance-id |-i|The EC2 instance ID you want search its creator|

## TIPS
_How I can find the instance creation time?_  
You can find instance creation time by looing EC2 console, description tab.

![creationdate](https://user-images.githubusercontent.com/14175234/46450624-34089180-c7cd-11e8-93d9-b31f7fbc56cc.png)
