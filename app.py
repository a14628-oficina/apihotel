#venv é .venv/bin/activate | é um ambiente de trabalho virtual/maquina virtual
from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.user import user
from resources.user import userRegister
from resources.user import userLogin
from resources.user import userLogout
from con_sql_alchemy import bd
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from datetime import timedelta



app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)       # Inicializa o JWT para dizer que estou a trabalhar na minha API

#Configurações
#SQLITE não se utiliza em base de dados
#Foi utilizada agora por ser apenas um teste
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hoteis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "a_minha_chave_secreta_longa_e_intransmissivel"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)



@jwt.token_in_blocklist_loader
def verifica_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST


@jwt.revoked_token_loader
def token_invalido(jwt_header, jwt_payload):
    return { "mensagem": "Logout efetuado! Faça login para aceder novamente!"}

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")
api.add_resource(user, "/users/<string:username>")
api.add_resource(userRegister,"/registar")
api.add_resource(userLogin, "/login")
api.add_resource(userLogout, "/logout")

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all() #Cria todas as tabelas definidas no modelo do SQLAlchemy
    app.run(debug=True)