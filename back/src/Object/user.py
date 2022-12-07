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
    
    def nointerest_add(folder_id):
        data = self.get()
        if data is None:
            return [False, "Invalid user", 404]
        if not "no_interest" in data:
            data["no_interest"] = []
        data["no_interest"].append(folder_id)
        return self._push(data)
    
    def nointerest_delete(folder_id):
        data = self.get()
        if data is None:
            return [False, "Invalid user", 404]
        if not "no_interest" in data:
            data["no_interest"] = []
        if not folder_id in data["no_interest"]:
            return [False, f"folder '{folder_id}'not in no interest list", 404]
        data["no_interest"].remove(folder_id)
        return self._push(data)
