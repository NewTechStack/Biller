from .CRUD import Crud
import uuid

class Folder(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'folder')

    def new(self, client_id):
        folder_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}"
        return [True, {}, None]

    def edit(self, name, conterpart, autrepartie, associate, price, user_in_charge, user_in_charge_price, extra):
        data = {
            'id': self.id
        }
        if name is not None:
            data['name'] = name
        if conterpart is not None:
            data['conterpart'] = conterpart
        if autrepartie is not None:
            data['autrepartie'] = autrepartie
        if associate is not None:
            data['associate'] = associate
        if price is not None:
            data['price'] = price
        if user_in_charge is not None:
            data['user_in_charge'] = user_in_charge
        if user_in_charge_price is not None:
            data['user_in_charge_price'] = user_in_charge_price
        if extra is not None:
            data['extra'] = extra
        return self._push(data)
