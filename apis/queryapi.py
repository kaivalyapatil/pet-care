
from fileinput import filename
from flask import Blueprint,jsonify,make_response, request
api=Blueprint("queryapi",__name__)
from flask_cors import cross_origin
from models.query import Query
from aws.aws_s3 import upload_file
from aws.aws_ses import send_email
from werkzeug.utils import secure_filename
from models.requestresponse import Requestresponse
import io

def get_blueprint():
    return api


arr=[]

@api.route('/querysend',methods=['POST'])
def register_request():
    
    data=request.form.to_dict()
    file1 = request.files['image']
    file2 = request.files['doc']
    
    addquery=Query(
        request_id=data['request_id'],
        fullname=data['fullname'],
        email=data['email'],
        mobile=data['mobile'],
        pet_catagory=data['pet_catagory'],
        pet_age=data['pet_age'],
        pet_gender=data['pet_gender'],
        issue_description=data['issue_description'],
        image=secure_filename(file1.filename),
        reports=secure_filename(file2.filename)
    )
    arr.append(addquery)
    binary_file = io.BytesIO(file1.read())    
    upload_file(binary_file,"pet-care-new",secure_filename(file1.filename))
    sub="pet protal"
    msg=f"""
        <html>
            <head><title>Request for Appointment</title></head>
            <body>
                <h3>Hi </h3>
                <p>My name is {addquery.fullname} ,i have a {addquery.pet_catagory} from 2 days its not feeling well.</p>
                <h4>Issue : {addquery.issue_description}</h4>
                <h5> Address </h5>
            </body>
        </html>
    """

    from_addr=addquery.email
    to_addr="kaivalyapatil0@gmail.com"
    send_email(sub,msg,from_addr,to_addr)
              
    
    return make_response(jsonify({'message':'request sent'}),201)


@api.route('/listquery',methods=["GET"])
@cross_origin()
def get_request():
    return jsonify( [c.serialize() for c in arr] )


# doctor to customer 
arr2=[]

@api.route('/sendmail',methods=["POST"])
@cross_origin()
def send_response_toquery():
    data=request.json
    requestdata=Requestresponse(
        request_id=data['request_id'],
        doctor_name=data['doctor_name'],
        email=data['email'],
        mobile=data['mobile'],
        respond_to_query=data['respond_to_query']
    )
    arr2.append(requestdata)
    print(arr2)
   

    sub="pet protal"
    msg=f"""
        <html>
            <head><title>Job Portal</title></head>
            <body>
                <h3>Hi {requestdata.doctor_name},</h3>
                <p>Your registration is successful. You will get the notifications in the registered emails later.</p>
                <h4>Job Portal Team</h4>
                <h5>Better job opportinities</h5>
            </body>
        </html>
    """

    from_addr=requestdata.email
    to_addr="kaivalyapatil0@gmail.com"
    send_email(sub,msg,from_addr,to_addr)
    return make_response(jsonify({'message':'request sent'}),201)

arr3=[]
@api.route('/listquerysol',methods=["GET"])
@cross_origin()
def get_request():
    arr.append(arr2)
    

    return jsonify( [c.serialize() for c in arr] )
    