from cmath import sqrt

class Node:
    def __init__(self, id, posX, posY):
        self.id = id
        self.pos = [posX, posY]
        self.connectedNodes = []
        self.accumCost = 0
        self.backPointer = []
        self.cheapestBack = None
        self.heading = None
        self.headingBed = None
        self.route = []
    def addConnection(self, newConnection):
        if isinstance(newConnection, list):
            self.connectedNodes = self.connectedNodes + newConnection
            for node in newConnection:
                addConnection(node, self)
        else:
            self.connectedNodes = self.connectedNodes + [newConnection]
            addConnection(newConnection, self)
    def __str__(self):
        stringToReturn = str(self.pos)
        return stringToReturn
    def __repr__(self):
        stringToReturn = str(self.id)
        return stringToReturn
    
def addConnection(node, newConnection):
    node.connectedNodes = node.connectedNodes + [newConnection]
