from .CRUD import Crud
import uuid

class Bank(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'bank')
    
    def new(self):
        self.id = str(uuid.uuid4())
        return [True, {}, None]

    def edit(self, internal_name, name, benef, iban, clearing, bic, bank_type):
        data = {
            'id': self.id
        }
        if internal_name is not None:
            data['internal_name'] = internal_name
        if name is not None:
            data['name'] = name
        if benef is not None:
            data['benef'] = benef
        if iban is not None:
            data['iban'] = iban
        if clearing is not None:
            data['clearing'] = clearing
        if bic is not None:
            data['bic'] = bic
        if bank_type is not None:
            if not isinstance(bank_type, list) or any([x not in ["provision", "invoice"] for x in bank_type]):
                return [False, "type should be a list of ['provision', 'invoice']", 400]
            data['type'] = bank_type
        return self._push(data)
