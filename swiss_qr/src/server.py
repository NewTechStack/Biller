import os
from bottle import route, run, request, response
import json
from qrbill import QRBill
import io

@route('/')
def index():
    return "working"

@route('/generate/svg', 'POST')
def index():
    response.content_type = 'application/json'
    creditor = request.json.get("creditor", {})
    person_mandatory = ["name", "street", "house_num", "pcode",  "country"]
    if any([x not in creditor for x in person_mandatory]) or any([not isinstance(creditor[x], str) for x in person_mandatory]):
        return json.dumps({"svg": None, "error": "creditor"})
    debtor = request.json.get("debtor", {})
    if any([x not in debtor for x in person_mandatory]) or any([not isinstance(debtor[x], str) for x in person_mandatory]):
        return json.dumps({"svg": None, "error": "debtor"})
    language = request.json.get("language", None)
    if language not in ['en', 'de', 'fr', 'it']:
        return json.dumps({"svg": None, "error": "language"})
    currency = request.json.get("currency", None)
    if currency not in ['CHF', 'EUR']:
        return json.dumps({"svg": None, "error": "currency"})
    amount = request.json.get("amount", None)
    if not isinstance(amount, int) and not isinstance(amount, float):
        return json.dumps({"svg": None, "error": "amount"})
    account = request.json.get("account", None)
    if account is None:
        return json.dumps({"svg": None, "error": "account"})
    reference_number = request.json.get("reference_number", None)
    my_bill = QRBill(
                account= account,
                creditor=creditor,
                amount=str(float(amount)),
                currency=currency,
                debtor=debtor,
                additional_information=request.json.get("additional_information", None),
                language=language,
                payment_line=True,
                font_factor=1.0,
            )
    data = io.StringIO()
    my_bill.as_svg(file_out=data, full_page=False)
    svg = data.getvalue().split("\n")[-1].replace("\"", "'")
    data.close()
    return json.dumps({"svg": svg})

run(host='0.0.0.0', port=8080)
