import flask
from flask import request, jsonify, render_template
import RunSim

app = flask.Flask(__name__)

values = {'packetGenerator': [],
          'node': [],
          'monitor': []}


@app.route('/run-sim', methods=['POST'])
def runSim():
    node_list = RunSim.test(values)

    return jsonify({'msg': 'Succeed!',
                    'nodes': node_list})


@app.route('/info', methods=['POST'])
def info():
    form = request.form
    if int(form['selector']) <= len(values[form['component']]):
        selector = int(form['selector']) - 1
        component = form['component']
        name = values[component][selector]['name']
        del values[component][selector]

        return jsonify({'msg': 'deleted!',
                        'name': name,
                        'component': component})
    else:
        return jsonify({'pass': 'True'})


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['component'] == "packetGenerator":
            name = request.form['name']
            creation_order = request.form['creation_order']
            componentType = request.form['component']

            for dictElem in values['packetGenerator']:
                if name in dictElem.values():
                    return jsonify({'error': 'Can not be same Packet Generator name.'})

            packetNum = request.form['packetNum']
            arrivalType = request.form['arrivalType']
            arrivalRate = request.form['arrivalRate']
            arrivalRateMax = request.form['arrivalRateMax']
            sizeType = request.form['sizeType']
            sizeRate = request.form['sizeRate']
            sizeRateMax = request.form['sizeRateMax']

            if arrivalType == "Uniform" and sizeType == "Uniform":
                if name and packetNum and arrivalType and arrivalRate and arrivalRateMax and sizeType and sizeRate and sizeRateMax:
                    values['packetGenerator'].append({'componentType': componentType,
                                                      'name': name,
                                                      'creationOrder': creation_order,
                                                      'packetNum': int(packetNum),
                                                      'arrivalType': arrivalType,
                                                      'arrivalRate': int(arrivalRate),
                                                      'arrivalRateMax': int(arrivalRateMax),
                                                      'sizeType': sizeType,
                                                      'sizeRate': int(sizeRate),
                                                      'sizeRateMax': int(sizeRateMax)
                                                      })
                    return jsonify(values['packetGenerator'])
                else:
                    return jsonify({'error': 'Missing Packet Generator Data!'})

            elif sizeType == "Uniform":
                if name and packetNum and arrivalType and arrivalRate and sizeType and sizeRate and sizeRateMax:
                    values['packetGenerator'].append({'componentType': componentType,
                                                      'name': name,
                                                      'creationOrder': creation_order,
                                                      'packetNum': int(packetNum),
                                                      'arrivalType': arrivalType,
                                                      'arrivalRate': int(arrivalRate),
                                                      'arrivalRateMax': None,
                                                      'sizeType': sizeType,
                                                      'sizeRate': int(sizeRate),
                                                      'sizeRateMax': int(sizeRateMax)})
                    return jsonify(values['packetGenerator'])
                else:
                    return jsonify({'error': 'Missing Packet Generator Data!'})

            elif arrivalType == "Uniform":
                if name and packetNum and arrivalType and arrivalRate and arrivalRateMax and sizeType and sizeRate:
                    values['packetGenerator'].append({'componentType': componentType,
                                                      'name': name,
                                                      'creationOrder': creation_order,
                                                      'packetNum': int(packetNum),
                                                      'arrivalType': arrivalType,
                                                      'arrivalRate': int(arrivalRate),
                                                      'arrivalRateMax': arrivalRateMax,
                                                      'sizeType': sizeType,
                                                      'sizeRate': int(sizeRate),
                                                      'sizeRateMax': None
                                                      })
                    return jsonify(values['packetGenerator'])
                else:
                    return jsonify({'error': 'Missing Packet Generator Data!'})

            else:

                if name and packetNum and arrivalRate:
                    values['packetGenerator'].append({'componentType': componentType,
                                                      'name': name,
                                                      'creationOrder': creation_order,
                                                      'packetNum': packetNum,
                                                      'arrivalType': arrivalType,
                                                      'arrivalRate': int(arrivalRate),
                                                      'arrivalRateMax': None,
                                                      'sizeType': sizeType,
                                                      'sizeRate': int(sizeRate),
                                                      'sizeRateMax': None
                                                      })

                    return jsonify(values['packetGenerator'])

                else:
                    return jsonify({'error': 'Missing Packet Generator Data!'})

        elif request.form['component'] == "Node":
            name = request.form['name']
            creation_order = request.form['creation_order']
            componentType = request.form['component']

            for dictElem in values['node']:
                if name in dictElem.values():
                    return jsonify({'error': 'Can not be same node name.'})

            bufferSize = request.form['bufferSize']
            transmissionRate = request.form['transmissionRate']
            source = request.form['source']

            if name and bufferSize and transmissionRate and source:
                values['node'].append({'componentType': componentType,
                                       'name': name,
                                       'creationOrder': creation_order,
                                       'bufferSize': int(bufferSize),
                                       'transmissionRate': int(transmissionRate),
                                       'source': source})

                return jsonify(values['node'])

            else:
                return jsonify({'error': 'Missing Node Data!'})

        elif request.form['component'] == "Monitor":
            name = request.form['name']
            componentToMonitor = request.form['componentToMonitor']
            recordArrival = request.form['recordArrival']
            recordWaiting = request.form['recordWaiting']
            componentType = request.form['component']
            debug = request.form['debug']
            if componentToMonitor and recordArrival and recordWaiting:
                values['monitor'].append({'name': name,
                                          'componentType': componentType,
                                          'componentToMonitor': componentToMonitor,
                                          'recordArrival': recordArrival,
                                          'recordWaiting': recordWaiting,
                                          'debug': debug})

                return jsonify(values['monitor'])

            else:
                return jsonify({'error': 'Missing Monitor Data!'})

        else:
            return jsonify({'error': 'Wrong Form Content'})

    return render_template("index.html")


if __name__ == '__main__':
    app.run()
