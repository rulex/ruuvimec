#!/usr/bin/env python3

import time
import threading
import bottle
from bottle import route, run, abort
# from ruuvitag_sensor.ruuvitag import RuuviTag
from ruuvitag_sensor.ruuvi import RuuviTagSensor

PORT = 8081
MACS = [
    'C3:2C:69:6E:24:92',
    'F5:BD:73:CE:08:A0',
    'D3:D1:CA:D2:A2:CE',
    'F4:7B:88:90:C5:0A',
    'D5:E8:f5:CB:84:2F',
    'CF:FC:1D:65:2E:98',
]

SENSORS_CACHE = {}

# sensors = {mac: RuuviTag(mac) for mac in MACS}
sensor_lock = threading.Lock()

class RuuviThread(threading.Thread):
    def run(self):
        RuuviTagSensor.get_datas(self.cb, MACS)
        # while True:
            # self._update_tags()
            # time.sleep(10)

    def cb(self, dat):
        try:
            mac = dat[0]
            data = dat[1]
            data['ts'] = time.time()
            SENSORS_CACHE[mac] = data
            print(f'{mac}: {data}')
        except:
            print('whoopsie')


    def _update_tags(self):
        with sensor_lock:
            for mac, sensor in sensors.items():
                sensor.update()
                SENSORS_CACHE[mac] = sensor.state
                SENSORS_CACHE[mac].ts = time.time()
                print("{}: {}".format(mac, sensor.state))

@bottle.get("/")
def index():
    return {mac: sensor for mac, sensor in SENSORS_CACHE.items()}


@bottle.get("/mac")
def get_sensors():
    ret = []
    for mac in SENSORS_CACHE:
        ret.append(mac)
    return {'macs': ret}


@bottle.get("/mac/<mac>")
def get_sensor(mac):
    if mac not in SENSORS_CACHE:
        return abort(404, "Sensor not found")
    return SENSORS_CACHE[mac]


@bottle.get("/test")
def get_test():
    return {'macs': MACS, 'cache': SENSORS_CACHE}


ruuvi_thread = RuuviThread()
ruuvi_thread.start()

run(host="0.0.0.0", port=PORT, debug=True)
#run(host="0.0.0.0", port=PORT)

