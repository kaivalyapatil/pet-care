from flask import Flask, jsonify, make_response, request
from flask_cors import CORS


app=Flask(__name__)
cors=CORS(app)
from apis import requestapi

@app.before_request
def before():                                                                                   
    print(f"Request is received in {request.method}-{request.url}")



@app.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({"error":"server error"}),500)

app.register_blueprint(requestapi.get_blueprint())
# app.register_blueprint(queryapi.get_blueprint())





# start the application 

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)