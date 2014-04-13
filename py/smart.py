from dataplicity.client.task import Task, onsignal

import time
import json
import os
import socket
import fcntl
import struct
import urllib2
from xbmcjson import XBMC

# CPU Usage
# Return % of CPU used by user as a character string
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Temperature information
def get_rpi_temperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
         temperature = float(f.read()) / 1000.0
    return temperature

# XBMC Label information
def get_xbmc_label(ip):
    print "My get label ip is " + ip
    json_result = urllib2.urlopen("http://" + ip + "/jsonrpc?request={%22jsonrpc%22:%222.0%22,%22method%22:%22XBMC.GetInfoLabels%22,%22params%22:%20{%20%22labels%22:%20[%22Container.Viewmode%22,%20%22ListItem.Label%22,%20%22Control.GetLabel(501)%22,%20%22Container.NumItems%22,%20%22Container.Position%22,%20%22Container.ListItem(-1).Label%22,%20%22Container.ListItem(1).Label%22%20]%20},%20%22id%22:1}").read()
    xbmc_info = json.loads(json_result)
    return xbmc_info

def get_xbmc_main_label(ip):
    print "My get label ip is " + ip
    json_result = urllib2.urlopen("http://" + ip + "/jsonrpc?request={%22jsonrpc%22:%222.0%22,%22method%22:%22GUI.GetProperties%22,%22params%22:{%22properties%22:[%22currentwindow%22]},%20%22id%22:%201}").read()
    xbmc_info = json.loads(json_result)
    return xbmc_info["result"]["currentwindow"]["label"]

class NetworkSettings(Task):
    def pre_startup(self):
        """Called prior to running the project"""
        # self.conf contains the data- constants from the conp
        self.sampler = self.conf.get('sampler')

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
        )[20:24])

    @onsignal('settings_update', 'smartdesk')
    def on_settings_update(self, name, settings):
        """Catches the 'settings_update' signal for 'smartdesk'"""
        # This signal is sent on startup and whenever settings are changed by the server
        self.code = settings.get_float('connection', 'code', 1.0)
	ip = "No Connection"
	if int(self.code) < 11:
		print 'Disabling networks'
	elif int(self.code) < 21:
		try:
		    print 'Enabling wireless mode'
		    ip = self.get_ip_address('wlan0')
		except:
		    ip = "No Connection"
	elif int(self.code) < 31:
		try:
		    print 'Enabling ethernet mode'
		    ip = self.get_ip_address('eth0')
		except:
		    ip = "No Connection"
	print 'I am the network code', ip,  self.code
	# Notify the user if network ip is detected
   	if ip != "No Connection":
		required = ""
		xbmc = self.login_xbmc(ip)
		# Show notification
		xbmc.GUI.ShowNotification({"title":"Smartdesk", "message":ip})
		time.sleep(5)
		self.goto_music(xbmc, ip)
		print "I am in music"
		required = "Music Add-ons"
		self.goto_goal(xbmc, ip, required)
		print "I am in music addons"
	 	time.sleep(5)
		required = "Radio"
		self.goto_goal(xbmc, ip, required)
		print "I am in radio"
		time.sleep(10)
		required = "Browse by genre"
		self.goto_goal(xbmc, ip, required)
		print "I am in genre"
		time.sleep(10)
		self.goto_goal(xbmc, ip, "Celtic")
		print "I am in celtic"
		self.goto_goal(xbmc, ip, "Celtic Music Radio")
		print "I am playing celic music station"

    def goto_music(self, xbmc, ip):
	xbmc.GUI.ActivateWindow(window="music")
	# Clear History
	destination = "Home"
	at = get_xbmc_main_label(ip)
	self.auto_pager(xbmc, ip, destination, at)
	xbmc.GUI.ActivateWindow(window="music")

    def auto_pager(self, xbmc, ip, destination, at):
	while (destination != at):
		print "I am at " + at
		xbmc.Input.Back()
 		time.sleep(2)
		at = get_xbmc_main_label(ip)

    def select_xbmc(self, xbmc):
	xbmc.Input.Select()
	time.sleep(5)

    def auto_selector_xbmc(self, xbmc, required, acquired, ip):
	while (required != acquired):
		print "a " + acquired + " r " + required
		xbmc.Input.Down()
		time.sleep(2)
   		acquired = get_xbmc_label(ip)["result"]["ListItem.Label"]

    def goto_goal(self, xbmc, ip, required):
    	print required
	acquired = get_xbmc_label(ip)["result"]["ListItem.Label"]
	time.sleep(2)
	self.auto_selector_xbmc(xbmc, required, acquired, ip)
	self.select_xbmc(xbmc)

    def login_xbmc(self, ip):
  	# Login with default xbmc/xbmc credential
	url = 'http://' + ip + '/jsonrpc'
	xbmc = XBMC(url)
  	return xbmc

    def poll(self):
	"""Called on a schedule defined in dataplicity.conf"""
        CPU_usage = getCPUuse()
	print CPU_usage
        self.do_sample(get_rpi_temperature())

    def do_sample(self, value):
        self.client.sample_now(self.sampler, value)

