from .CRUD import Crud

class Bank(Crud):
    def __init__(self, id = None):
        super().__init__(id, 'bank')

    def edit(self, internal_name, name, benef, iban, clearing, bic):
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
        return self._push(data)
