#as a owner to customer
class Requestresponse:
    request_id:int =0
    doctor_name:str=""
    email:str=""
    mobile:str=""
    visit_date_time:str=""
    fees:str=""

    def __init__(self,request_id:int, doctor_name:str,email:str,mobile:str,visit_date_time:str,fees:str)->None:
        self.request_id=request_id
        self.doctor_name=doctor_name
        self.email=email
        self.mobile=mobile
        self.visit_date_time=visit_date_time
        self.fees=fees
   
    def serialize(self) -> any:
        return {
            'request_id':self.request_id,
            'doctor_name':self.doctor_name,
            'email':self.email,
            'mobile':self.mobile,
            'visit_date_time':self.visit_date_time,
            'fees':self.fees,
            
        }