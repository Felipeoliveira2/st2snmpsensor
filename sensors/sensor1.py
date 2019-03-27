import eventlet
from easysnmp import Session
from st2reactor.sensor.base import Sensor

class SnmpSensor(Sensor):
    def __init__(self, sensor_service, config):
        super(SnmpSensor, self).__init__(sensor_service=sensor_service, config=config)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = False

    def setup(self):
        pass

    def run(self):
        while not self._stop:
            self._logger.debug('SnmpSensor dispatching trigger...')
        #############################################
            session = Session(hostname='10.224.159.6', community='DataCenter', version=2)

            system_items = session.walk('.1.3.6.1.2.1.25.4.2.1.2')
            payload_result_snmp = {'servicestatus': 0}
            for item in system_items:
                payload_result =  '{value}'.format(value=item.value)
                if payload_result == "nginx":
                    payload_result_snmp =  {'servicestatus': 1}
        #############################################
            self.sensor_service.dispatch(trigger='hello_st2.event1', payload=payload_result_snmp)
            eventlet.sleep(30)

    def cleanup(self):
        self._stop = True

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass