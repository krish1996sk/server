from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)

Devices = {
    'device1': {'status': 'good with all interfaces working'},
    'device2': {'status': 'hard disk failure'},
    'device3': {'status': 'good'},
    'device4': {'status': 'RPD not working'},
    'device5': {'status': 'Router broken'}
}

Devices = json.load(open(Devices.json))


def abort_if_device_doesnt_exist(device_id):
    if device_id not in Devices:
        abort(404, message="Device {} doesn't exist".format(device_id))

parser = reqparse.RequestParser()
parser.add_argument('status')


class Device(Resource):
    def get(self, device_id):
        abort_if_device_doesnt_exist(device_id)
        return Devices[device_id]

    def delete(self, device_id):
        abort_if_device_doesnt_exist(device_id)
        del Devices[device_id]
        with open('Devices.json', 'w') as f:
            json.dump(Devices, f, indent=2)
        return '', 204

    def put(self, device_id):
        args = parser.parse_args()
        task = {'status': args['status']}
        Devices[device_id] = task
        with open('Devices.json', 'w') as f:
            json.dump(Devices, f, indent=2)
        return task, 201


class DeviceList(Resource):
    def get(self):
        return jsonify(Devices)

    def post(self):
        args = parser.parse_args()
        device_id = int(max(Devices.keys()).lstrip('device')) + 1
        device_id = 'device%i' % device_id
        Devices[device_id] = {'status': args['status']}
        with open('Devices.json', 'w') as f:
            json.dump(Devices, f, indent=2)
        return Devices[device_id], 201

api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<device_id>')


if __name__ == '__main__':
    app.run(debug=True)
