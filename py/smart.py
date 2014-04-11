from dataplicity.client.task import Task, onsignal

import socket
import fcntl
import struct
from xbmcjson import XBMC


def get_rpi_temperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
         temperature = float(f.read()) / 1000.0
    return temperature

class NetworkSettings(Task):
    def pre_startup(self):
        """Called prior to running the project"""
        # self.conf contains the data- constants from the conp
        self.sampler = self.conf.get('sampler')
        global ip
        ip = self.get_ip_address('eth0')
        print ip

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
        )[20:24])


    @onsignal('settings_update', 'my')
    def on_settings_update(self, name, settings):
        """Catches the 'settings_update' signal for 'my'"""
        # This signal is sent on startup and whenever settings are changed by the server
        self.code = settings.get_float(self.sampler, 'code', 1.0)
        print 'I am the network code ',  self.code
   
    def poll(self):
	"""Called on a schedule defined in dataplicity.conf"""
        #Login with default xbmc/xbmc credential
        url = 'http://' + ip + '/jsonrpc'
        xbmc = XBMC(url)
        xbmc.Input.Up()
	self.do_sample(get_rpi_temperature())
       
    def do_sample(self, value):
        self.client.sample_now(self.sampler, value)

