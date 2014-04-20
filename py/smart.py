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

    def set_basic_settings(self, settings):
    	self.code = settings.get_float('connection', 'code', 1.0)
	self.option = settings.get('music', 'option')
	self.addon = settings.get('music', 'addon')
	self.category = settings.get('music', 'category')
	self.relax_volume = settings.get_float('music-relax', 'volume', 1.0)
	self.relax_activate = settings.get('music-relax','activate')
	self.relax_type = settings.get('music-relax', 'type')
	self.relax_station = settings.get('music-relax','station')
	self.happy_volume = settings.get_float('music-happy', 'volume', 1.0)
	self.happy_activate = settings.get('music-happy','activate')
	self.happy_type = settings.get('music-happy', 'type')
	self.happy_station = settings.get('music-happy','station')
	self.sad_volume = settings.get_float('music-sad', 'volume', 1.0)
	self.sad_activate = settings.get('music-sad','activate')
	self.sad_type = settings.get('music-sad', 'type')
	self.sad_station = settings.get('music-sad','station')
	self.annoyed_volume = settings.get_float('music-annoyed', 'volume', 1.0)
	self.annoyed_activate = settings.get('music-annoyed','activate')
	self.annoyed_type = settings.get('music-annoyed', 'type')
	self.annoyed_station = settings.get('music-annoyed','station')
	self.regional_volume = settings.get_float('music-regional', 'volume', 1.0)
	self.regional_activate = settings.get('music-regional','activate')
	self.regional_type = settings.get('music-regional', 'type')
	self.regional_station = settings.get('music-regional','station')

    @onsignal('settings_update', 'smartdesk')
    def on_settings_update(self, name, settings):
        """Catches the 'settings_update' signal for 'smartdesk'"""
        # This signal is sent on startup and whenever settings are changed by the server
  	self.set_basic_settings(settings)
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
		# Play music station
		self.select_music_station(xbmc, ip)

    def select_music_station(self, xbmc, ip):
    	# Play relaxed music
	if self.relax_activate == "yes":
		self.play_relaxed_music(xbmc, ip)
	# Play happy music
	elif self.happy_activate == "yes":
		self.play_happy_music(xbmc, ip)
	# Play sad music
	elif self.sad_activate == "yes":
		self.play_sad_music(xbmc, ip)
	# Play annoyed music
	elif self.annoyed_activate == "yes":
		self.play_annoyed_music(xbmc, ip)
	# Play regional music
	elif self.regional_activate == "yes":
		self.play_regional_music(xbmc, ip)
	# stop music
	else:
		self.stop_music(xbmc, ip)
    
    def play_relaxed_music(self, xbmc, ip):
	xbmc.Application.SetVolume({"volume": self.relax_volume})
	self.set_default_settings(xbmc, ip)
        self.goto_goal(xbmc, ip, self.relax_type)
        print "I am in " + self.relax_type
        self.goto_goal(xbmc, ip, self.relax_station)
        print "I am playing " + self.relax_station
        
    def play_happy_music(self, xbmc, ip):
	xbmc.Application.SetVolume({"volume": self.happy_volume})
	self.set_default_settings(xbmc, ip)
        self.goto_goal(xbmc, ip, self.happy_type)
        print "I am in " + self.happy_type
        self.goto_goal(xbmc, ip, self.happy_station)
        print "I am playing " + self.happy_station

    def play_sad_music(self, xbmc, ip):
	xbmc.Application.SetVolume({"volume": self.sad_volume})
	self.set_default_settings(xbmc, ip)
        self.goto_goal(xbmc, ip, self.sad_type)
        print "I am in " + self.sad_type
        self.goto_goal(xbmc, ip, self.sad_station)
        print "I am playing " + self.sad_station
        
    def play_annoyed_music(self, xbmc, ip):
	xbmc.Application.SetVolume({"volume": self.annoyed_volume})
	self.set_default_settings(xbmc, ip)
        self.goto_goal(xbmc, ip, self.annoyed_type)
        print "I am in " + self.annoyed_type
        self.goto_goal(xbmc, ip, self.annoyed_station)
        print "I am playing " + self.annoyed_station
        
    def play_regional_music(self, xbmc, ip):
	xbmc.Application.SetVolume({"volume": self.regional_volume})
	self.set_default_settings(xbmc, ip)
        self.goto_goal(xbmc, ip, self.regional_type)
        print "I am in " + self.regional_type
        self.goto_goal(xbmc, ip, self.regional_station)
        print "I am playing " + self.regional_station

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

