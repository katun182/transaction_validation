from decimal import getcontext, Decimal
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HextoDecimal(Resource):
    def get(self, hexvalue):
        return {"Decimal Value" : int(hexvalue, 16)}

class ChattyVerification(Resource):
    def post(self):
        data_to_verify = request.get_json()
        if(data_to_verify['sender']['previousETH'] == data_to_verify['sender']['currentETH']):
            return {'message':'Unsuccessful Trasaction!'}, 403
        else:
            gas_used= (int(data_to_verify['gasUSED'], 16)/100000000)
            if(data_to_verify['sender']['currentETH']+(gas_used)+data_to_verify['sender']['transferredETH']==data_to_verify['sender']['previousETH']):
                if(data_to_verify['sender']['previousCHT']-data_to_verify['sender']['currentCHT'] == data_to_verify['receiver']['currentCHT']-data_to_verify['receiver']['previousCHT'] == data_to_verify['transferredCHT']):
                    return {'message': 'Verification Success!'}, 200
            else:
                return {'message':'Verification Failed!'}

class EtherVerification(Resource):
    def post(self):
        data_to_verify = request.get_json()

        gas_used = (int(data_to_verify['gasUSED'], 16))/10000000

        actual_gas=data_to_verify['sender']['previousETH']-data_to_verify['sender']['currentETH']-data_to_verify['transferredETH']

        receiver_wallet = data_to_verify['receiver']['currentETH'] - data_to_verify['receiver']['previousETH']

        if(round(actual_gas,15) == gas_used):
            if(round(receiver_wallet,15) == data_to_verify['transferredETH']):
                return {'message':'Verification Success!'}
        else:
            return {'message':'Verification Failed!'}

        return {'message':'check print!'}

api.add_resource(HextoDecimal, '/verify/<string:hexvalue>')
api.add_resource(ChattyVerification, '/verifyCHT')
api.add_resource(EtherVerification, '/verifyETH')

app.run(port=5000, debug=True)