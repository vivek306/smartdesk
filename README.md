smartdesk
=========

Converting the custom made lap-desk into a smart desk using the Raspberry pi running raspBMC and  controlling its various features via Dataplicity

![alt tag](https://raw.githubusercontent.com/vivek306/smartdesk/master/images/SetupEffects.jpg)

<h3>
initial setup
</h3>

<b>intall raspBMC</b> (http://www.raspberrypi.org/downloads/) into your SD Card (there are various ways to do it and if you are a Mac user I would strongly recommend using Pi Filler (http://ivanx.com/raspberrypi/) 


<b>install Dataplicity</b> (http://dataplicity.com/get-started/), it is an amazing free tool for devs to control Raspberry pi online

<h3>
SSH into the raspBMC
</h3>

The most efficient way to get into the command line for raspBMC OS is to SSH it (http://www.raspbmc.com/wiki/user/using-ssh/)

Once you login your screen should say something like  

<b>pi@raspbmc :</b>

There is a great tutorial for Rasbian OS (http://dataplicity.com/get-started/raspberry-pi/), but for RaspBMC there are some minor changes 

<h4>1 - 'Prep the pi'</h4>

Just before 'Install the dataplicity examples' you got to sudo install git and ssl certificates

<b>sudo apt-get install git-core</b>  
<b>sudo apt-get install ca-certificates</b> (more details on ssl can be found here https://help.ubuntu.com/community/OpenSSL)

<h4>3 - 'Register hardware'</h4>

<b>sudo dataplicity init -u USERNAME -p PASSWORD</b> initializes the dataplicity Core  

Now in raspBMC '~/' = /home/pi/  
to avoid this confusion quickly do a 'ls -la' to list all files, by default it should be  
/home/pi/dataplicity/dataplicity/examples/sinewave

<h4>5 - 'Hotting up'</h4>  

<b>'vi' editor</b> should be present by default to edit text files  
<b>sudo vi dataplicity.conf</b> will get you into the file as admin. Press 'i' to edit the file and once completed press 'Esc' followed by 'Shift + zz" to save and close the file  

To create a new file with 'vi' just go  
<b>'sudo vi pitest.py'</b>

<h4>You should now have some grip of Dataplicity and the RaspBMC, next is to install Fusion</h4>
There are many tutorials for this, I personally followed this  
http://www.youtube.com/watch?v=EA6A-YwpaSI  

<h4>Great, now the Pi should be on Steroids breathing fire</h4>
Just to make sure everything is fine, go to Music->Music Addons and look for "Radio" Plugin (If it is missing see if you can find it in "Get More" and if you still can't find it make sure you followed the fusion tutorial properly) 


<h3>Smart-Desk, Sapota 1.0 Beta</h3>
![alt tag](https://raw.githubusercontent.com/vivek306/smartdesk/master/images/Sapota%20Small.png)

I have only tested this on nBox Skin (It is the sexiest of all!!), System->System->Skin and install nBox  

<h4>Install and Run Sapota 1.0 Beta</h4>
Log back into the SSH  
Sapota requires <b>XBMC Client</b>  
<b>sudo pip install xbmc-json</b> https://github.com/jcsaaddupuy/python-xbmc this is a great tool for controlling the raspBMC via JASON Rest based calls

Navigate into dataplicity examples  
<b>cd dataplicity/dataplicity/examples</b>  

Git Clone the Smart Desk  
<b>git clone https://github.com/vivek306/smartdesk.git</b>

To Run the Smart Desk  
<b>sudo dataplicity run</b> inside the Smartdesk folder and to stop "Ctrl+c"  

Now Go to your dataplicity account and you should see my/Smart Desk/"Weird Numbers"/"Yor Device with Weird Numbers" click it  
![alt tag](https://github.com/vivek306/smartdesk/blob/master/images/SmartDesk%20Sapota%201.0%20Control%20Panel.png)  

Now "Check" - <b>Relax</b> and Click "Play Music", you should see   
![alt tag](https://raw.githubusercontent.com/vivek306/smartdesk/master/images/Sapota%201.0.png)  

<b>Please note that polling happens once every 60 secs and hence the music will take some time to play, feel free to poll it every second</b>  

<h4>Credits</h4>

<b>Essa Saulat</b> (Helped me build Custom Case for the Raspberry Pi with the help of http://squareitround.co.uk/Resources/Punnet_net_Mk1.pdf")  
![alt tag](https://raw.githubusercontent.com/vivek306/smartdesk/master/images/SmartDesk%20Pi.png)  

<b>Essa Saulat and Riham Satti<b> (Helped me name the the software Sapota :D)



