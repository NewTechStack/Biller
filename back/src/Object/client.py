from .CRUD import Crud
import uuid

class Client(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'client')

    def new(self):
        self.id = str(uuid.uuid4())
        return [True, {}, None]

    def edit(self, type, name_1, name_2, email, phone, adresse, lang, extra = None):
        data = {
            'id': self.id
        }
        if type is not None:
            data['type'] = type
        if name_1 is not None:
            data['name_1'] = name_1
        if name_2 is not None:
            data['name_2'] = name_2
        if email is not None:
            data['email'] = email
        if phone is not None:
            data['phone'] = phone
        if adresse is not None:
            data['adresse'] = adresse
        if lang is not None:
            data['lang'] = lang
        if extra is not None:
            data['extra'] = extra
        return self._push(data)
