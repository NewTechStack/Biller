from .CRUD import Crud

class User(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'user')

    def edit(self, first_name, last_name, email, phone, image, price, index):
        data = {
            'id': self.id
        }
        if first_name is not None:
            data['first_name'] = first_name
        if last_name is not None:
            data['last_name'] = last_name
        if email is not None:
            data['email'] = email
        if phone is not None:
            data['phone'] = phone
        if image is not None:
            data['image'] = image
        if price is not None:
            data['price'] = price
        if index is not None:
            data['index'] = index
        if extra is not None:
            data['extra'] = extra
        return self._push(data)
