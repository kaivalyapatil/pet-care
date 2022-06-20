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


arr_request=[]

@api.route('/api/request',methods=['POST'])
@cross_origin()
def register_request():
    """add the request"""
    
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
    arr_request.append(addrequest)
    
    binary_file1 = io.BytesIO(file1.read())
    binary_file2 = io.BytesIO(file2.read())
    upload_file(binary_file1,"pet-care-new",secure_filename(file1.filename))
    upload_file(binary_file2,"pet-care-new",secure_filename(file2.filename))

    # to customer 
    sub="pet protal"
    msg=f"""
        <html>
            <head><title>Conformation mail</title></head>
            <body>
                <h3>Request send successfully</h3>
            </body>
        </html>
    """
    from_addr="kaivalyapatil0@gmail.com"
    to_addr=addrequest.email
    send_email(sub,msg,from_addr,to_addr)
    return make_response(jsonify({'message':'request sent'}),201)


@api.route('/api/requestlist',methods=["GET"])
@cross_origin()
def get_request():
    '''Get all the request and response'''
    return jsonify( [c.serialize() for c in arr_request] )


@api.route('/api/updaterequest/<int:request_id>',methods=["POST"])
@cross_origin()
def send_res_to_request(request_id):
    '''Add the response to request'''
    data=request.form.to_dict()
    requestdata=Requestresponse(
        request_id=request_id,
        doctor_name=data['doctor_name'],
        email=data['email'],
        mobile=data['mobile'],
        visit_date_time=data['visit_date_time'],
        fees=data['fees']
    )
    arr_request.append(requestdata)
    print(arr_request)
   
    return make_response(jsonify({'message':'request sent'}),201)


# Query

arr_query=[]

@api.route('/api/querysend',methods=['POST'])
def register_query():
    '''Add the query'''
    data=request.form.to_dict()
    file1 = request.files['image']
    file2 = request.files['doc']
    
    addquery=Query(
        query_id=data['query_id'],
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
    binary_file1 = io.BytesIO(file1.read())
    binary_file2 = io.BytesIO(file2.read())  
    upload_file(binary_file1,"pet-care-new",secure_filename(file1.filename))
    upload_file(binary_file2,"pet-care-new",secure_filename(file2.filename))
    return make_response(jsonify({'message':'request sent'}),201)


@api.route('/api/listquery',methods=["GET"])
@cross_origin()
def get_query_res():
    '''Get all the query and response'''
    return jsonify( [c.serialize() for c in arr_query] )


# doctor to customer 


@api.route('/api/sendrestoquery/<int:query_id>',methods=["POST"])
@cross_origin()
def send_response_toquery(query_id):
    '''Add the response to query'''
    data=request.form.to_dict()
    requestdata1=Updatequery(
        query_id=query_id,
        doctor_name=data['doctor_name'],
        email=data['email'],
        mobile=data['mobile'],
        respond_to_query=data['respond_to_query']
    )
    arr_query.append(requestdata1)
   
    return make_response(jsonify({'message':'request sent'}),201)



