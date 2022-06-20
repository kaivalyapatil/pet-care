
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
    arr_request.append(addrequest)
    
    binary_file1 = io.BytesIO(file1.read())
    binary_file2 = io.BytesIO(file2.read())
    upload_file(binary_file1,"pet-care-new",secure_filename(file1.filename))
    upload_file(binary_file2,"pet-care-new",secure_filename(file2.filename))

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
    return make_response(jsonify({'message':'request sent'}),201)


@api.route('/list',methods=["GET"])
@cross_origin()
def get_request():
    return jsonify( [c.serialize() for c in arr_request] )


@api.route('/updaterequest/<int:request_id>',methods=["GET","POST"])
@cross_origin()
def send_update_request(request_id):
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
    return make_response(jsonify({'message':'request sent'}),201)

v=[]
@api.route('/listquery',methods=["GET"])
@cross_origin()
def get_query():
    v=jsonify( [c.serialize() for c in arr_query] )
    return v


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
   
    return make_response(jsonify({'message':'request sent'}),201)

d=[]
@api.route('/listquerysol',methods=["GET"])
@cross_origin()
def get_output():
    d=jsonify( ([c.serialize() for c in arr_queryres ]))
    v.append(d)
    return v

