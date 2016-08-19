# Louver

Louvers are rarely seen as primary design elements in the language of 
modern architecture, but rather simply a technical device.

This louver is used to serve as technical device to enable an 
automated home.

## Getting started

There are two+ components involved.

#### The Server (DigitalOcean)

Consists of: 
 
 - Nginx (sitting in front of all else)
 - Crossbar application to handle communication
 - Django application to enable a friendly UI

The server is the WAMP Server that connects all of our devices
to one another.

#### The IOT Devices. (aka Raspberry Pis)

Consists of:
 - Access Point Script (hostapd | isc-dhcp-server | iw | iptables)
 - Flask Application to Setup SSIDs (works in conjunction with the AP)
 - Autobahn|Python Application
 - Any peripherals you would like to connect to it.

When serving their primary purpose, these devices are connected 
via Autobahn to our Crossbar application sitting on the Server.
