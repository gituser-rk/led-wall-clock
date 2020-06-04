import logging
import requests

logging.basicConfig(filename='/opt/led-wall-clock-iobroker/weather.log',level=logging.DEBUG)
# URL's for value retrieval. One value per URL. Requires iobroker.simple-api and iobroker.web adapters

TempOutsideUrl = "http://172.16.1.91:8087/getPlainValue/hm-rpc.0.HEQ0110761.1.TEMPERATURE/" # Sensor Nordseite
TempInsideUrl = "http://172.16.1.91:8087/getPlainValue/hm-rpc.0.OEQ1667692.1.TEMPERATURE/" # Sensor Wohnbereich
HumidityInsideUrl = "http://172.16.1.91:8087/getPlainValue/hm-rpc.0.OEQ1667692.1.HUMIDITY/" # Sensor Wohnbereich
HumidityOutsideUrl = "http://172.16.1.91:8087/getPlainValue/hm-rpc.0.HEQ0110761.1.HUMIDITY/" # Sensor Nordseite


class Weather(object):
    def __init__(self, scheduler, zip, station):
        self._zip = zip
        self._station = station
        self.update()
        # Update every 5 minutes
        scheduler.add_job(self.update, 'cron', minute='*/5')
    def update(self):
        logging.info("Updating ...")
        # HTTP value retrieval:
        try:
            rTempOutside = requests.get(TempOutsideUrl)
            TempOutside = rTempOutside.text
            rTempInside = requests.get(TempInsideUrl)
            TempInside = rTempInside.text
            rHumidityOutside = requests.get(TempOutsideUrl)
            HumidityOutside = rHumidityOutside.text
            rHumidityInside = requests.get(HumidityInsideUrl)
            HumidityInside = rHumidityInside.text
            logging.info("Values sucessfully retrieved")
        #in case of failure write "99" into the variables
        except:
            TempOutside = 99
            TempInside = 99
            HumidityOutside = 99
            HumidityInside = 99
            logging.info("Error in retrieving values - setting all to '99'")
        self.TempOutside = float(TempOutside)
        self.TempInside = float(TempInside)
        self.HumidityOutside = float(HumidityOutside)
        self.HumidityInside = float(HumidityInside)

	
