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

