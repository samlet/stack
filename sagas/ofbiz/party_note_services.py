from flask import Flask
from flask import request

from sagas.ofbiz.entities import OfEntity as e
from sagas.ofbiz.services import OfService as s, oc
import datetime

app = Flask(__name__)

@app.route('/notes', methods = ['GET'])
def notes():
    """
    $ curl "http://localhost:5000/notes?_start=1&_limit=5" | json
    :return:
    """
    start = request.args.get('_start', '0', type=int)
    limit = request.args.get('_limit', '10', type=int)
    print("get", start, limit)
    return e('json').listNoteData(_offset=start,_limit=limit), 200

@app.route('/note', methods = ['POST'])
def post_note():
    """
    curl -XPOST -H 'Content-Type: application/json' -d '{"cnt":"bob"}'  http://localhost:5000/note
    :return:
    """
    print("request is json?", request.is_json)
    content = request.get_json()
    note_name = "todo " + str(datetime.datetime.now())
    if 'name' in content:
        note_name=content['name']

    cnt = content['cnt']
    ok, r = s().createPartyNote(partyId='DemoCustomer',
                                noteName=note_name,
                                note=cnt)
    if not ok:
        print(r)
        return 'action fail', 409
    else:
        print('created', r['noteId'])
    return str(r['noteId']), 201

app.run(host='0.0.0.0', port= 5000, debug=True)

