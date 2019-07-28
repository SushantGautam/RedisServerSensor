import json
import binascii
from ast import literal_eval as make_tuple
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.views.decorators.clickjacking import xframe_options_exempt

from webViz.models import PySensorData
from webViz.reciever import decrypteddata


@xframe_options_exempt
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "BoothMasterSocket"
        self.room_group_name = 'booth_updates'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

        '''async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "refreshall",
                'boothname': "boothmaster",

            }
        ) '''

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, ):
        text_data_json = json.loads(text_data)
        message1 = text_data_json['message']
        decdata = binascii.unhexlify(message1)
        decrypt_message = decrypteddata(decdata)
        data_tuple = make_tuple(decrypt_message.decode())
        message = data_tuple

        #
        # "DateTime"
        # "Latitude"
        # "Longitude"
        # "Temperature_F"
        # "RelativeHumidity"
        # "LPG_PPM"
        # "CO_PPM"
        # "Smoke_PPM"
        # "Pressure_hPa"
        # "Altitude_m"
        # "PM_25"

        dataObj = PySensorData.objects.using("serveo-server").create(Latitude=message[2] / 100,
                                                                     Longitude=message[3] / 100,
                                                                     Temperature_F=message[0],
                                                                     RelativeHumidity=message[1],
                                                                     LPG_PPM=message[4],
                                                                     CO_PPM=message[5],
                                                                     Smoke_PPM=message[6],
                                                                     Pressure_hPa=message[7]/100,
                                                                     Altitude_m=message[8],
                                                                     PM_25=message[9]).save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        temp = message[0]
        hum = message[1]
        lat = (message[2] / 100)
        lon = message[3] / 100
        lpg = message[4]
        co = message[5]
        smoke = message[6]
        pressure = message[7]/100
        altitude = message[8]
        particulate = message[9]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'temp': temp,
            'hum': hum,
            'lat': lat,
            'lon': lon,
            'lpg': lpg,
            'co': co,
            'somke': smoke,
            'pressure': pressure,
            'altitude': altitude,
            'particulate': particulate,
            'ifsuccess': 'success',
        }))
