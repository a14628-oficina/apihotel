from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        return{"hoteis":[hotel.json() for hotel in HotelModel.query.all()]}

    
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatorio")
    argumentos.add_argument("estrelas", type=float, required=True, help="estrelas do hotel é obrigatorio")
    argumentos.add_argument("diaria", type=float, required=True, help="Diaria do hotel é obrigatorio")
    argumentos.add_argument("cidade", type=str, required=True, help="Cidade do hotel é obrigatorio")

    
    def get(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
                return hotel.json(), 200
        return {"mensagem":"Hotel não foi encontrado"}

    
    def post(self,hotel_id): 
        
        dados = Hotel.argumentos.parse_args()#Dados é um dicionario
        hotel = HotelModel.find_hotel(hotel_id)#
        if hotel is not None:
            return {"mensagem":f"O hotel com id {hotel_id}ja existe na minha lista"}
        
         
        novo_hotel = HotelModel(hotel_id, **dados)
        try:
            novo_hotel.save_hotel()
            return novo_hotel.json(), 200
        except:
            return{"mensagem":"Um erro interno do servidor aconteceu ..."}, 500

    
    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args()#Dados é um dicionario
        
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                hotel.update_hotel(*dados)
                hotel.save_hotel()
                return hotel.json(), 200
            except:
                return{"mensagem":"Um erro interno do servidor aconteceu ..."}, 500
            
        novo_hotel = HotelModel(hotel_id, **dados)
        try:
            novo_hotel.save_hotel()
            return novo_hotel(), 201
        except:
            return{"mensagem":"Um erro interno do servidor aconteceu ..."}, 500


    def delete(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                hotel.delete_hotel()
                return{"mensagem":"Hotel removido com sucesso"}, 200
            except:
                return{"mensagem":"Um erro interno do servidor aconteceu ..."}, 500
        return{"mensagem":"Hotel não encontrado "}, 404