import boto3
import os
from botocore.exceptions import ClientError
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_email(subject, message, from_addr, to_addr) -> None :

    
    try:
        region=os.environ["AWS_REGION"]
        access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
        secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        ses = boto3.client("ses", 
            region_name=region,
            aws_access_key_id=access_key_id,  
            aws_secret_access_key=secret_access_key)    
    except Exception  as ex:
        ses = boto3.client("ses")

    CHARSET = "UTF-8"
    try:
        #Provide the contents of the email.
        response = ses.send_email(
            Destination={ 'ToAddresses': [ to_addr ]  },
            Message={
                'Body': {                    
                    'Html': {
                        'Charset': CHARSET,
                        'Data': message,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=from_addr
        )    
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f"Email sent! Message ID:{response['MessageId']}")


def send_mail_with_attachments(subject, message,from_addr, to_addr,file_attachments,cc_addresses=None):
    ses = boto3.client("ses",region_name="ap-south-1")
    CHARSET = 'UTF-8'

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From']=from_addr
    msg['To']=to_addr

    #Add message Body
    msgbody = MIMEText(message.encode(CHARSET),'plain',CHARSET)
    msg.attach(msgbody)

    #Add attachments
    for file in file_attachments:
        attachment = MIMEApplication(open(file,'rb').read())
        attachment.add_header('Content-Disposition','attachment',filename=os.path.basename(file))
        msg.attach(attachment)

    try:
        response = ses.send_raw_email(
            Source = from_addr,
            Destinations = [to_addr],
            
            RawMessage={
                'Charset': CHARSET,
                'Data':msg.as_string(),
            }
        )
        print("message id :", response['MessageId'])
        print("Message send Successfully")
    except Exception as e:
        print("Error:", e)
