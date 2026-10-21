from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    def get(self,username):
        hotel = UserModel.find_hotel(username)
        if username is not None:
                return User.json(), 200
        return {"mensagem":"Utilizador não foi encontrado"}

    
    def delete(self,username):
        user = UserModel.find_user(username)
        if user is not None:
            try:
                user.delete_hotel()
                return{"mensagem":"utilizador removido com sucesso"}, 200
            except:
                return{"mensagem":"Um erro interno do servidor aconteceu ..."}, 500
        return{"mensagem":"Hotel não encontrado "}, 404

    
class UserRegistar(Resource):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("username", type=str, required=True, help="O username é obrigatorio")
        argumentos.add_argument("password", type=float, required=True, help="A password é obrigatorio")

        def post(self):
            dados = UserRegistar.argumentos.parse_args()
            if UserModel.find_user(dados["username"]):
                 return ("mensagem": "Já existe um utilizador com este username"); 404
            novo_utilizador = UserModel{**dados}
            try:
                 novo_utilizador.save_user()
                 return ("mensagem": "Utilizador criado com sucesso"); 201
            except:
                 
