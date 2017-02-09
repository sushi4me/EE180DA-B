from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
 
class IphoneChat(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print "clients are ", self.factory.clients
 
    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        a = data.split(':')
        print a
        if len(a) > 1:
            command = a[0]
            content = a[1]
 
            msg = ""
            if command == "iam":
                self.name = content
                msg = self.name + " has joined"
 
            elif command == "msg":
                msg = self.name + ": " + content
                print msg
 
            for c in self.factory.clients:
                c.message(msg)

    def message(self, message):
        self.transport.write(message + '\n') 


factory = Factory()
factory.protocol = IphoneChat
factory.clients = []
<<<<<<< HEAD
reactor.listenTCP(60, factory)
=======
reactor.listenTCP(80, factory)
>>>>>>> 27d2098d3cb40e01a488f652572c88035e0da118
print "Iphone Chat server started"
reactor.run()
