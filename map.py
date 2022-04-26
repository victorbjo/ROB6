from nodeClass import Node
from cmath import sqrt
def mesaureDist(node0 : Node, node1 : Node):
    a = node1.pos[0]-node0.pos[0]
    a = a * a
    b = node1.pos[1]-node0.pos[1]
    b = b * b
    return abs(sqrt(a+b).real)
def djikstra(start, goal):
    queue  : list[Node] = [start]
    sentBy : list[Node] = [start]
    while queue:
        currentNode = queue.pop(0)
        sentByNode = sentBy.pop(0)
        currentNode.backPointer.append(sentByNode)
        newCost = sentByNode.accumCost + mesaureDist(sentByNode, currentNode)
        if newCost > currentNode.accumCost and currentNode.accumCost != 0:
            continue
        currentNode.cheapestBack = sentByNode
        currentNode.accumCost = newCost
        if currentNode == goal:
            continue
        for connection in currentNode.connectedNodes:
            if connection not in currentNode.backPointer:
                sentBy.append(currentNode)
                queue.append(connection)
                
def shortestRoute(start : Node, goal : Node):
    djikstra(start, goal)
    listToReturn = []
    currentNode = goal
    while True:
        listToReturn.append(currentNode)
        if currentNode == start:
            listToReturn.reverse()
            return listToReturn
        currentNode = currentNode.cheapestBack

if __name__ == "__main__":
    n0 = Node("a",0,0)
    n1 = Node("b",2,0)
    n2 = Node("c",3,1)
    n3 = Node("d",2,1)
    n0.addChild([n1, n3])
    n1.addChild([n2, n3])
    n2.addChild(n3)


    #djikstra(n0, n2)
    print(shortestRoute(n0,n2))