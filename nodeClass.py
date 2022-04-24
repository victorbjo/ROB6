from cmath import sqrt

class Node:
    def __init__(self, id, posX, posY):
        self.id = id
        self.goal = None
        self.pos = [posX, posY]
        self.connectedNodes = []
        self.cost = []
        self.route = []
        self.accumCost = 0
        self.backPointer = []
        self.cheapestBack = None
    def addChild(self, newConnection):
        if isinstance(newConnection, list):
            self.connectedNodes = self.connectedNodes + newConnection
            for node in newConnection:
                addChild(node, self)
        else:
            self.connectedNodes = self.connectedNodes + [newConnection]
            addChild(newConnection, self)
    def __str__(self):
        stringToReturn = str(self.pos)
        return stringToReturn
    def __repr__(self):
        stringToReturn = str(self.id)
        return stringToReturn
    
def addChild(node, newConnection):
    node.connectedNodes = node.connectedNodes + [newConnection]