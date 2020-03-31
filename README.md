#Raspberry Pi Water Drop Controller

The idea is to be able to use the raspberry pi as a web interface for quickly dialing in your settings in order to trigger two drop from an electronic solenoid and then trigger the camera as the drops hit the surface of water in the dish below.  This has been implimented in this forked project from [Marcelo Rovai](https://github.com/Mjrovai/RPi-Flask-WebServer.git).  The other inspiration was [David Hunt](http://www.davidhunt.ie/water-droplet-photography-with-raspberry-pi/) who has some code on his webpage that I used as inpiration and a starting point to move forward with this project.  It took longer than I'm willing to admit and the project is a bigger mess than I would like but it is fun to play to see the different pictures that it generates.  I had to take David code and attempt to switch it to scheduled based triggers in order to be able to dynamically update both the shutter timing and second drop timing.  I was somewhat successful however there does seem to be some issues currently still.  I have been able accomplish what I'm looking to do for now so I'm considering the project finished however I do enjoy learning (Programming is not my day job curently) so if you do have constructive suggestion I will be interested in seeing them.

This Project has been challenging but most importantly fun as I have worked my through the issues.  If you end up using it for something it would be fun to hear about it.

Current set-up is about a meter above the surface that I'm dropping drops into but timing can be adjusted somewhat to a bit higher or bit lower depedning on that you have.

As far as hardware it set-up similar to what David has described on his blog.  I did however buy a relay board from Amazon after horribly failing soldering together my own.


![Web Interface Page](https://github.com/johanknelsen/RPi-Flask-WebServer/blob/master/Pictures/Annotation%202020-03-31%20115003.png)
