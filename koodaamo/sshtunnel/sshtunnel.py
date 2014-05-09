#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getpass, docopt
from twisted.conch.ssh.transport import SSHClientTransport
from twisted.conch.ssh import userauth, connection
from twisted.conch.ssh.forwarding import SSHListenClientForwardingChannel
from twisted.conch.ssh.forwarding import SSHListenForwardingFactory
from twisted.internet import defer, protocol, reactor
from twisted.python import log

# settings init

USER = ''
PASSWORD = ''
HOST = ''
PORT = 22

LOCALPORT = 0
REMOTEHOST = ""
REMOTEPORT = 0


class Transport(SSHClientTransport):

    def verifyHostKey(self, key, fingerprint):
        print 'host key fingerprint: %s' % fingerprint
        return defer.succeed(1)

    def connectionSecure(self):
        self.requestService(Auth(USER, Connection()))


class Auth(userauth.SSHUserAuthClient):

    def getPassword(self):
        return defer.succeed(PASSWORD)


class Connection(connection.SSHConnection):

    def serviceStarted(self):
       Channel = SSHListenClientForwardingChannel
       Factory = SSHListenForwardingFactory
       ffactory = Factory(self, (REMOTEHOST, REMOTEPORT), Channel)
       s = reactor.listenTCP(LOCALPORT, ffactory)


def get_factory(user, password, lport, rhost, rport):
	"factory for forwarding SSH tunnel"

	global USER, PASSWORD, LOCALPORT, REMOTEHOST, REMOTEPORT
	USER, PASSWORD = user, password
	LOCALPORT = lport
	REMOTEHOST = rhost
	REMOTEPORT = rport

	factory = protocol.ClientFactory()
	factory.protocol = Transport
	return factory



doc = """
Usage:
  tunnel <user> <passwd> <host> <port> <localport> <remotehost> <remoteport> [--debug]
  tunnel -h | --help
  tunnel --version

Options:
  -d --debug    Show debug information.
  -h --help     Show this screen.
  -v --version  Show version.
"""


def tunnel():
	"command-line interface"

	args = docopt.docopt(doc, version='tunnel 1.0')

	if args["--debug"]:
		log.startLogging(sys.stdout)
	else:
		print("\nstarting tunnel")
	user, passwd = args["<user>"], args["<passwd>"]
	lp = int(args["<localport>"])
	rh, rp = args["<remotehost>"], int(args["<remoteport>"])
	
	factory = get_factory(user, passwd, lp, rh, rp)
	reactor.connectTCP(args["<host>"], int(args["<port>"]), factory)

	reactor.run()
