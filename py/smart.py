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
	self.option = settings.get('music', 'option')
	self.addon = settings.get('music', 'addon')
	self.category = settings.get('music', 'category')
	self.relax_volume = settings.get_float('music-relax', 'volume', 1.0)
	self.relax_activate = settings.get_float('music-relax','activate', 1.0)
	self.relax_type = settings.get('music-relax', 'type')
	self.relax_station = settings.get('music-relax','station')
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
		if self.relax_activate == 1:
			self.play_relaxed_music(xbmc, ip)
		elif self.relax_activate == 0:
			self.stop_music(xbmc, ip)

    def play_relaxed_music(self, xbmc, ip):
	xbmc.Application.SetVolume({"volume": self.relax_volume})
	self.set_default_settings(xbmc, ip)
        self.goto_goal(xbmc, ip, self.relax_type)
        print "I am in " + self.relax_type
        self.goto_goal(xbmc, ip, self.relax_station)
        print "I am playing " + self.relax_station

    def stop_music(self, xbmc, ip):
	print 'Stopping player'
	xbmc.Player.Stop({"playerid":0})
	xbmc.GUI.ActivateWindow(window="home")

    def set_default_settings(self, xbmc, ip):
	#show notification
	xbmc.GUI.ShowNotification({"title":"Smartdesk", "message":ip})
        time.sleep(5)
        self.goto_music(xbmc, ip)
        print "I am in music, looking for " + self.option
        required = self.option
        self.goto_goal(xbmc, ip, required)
        print "I am in " + self.option
        time.sleep(5)
        required = self.addon
        self.goto_goal(xbmc, ip, required)
        print "I am in " + self.addon
        time.sleep(10)
        required = self.category
        self.goto_goal(xbmc, ip, required)
        print "I am in " + self.category
        time.sleep(10)

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
   		try:
			acquired = get_xbmc_label(ip)["result"]["ListItem.Label"].encode('ascii','ignore')
		except:
			acquired = "Don't bother"

    def goto_goal(self, xbmc, ip, required):
    	print required
	try:
		acquired = get_xbmc_label(ip)["result"]["ListItem.Label"].encode('ascii','ignore')
	except:
		acquired = "Don't bother"
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
        CPU_usage = float(getCPUuse())
	print CPU_usage, get_rpi_temperature()
        self.do_sample(CPU_usage)

    def do_sample(self, value):
        self.client.sample_now(self.sampler, value)

