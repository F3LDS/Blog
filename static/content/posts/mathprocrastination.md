title: Math Procrastination
date: April 4, 2013

It started out as a normal night. I had a math assignment due the next day so I headed down to the Purdue House computer lab to print it out. 

Just my luck, not a single computer would connect to the printer. Jeez, it must be like Whack-A-Mole for the UITS folks trying to keep the campus infrastructure running smoothly. No biggie, I poke around the printer’s settings menu until I find the IP address, pop it into windows and I’m off and running.

I got back to my apartment and what did I do? Not work on the homework of course. No, with the printer IP address still in my hand I dug up an ancient article on hacking HP Printers to display custom messages. It involves telnetting into the printer on port 9100 and executing a little code snippet.

<img src="/static/content/images/mathprocrastination/1.png">

Boom, done! Someone is sure to get a kick out of that. Or at least a UITS employee will scratch their head over it. I’ll have to go check the printer tomorrow but based off my experiences fooling around in my Net+ class in high school, this should’ve worked just fine.

This little trick got me thinking… what If I sent this command out across the entire IUPUI network to all devices running on this port? I could easily change the ready message for every printer on campus (and perhaps IU and Purdue as well…). Legal problems aside, how would I go about doing this? Well I have two options.

I could port scan the entire network for all devices with port 9100 open. Not only will this take forever but it’s sure to generate a lot of really suspicious looking activity from my account. No thanks.

Or perhaps there’s already a list of printers somewhere… Aha! My IU Printer Finder App! I opened that up and was disappointed to find it didn’t actually list any IP addresses. No fear, I’m sure this app uses some sort of file to cache all listed devices. I opened Activity Monitor to take a look at what files it was using and found one that looked promising:

<img src="/static/content/images/mathprocrastination/2.png">

Cache.db it was then. Seeing as it was some kind of database I tried opening it in Firefox’s SQLite database browser.

<img src="/static/content/images/mathprocrastination/3.png">

Success! Now I had a list of all the calls the IU Printer Finder made to a remote server in order to list the active printers on the network. I slapped one of the URLs into my web browser and I got back a pretty little XML file of all the buildings on campus containing printers.

<img src="/static/content/images/mathprocrastination/4.png">

Now we’re getting somewhere. I noticed that other remote calls in the SQLite database were simply the URL plus the name of the building. So by navigating to “/PrinterService.svc/Indianapolis/SL 1st Floor” I was able to move further into the XML tree. This time I could see a list of all the printers in that building. Go one more step and append the printer name and… 

<img src="/static/content/images/mathprocrastination/5.png">

Oh my, hello there printer address! There we have it; A fully parsable xml file structure containing the addresses of all the printers on each IU/Purdue campus.

Next up is writing a python script to extract the addresses and attempt to execute the READYMSG command on each one. If it works, I could even set up a script to run on my partition of the Pegasus server to update the message each day, sidestepping the problem of the printers losing their memory on reboot.

Will I actually do this? Maybe. I started to wonder if perhaps there’s a code of conduct violation in here somewhere. It’s not malicious by any means, It’s quite harmless. In fact if I where to display: “Go Jags!” on every printer I doubt there would consequences beyond a “Haha, clever. Now don’t do it again”. 

Hey, #YOLOSWAG right?