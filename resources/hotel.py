from flask_restful import Resource,reqparse
from models.hotel import hotelModel
from flask_jwt_extended import jwt_required

hoteis = [
    {"hotel_id": 'paraiso', "nome": 'Hotel Paraiso', "estrelas": 4.8, "diaria": 125.75, "cidade": 'Porto'},
    {"hotel_id": 'fukui', "nome": 'Fukui Paradise', "estrelas": 4.9, "diaria": 225.75, "cidade": 'Lisboa'},
    {"hotel_id": 'saint', "nome": 'Resort Saint', "estrelas": 4.3, "diaria": 165.75, "cidade": 'Coimbra'}
]

class Hoteis(Resource):
    parametros = reqparse.RequestParser()
    parametros.add_argument("cidade", type=str, default="", location="args")
    parametros.add_argument("estrelas_min", type=float, default=0, location="args")
    parametros.add_argument("estrelas_max", type=float, default=0, location="args")
    parametros.add_argument("diaria_min", type=float, default=0, location="args")
    parametros.add_argument("diaria_max", type=float, default=0, location="args")
    parametros.add_argument("itens", type=int, default=5, location="args")
    parametros.add_argument("pagina", type=int, default=1, location="args")

    def get(self):
        meus_filtros = Hoteis.parametros.parse_args()
        query = hotelModel.query

        if meus_filtros["cidade"]:
            query = query.filter(hotelModel.cidade == meus_filtros ["cidade"])

        if meus_filtros["estrelas_min"]:
                    query = query.filter(hotelModel.estrelas == meus_filtros ["estrelas_min"])

        if meus_filtros["estrelas_max"]:
                    query = query.filter(hotelModel.estrelas == meus_filtros ["estrelas_max"])

        if meus_filtros["diaria_min"]:
                    query = query.filter(hotelModel.diaria == meus_filtros ["diaria_min"])

        if meus_filtros["diaria_max"]:
                    query = query.filter(hotelModel.diaria == meus_filtros ["diaria_max"])

        page = meus_filtros["pagina"]
        num_hoteis_por_pagina = meus_filtros["itens"]
        pagination = query.paginate(page=page, per_page=num_hoteis_por_pagina, error_out=False)


        resultado_hotel = [hotel.json() for hotel in pagination.items]

        return {
            "hoteis": resultado_hotel,
            "qtde_items": pagination.total,
            "qtde_paginas": pagination.pages,
            "pagina_atual": page
            }


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome",type=str, required = True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas",type=float, required = True, help="As estrelas do hotel são obrigatório")
    argumentos.add_argument("diaria",type=float, required = True, help="A diaria do hotel é obrigatória")
    argumentos.add_argument("cidade",type=str, required = True, help="A cidade do hotel é obrigatório")
    
    def get(self, hotel_id):
        hotel = hotelModel.find_hotel(hotel_id) #Devolve o hotel ou devolve None
        if hotel is not None:
                return hotel.json(), 200
        return  { "mensagem": "Hotel não foi encontrado"}


    @jwt_required()
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        hotel = hotelModel.find_hotel(hotel_id)

        if hotel is not None:
              return { "mensagem": "Hotel com este id já existe" }

        try:
            novo_hotel = hotelModel(hotel_id, **dados)
            novo_hotel.save_hotel()
            return hotel.json(),200
        except:
            return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500

        
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        
        #Se o hotel ID existe
        hotel = hotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                lista = [dado for dado in dados.values()]
                hotel.update_hotel(*lista)
                hotel.save_hotel()
                return hotel.json(),200
            except:
                return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500


    @jwt_required()
    def delete(self,hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        novo_hotel = hotelModel(hotel_id, **dados)

        hotel = hotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                novo_hotel.delete_hotel()
                return hotel.json(),200
            except:
                return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500
        return {"Mensagem": "Hotel não encontrado"},404