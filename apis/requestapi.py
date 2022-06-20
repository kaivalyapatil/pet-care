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
    '''For Sending the request parameters these are required
 
 Parameters:

    request_id : int
            Request id
    fullname   : str
            Name of the person who wants to send the request
    email      : str
            Person emailID
    mobile     : str
            Person mobile no
    address    : str
            Person Address
    city       :
            Person city
    pincode    :str
            Person city pincode it must be unique
    pet_catagory:str
            Which type of Animal, Dog,Cat etc.
    pet_age     :str
            pet Age
    pet_gender  :str
            pet gender
    issue_description:str
           if pet is having some medical treament describe here issue 
    image       :str
            share injury pictures
    reports     :str
            share previous medical reports
    
    '''

    
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
   
    '''For Getting the request parameters

    Parameters:

    request_id : int
            Request id
    fullname   : str
            Name of the person who is sending the request to the Docter
    email      : str
            Person emailID
    mobile     : str
            Person mobile no
    address    : str
            Person Address
    city       :
            Person city
    pincode    :str
            Person city pincode it must be unique
    pet_catagory:str
            Which type of Animal, Dog,Cat etc.
    pet_age     :str
            pet Age
    pet_gender  :str
            pet gender
    issue_description:str
           if pet is having some medical treament describe here issue 
    image       :str
            injury pictures
    reports     :str
            previous medical reports

    Returns
    -------
    list
        a list of request receiving to the doctor
    '''

    return jsonify( [c.serialize() for c in arr_request] )

arr_response=[]

@api.route('/api/updaterequest/<int:request_id>',methods=["POST"])
@cross_origin()
def send_res_to_request(request_id):
   
    '''Response back to request providing details of the Doctor

    Parameters:

        request_id: int
            Response revert back to person woh is send the request through requestId
        doctor_name:str
            Name of the Doctor
        email:str
            EmailID of the Doctor
        mobile:str
            Doctor mobile no
        visit_date_time:str
            Appointment Date and time
        fees:str
            Fees they are offered
   
    '''

    data=request.form.to_dict()
    requestdata=Requestresponse(
        request_id=request_id,
        doctor_name=data['doctor_name'],
        email=data['email'],
        mobile=data['mobile'],
        visit_date_time=data['visit_date_time'],
        fees=data['fees']
    )
    arr_response.append(requestdata)
    print(arr_response)
   
    return make_response(jsonify({'message':'response sent to customer'}),201)

@api.route('/api/responselist',methods=["GET"])
@cross_origin()
def get_request():
   
    '''For Getting the response parameters

    Parameters:

    request_id : int
            Request id
    doctor_name   : str
            Name of the doctor 
    email      : str
            Person emailID
    mobile     : str
            Person mobile no
    visit_date_time    : str
            Person visit_date_time
    fees       :
            Person fees
   
    Returns
    -------
    list
        a list of request receiving to the doctor
    '''

    return jsonify( [c.serialize() for c in arr_response] )

# Query

arr_query=[]

@api.route('/api/querysend',methods=['POST'])
def register_query():
    
    '''For Sending the query parameters these are required
 
 Parameters:

    request_id : int
            Request id
    fullname   : str
            Name of the person who wants to send the request
    email      : str
            Person emailID
    mobile     : str
            Person mobile no
    pet_catagory:str
            Which type of Animal, Dog,Cat etc.
    pet_age     :str
            pet Age
    pet_gender  :str
            pet gender
    issue_description:str
           if pet is having some medical treament describe here issue 
    image       :str
            share injury pictures
    reports     :str
            share previous medical reports
    
    '''

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
    return make_response(jsonify({'message':'query sent successfully'}),201)


@api.route('/api/listquery',methods=["GET"])
@cross_origin()
def get_query_res():
    
    '''get all the queries
 
 Parameters:

    query_id : int
            Query id
    fullname   : str
            Name of the person who wants to send the request
    email      : str
            Person emailID
    mobile     : str
            Person mobile no
    pet_catagory:str
            Which type of Animal, Dog,Cat etc.
    pet_age     :str
            pet Age
    pet_gender  :str
            pet gender
    issue_description:str
           write a query if they have 
    image       :str
            share pictures
    reports     :str
            share medical reports
    
    Return
        list
            a list of query related to pet
    '''

    return jsonify( [c.serialize() for c in arr_query] )


# doctor to customer 

arr_queryresponse=[]

@api.route('/api/sendrestoquery/<int:query_id>',methods=["POST"])
@cross_origin()
def send_response_toquery(query_id):
    
    '''Response back to query,providing details of the Doctor

    Parameters:

        query_id: int
            Response revert back to person woh is send the request through query_Id
        doctor_name:str
            Name of the Doctor
        email:str
            EmailID of the Doctor
        mobile:str
            Doctor mobile No
        respond_to_query:str
            Doctor Send the particular solution

   
    '''

    data=request.form.to_dict()
    requestdata1=Updatequery(
        query_id=query_id,
        doctor_name=data['doctor_name'],
        email=data['email'],
        mobile=data['mobile'],
        respond_to_query=data['respond_to_query']
    )
    arr_queryresponse.append(requestdata1)
    
    return make_response(jsonify({'message':'response to query sent successfully'}),201)



@api.route('/api/listquery',methods=["GET"])
@cross_origin()
def get_query_res():
    
    '''get all the queries
 
 Parameters:

    query_id : int
            query_id id
        doctor_name:str
            Name of the Doctor
        email:str
            EmailID of the Doctor
        mobile:str
            Doctor mobile No
        respond_to_query:str
            Doctor Send the particular solution

    Return
        list
            a list of query response from doctor to customer
    '''

    return jsonify( [c.serialize() for c in arr_queryresponse] )