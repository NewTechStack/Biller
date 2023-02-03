import requests
import json
import jwt
import uuid
from tinydb import TinyDB, Query

db = TinyDB('/db.json')
sso_front = "https://sso.rocketbonds.fr"
sso_back = "https://api.sso.rocketbonds.fr"
apitoken = "c36b7c1d813e4839aa111f09784da16b"
registry_id = "89ec2369-35c1-4e0a-a48e-64a4d3ce988f"

class Sso:
    def __init__(self):
        self.apitoken = ""
        self.user = None

    def get_url(self):
        response = requests.request(
            "POST",
            f"{sso_back}/extern/key",
            headers = {
              'Content-Type': 'application/json'
            },
            data = json.dumps(
                {
                  "apitoken": apitoken,
                  "valid_until": 180
                }
            )
        )
        data = json.loads(response.text)
        if not 'data' in data:
            return [False, "Error connecting to sso api", 500]
        data = data['data']
        key = data["key"]
        auth = data["auth"]
        id = str(uuid.uuid4())
        data['id'] = id
        db.insert(data)
        url = f"{sso_front}/sso/extern/{key}/{auth}/accept"
        return [True, {"url": url, "id": id}, None]

    def get_token(self, id):
        r = Query()
        res = db.search(r.id == id)
        db.remove(r.id == id)
        if len(res) != 1:
            return [False, "Invalid id", 404]
        key = res[0]['key']
        secret = res[0]['secret']
        response = requests.request(
            "POST",
            f"{sso_back}/extern/key/{key}/token",
            headers = {
              'Content-Type': 'application/json'
            },
            data = json.dumps(
                {
                  "apitoken": apitoken,
                  "secret": secret
                }
            )
        )
        data = json.loads(response.text)
        token = data['data']['usrtoken']
        ret = self.__decode(token)
        if ret[0] is True:
            ret[1] = data['data']
        return ret

    def verify(self, token):
        res = self.__decode(token, get_data = True)
        if not res[0]:
            return res
        self.user = res[1]["data"]["payload"]
        return [True, {}, None]

    def __decode(self, token, get_data = False, try_serie = 0):
        url = f"{sso_back}/extern/public"
        payload = json.dumps({
          "apitoken": apitoken,
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        public_key = json.loads(response.text)['data']['public_key']
        try:
            public_key = json.loads(response.text)['data']['public_key']
        except:
            if try_serie > 20:
                return [False, "Request delayed", 500]
            return self.__decode(token, get_data, try_serie + 1)
        try:
            data = jwt.decode(
                token,
                public_key,
                leeway=0,
                issuer="auth:back",
                audience=f"auth:{registry_id}",
                algorithms=['RS256']
            )
        except jwt.ExpiredSignatureError:
            return [False, "SSO: Signature expired", 403]
        except jwt.InvalidSignatureError:
            return  [False, "SSO: Invalid signature", 400]
        except jwt.InvalidIssuedAtError:
            return [False, "SSO: Invalid time", 400]
        except jwt.InvalidIssuerError:
            return [False, "SSO: Invalid issuer", 403]
        except jwt.InvalidAudienceError:
            return [False, "SSO: Invalid audience", 401]
        except jwt.ImmatureSignatureError:
            return [False, "SSO: Invalid time", 400]
        except jwt.DecodeError:
            return [False, "SSO: Invalid jwt", 400]
        if get_data == True:
            return [True, {"data": data}, None]
        return [True, {"usrtoken": token}, None, {"usrtoken": token}]

# res = get_url()
# print(res[1]['url'])
# print(get_token(res[1]['id']))
