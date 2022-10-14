from .CRUD import Crud
import uuid

class Folder(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'folder')

    def new(self, client_id):
        folder_id = str(uuid.uuid4())
        self.id = f"{client_id}/{folder_id}"
        return [True, {}, None]

    def edit(self, name, conterpart, autrepartie, associate, price):
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
        return self._push(data)
