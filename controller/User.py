# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import hashlib, base64, json,jwt

from config import app_config, app_active
from model.User import User
from controller.Email import EmailController

config = app_config[app_active]


class UserController:
    def __init__(self):
        self.user_model = User()
        self.email_controller = EmailController()

    def verify_auth_token(self, access_token):
        status = 401

        try:
            jwt.decode(access_token, config.SECRET, algorithms="HS256")

            message = "Token válido"
            status = 200
        except jwt.ExpiredSignatureError:
            message = "Token expirado, realize um novo login"
        except:
            message = "Token inválido"

        return {
            "message": message,
            "status": status
        }

    def generate_auth_token(self, data, exp=30, time_exp=False):
        if time_exp:
            date_time = data["exp"]
        else:
            date_time = datetime.utcnow() + timedelta(minutes=exp)

        dict_jwt = {
            "id": data["id"],
            "username": data["username"],
            "exp": date_time
        }
        access_token = jwt.encode(dict_jwt, config.SECRET, algorithm="HS256")

        return access_token
    
    def get_user_by_id(self, user_id):
        try:
            self.user_model.id = user_id
            res = self.user_model.get_user_by_id()

            result = {
                "id": res.id,
                "name": res.username,
                "email": res.email,
                "date_created": res.date_created
            }
            status = 200
        except Exception as e:
            result = []
            status = 400
            print(e)
        finally:
            return {
                "result": result,
                "status": status
            }

    def get_admin_login(self, user_id):
        self.user_model.id = user_id

        response = self.user_model.get_user_by_id()

        return response

    def login(self, email, password):
        # pega os dados de e-mail e salva no atributo da model de usuário.
        self.user_model.email = email

        # Verifica se o usuário existe no banco de dados
        result = self.user_model.get_user_by_email()

        # Caso o usuário exista o result não será None
        if result is not None:
            # Verifica se o password que o usuário enviou, agora convertido em hash, é igual ao password que foi pego
            # no banco de dados para esse usuário.
            res = self.user_model.verify_password(password, result.password)

            # se for o mesmo retornará True
            if res:
                return result
            else:
                return {}
        return {}

    def recovery(self, to_email):
        self.user_model.email = to_email
        res = self.user_model.get_user_by_email()

        if res is not None:
            user_id = res.id
            username = res.username
            recovery_code = self.generate_auth_token({
                "id": user_id,
                "username": username
            }, exp=5)
            # recovery_code = jwt.decode(recovery_code, config.SECRET, algorithm='HS256')

            try:
                self.user_model.id = user_id
                res = self.user_model.update({
                    "recovery_code": recovery_code
                })

                if res:
                    content_text = "Olá %s. Para realizar a alteração de senha, você precisa acessar a seguinte url: %snew-password/%s" % (username, config.URL_MAIN, recovery_code)
                else:
                    return {
                        "status_code": 401,
                        "body": "Erro ao gerar código de envio"
                    }
            except:
                return {
                    "status_code": 401,
                    "body": "Erro ao gerar código de envio"
                }

            try:
                result = self.email_controller.send_email(to_email, "Recuperação de senha", content_text)
            except:
                return {
                    "status_code": 401,
                    "body": "Erro no serviço de e-mail. Por favor, entre em contato com o administrador."
                }
        else:
            result = {
                "status": 401,
                "body": "Usuário inexistente"
            }

        return result

    def get_user_by_recovery(self, recovery_password):
        self.user_model.recovery_code = recovery_password

        return self.user_model.get_user_by_recovery()

    def new_password(self, user_id, password):
        self.user_model.set_password(password)
        self.user_model.id = user_id

        return self.user_model.update({
            "password": self.user_model.password
        })
