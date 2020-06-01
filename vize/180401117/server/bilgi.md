The official example of multicast can be found at /usr/share/doc/python2.3/examples/Demo/sockets/mcast.py (at least on Debian Sarge, after apt-get install python-examples). It worked on my machine, but I have yet to try it running on different machines. -- -- 200.138.245.121 2006-08-09 03:20:30

I've been googling for some time now, and still have yet to find a working example of Python multicast listening.

(The example below has been updated to work -- Steven Spencer 2005-04-14 13:19:00)

(I've replaced it with one that works. -- Asgeir S. Nilsen 2005-05-09 19:25:00)

(I've corrected the mreq according to the comment below -- Sebastian Setzer 2006-01-25 14:28:00)

(I added an "=" to the "4sl" struct packing. Both the old version and the new version work on my 32-bit machine, but the Python documentation for the struct module suggests that "l" would be 64 bits on an LP64 or LPI64 platform without it, so I thought it would be prudent to add. -- Kragen Sitaker 2010-04-28 07:03:00)
