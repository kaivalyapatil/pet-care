
class Query:
    query_id:int =0
    fullname:str=""
    email:str=""
    mobile:str=""
    pet_catagory:str=""
    pet_age:str=""
    pet_gender:str=""
    issue_description:str=""
    image:str=""
    reports:str=""

    def __init__(self,query_id:int, fullname:str,email:str,mobile:str,pet_catagory:str,pet_age:str,pet_gender:str,issue_description:str,image:str,reports:str)->None:
        self.query_id=query_id
        self.fullname=fullname
        self.email=email
        self.mobile=mobile
        self.pet_catagory=pet_catagory
        self.pet_age=pet_age
        self.pet_gender=pet_gender
        self.issue_description=issue_description
        self.image=image
        self.reports=reports
   
    def serialize(self) -> any:
        return {
            'query_id':self.query_id,
            'fullname':self.fullname,
           'email':self.email,
            'mobile':self.mobile,
            'pet_catagory':self.pet_catagory,
            'pet_age':self.pet_age,
            'pet_gender':self.pet_gender,
            'issue_description':self.issue_description,
            'image':self.image,
            'reports':self.reports
        }