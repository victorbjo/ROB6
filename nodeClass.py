from cmath import sqrt
from platform import node

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
                self.cost.append(mesaureDist(self, node))
                addChild(node, self)
        else:
            self.connectedNodes = self.connectedNodes + [newConnection]
            self.cost.append(mesaureDist(self, newConnection))
            addChild(newConnection, self)
    def __str__(self):
        stringToReturn = str(self.pos)
        return stringToReturn
    def __repr__(self):
        stringToReturn = str(self.id)
        return stringToReturn
    
def mesaureDist(node0 : Node, node1 : Node):
    a = node1.pos[0]-node0.pos[0]
    a = a * a
    b = node1.pos[1]-node0.pos[1]
    b = b * b
    return sqrt(a+b).real
def addChild(node, newConnection):
    node.connectedNodes = node.connectedNodes + [newConnection]
    node.cost.append(mesaureDist(node, newConnection))