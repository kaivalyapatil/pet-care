#as a owner to customer
class Updatequery:
    request_id:int =0
    doctor_name:str=""
    email:str=""
    mobile:str=""
    respond_to_query:str=""
    

    def __init__(self,request_id:int, doctor_name:str,email:str,mobile:str,respond_to_query:str)->None:
        self.request_id=request_id
        self.doctor_name=doctor_name
        self.email=email
        self.mobile=mobile
        self.respond_to_query=respond_to_query
        
    def serialize(self) -> any:
        return {
            'request_id':self.request_id,
            'doctor_name':self.doctor_name,
           'email':self.email,
            'mobile':self.mobile,
            'respond_to_query':self.respond_to_query
           
        }