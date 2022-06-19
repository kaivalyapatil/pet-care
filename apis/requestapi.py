
from fileinput import filename
from flask import Blueprint,jsonify,make_response, request
from flask_cors import cross_origin

from models.updatequery import Updatequery
api=Blueprint("requestapi",__name__)
from models.petrequest import Petrequest
from aws.aws_s3 import upload_file
from aws.aws_ses import send_email,send_mail_with_attachments
from werkzeug.utils import secure_filename
from models.requestresponse import Requestresponse
import io
from models.query import Query




def get_blueprint():
    return api


arr=[]

@api.route('/register',methods=['POST'])
@cross_origin()
def register_request():
    
    data=request.form.to_dict()
    file1 = request.files['image']
    file2 = request.files['doc']
    
    addrequest=Petrequest(
        request_id=data['request_id'],
        fullname=data['fullname'],
        email=data['email'],
        mobile=data['mobile'],
        address=data['address'],
        city=data['city'],
        pincode=data['pincode'],
        pet_catagory=data['pet_catagory'],
        pet_age=data['pet_age'],
        pet_gender=data['pet_gender'],
        issue_description=data['issue_description'],
        image=secure_filename(file1.filename),
        reports=secure_filename(file2.filename)
    )
    arr.append(addrequest)
    binary_file = io.BytesIO(file1.read())    
    upload_file(binary_file,"pet-care-new",secure_filename(file1.filename))
    # to customer 
    sub1="pet protal"
    msg1=f"""
        <html>
            <head><title>Conformation mail</title></head>
            <body>
                <h3>Request send successfully</h3>
            </body>
        </html>
    """
    from_addr1="kaivalyapatil0@gmail.com"
    to_addr1=addrequest.email
    send_email(sub1,msg1,from_addr1,to_addr1)

    #owner
    sub="PET CARE PORTAL"
    msg=f"""
        <html>
            <head><title>Request for pet-service Appointment</title></head>
            <body>
                <h3>Hello sir </h3>
                <p>My name is {addrequest.fullname} ,I have a {addrequest.pet_catagory} .From last 2 days my pet condition is not well .i have mention in detail below ,also attahced some photos and documents regarding the issue.</p>
                <h5>Issue : {addrequest.issue_description}.</h5>
                <h5>i request you to arrange doctor as early as possible.</h5>
                <h5>thank you.</h5>
                <h5>Address:{addrequest.address} , city:{addrequest.city}, pincode:{addrequest.pincode}</h5>
                <h5>pet_catagory:{addrequest.pet_catagory}, pet_age:{addrequest.pet_age}, pet_gender:{addrequest.pet_gender}</h5>
                <h5>image:{addrequest.image}</h5>
                <h5>reports:{addrequest.reports}</h5>
            </body>
        </html>
    """


    from_addr=addrequest.email
    to_addr="kaivalyapatil0@gmail.com"
    file_attachments=[addrequest.image,addrequest.reports]
    send_mail_with_attachments(sub,msg,from_addr,to_addr,file_attachments)
              
    
    return make_response(jsonify({'message':'request sent'}),201)


@api.route('/list',methods=["GET"])
@cross_origin()
def get_request():
    return jsonify( [c.serialize() for c in arr] )


# owner to customer 
arr2=[]

@api.route('/sendmail',methods=["POST"])
@cross_origin()
def send_response_mail():
    data=request.json
    requestdata=Requestresponse(
        request_id=data['request_id'],
        doctor_name=data['doctor_name'],
        email=data['email'],
        mobile=data['mobile'],
        visit_date_time=data['visit_date_time'],
        fees=data['fees']
    )
    arr2.append(requestdata)
    print(arr2)
   
    sub="PET CARE PORTAL"
    msg=f"""
        <html>
            <head><title>Response from pet Care Center</title></head>
            <body>    
                <h3>Thank you for beliving in us</h3>
                <p>your appointment details given below</p>
                <p>request_id:{requestdata.request_id}</p>
                <p>doctor_name:{requestdata.doctor_name}</p>
                <p>email:{requestdata.email} ,     mobile:{requestdata.mobile}</p>
                <p>visit_date_time:{requestdata.visit_date_time}</p>
                <p>fees:{requestdata.fees}</p>
                <h4>owner pet service</h4>
                <h5>mobile no:8898765678</h5>
            </body>
        </html>
    """

   

    from_addr=requestdata.email
    to_addr="kaivalyapatil0@gmail.com"
    send_email(sub,msg,from_addr,to_addr)
    return make_response(jsonify({'message':'request sent'}),201)


# Query

arr_query=[]

@api.route('/querysend',methods=['POST'])
def register_query():
    
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
    arr_query.append(addquery)
    binary_file = io.BytesIO(file1.read())    
    upload_file(binary_file,"pet-care-new",secure_filename(file1.filename))
    sub="PET CARE PORTAL"
    msg=f"""
        <html>
            <head><title>Request for online consultation</title></head>
            <body>
                <p>Hello sir </p>
                <p>My name is {addquery.fullname} ,I have a {addquery.pet_catagory} .From last 2 days my pet condition is not well .i have mention in detail below ,also attahced some photos and documents regarding the issue.</p>
                <p>Issue : {addquery.issue_description}.</p>
                <p>i request you sir to reply as early as possible.</p>
                <p>thank you.</p>
                <p>pet_catagory:{addquery.pet_catagory}</p>
                <p>pet_age:{addquery.pet_age}</p>
                <p>pet_gender:{addquery.pet_gender}</p>
                <p>image:{addquery.image}</p>
                <p>reports:{addquery.reports}</p>
            </body>
        </html>
    """


    from_addr=addquery.email
    to_addr="kaivalyapatil0@gmail.com"
    send_email(sub,msg,from_addr,to_addr)
              
    
    return make_response(jsonify({'message':'request sent'}),201)


@api.route('/listquery',methods=["GET"])
@cross_origin()
def get_query():
    return jsonify( [c.serialize() for c in arr_query] )


# doctor to customer 
arr_queryres=[]

@api.route('/sendrestoquery',methods=["POST"])
@cross_origin()
def send_response_toquery():
    data=request.form.to_dict()
    requestdata1=Updatequery(
        request_id=data['request_id'],
        doctor_name=data['doctor_name'],
        email=data['email'],
        mobile=data['mobile'],
        respond_to_query=data['respond_to_query']
    )
    arr_queryres.append(requestdata1)
    print(arr_queryres)
   

    sub="PET CARE PORTAL"
    msg=f"""
        <html>
            <head><title>Respond to query</title></head>
            <body>
                <h3>Thank you for beliving in us</h3>
                <p>request_id:{requestdata1.request_id}</p>
                <p>respond_to_query:{requestdata1.respond_to_query}</p>
                <p>doctor_name:{requestdata1.doctor_name}</p>
                <p>email:{requestdata1.email} ,     mobile:{requestdata1.mobile}</p>
                <p>
            </body>
        </html>
    """

    

    from_addr=requestdata1.email
    to_addr="kaivalyapatil0@gmail.com"
    send_email(sub,msg,from_addr,to_addr)
    return make_response(jsonify({'message':'request sent'}),201)


@api.route('/listquerysol',methods=["GET"])
@cross_origin()
def get_output():
    return jsonify( [c.serialize() for c in arr_queryres] )

