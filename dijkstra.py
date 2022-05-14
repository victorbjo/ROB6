from nodeClass import Node
from cmath import sqrt
def mesaureDist(node0 : Node, node1 : Node): # Measure the distance between two nodes using pythagoras theorem
    a = node1.pos[0]-node0.pos[0]
    a = a * a
    b = node1.pos[1]-node0.pos[1]
    b = b * b
    return abs(sqrt(a+b).real)
def djikstra(start, goal): 
    queue  : list[Node] = [start] #list of nodes to run through
    sentBy : list[Node] = [start]
    while queue: 
        currentNode = queue.pop(0) #clears first entry
        sentByNode = sentBy.pop(0) #clears first entry
        currentNode.backPointer.append(sentByNode) #adds which node it is sent from to the backpointer list
        newCost = sentByNode.accumCost + mesaureDist(sentByNode, currentNode) #calculates the new distance and adds its cost to the previous cost for currentnode
        if newCost > currentNode.accumCost and currentNode.accumCost != 0: #checks if the new cost is lower than the previous (and is not 0)
            continue
        currentNode.cheapestBack = sentByNode
        currentNode.accumCost = newCost
        if currentNode == goal:
            continue
        for connection in currentNode.connectedNodes: #checks connects to current node
            if connection not in currentNode.backPointer: #if connected node in not present in backpointer list then append current node to sentBy and connections to the queue of nodes to iterate through
                sentBy.append(currentNode)
                queue.append(connection)
                
def shortestRoute(start : Node, goal : Node):
    djikstra(start, goal)
    listToReturn = [] #initializes list for cheapest node route
    currentNode = goal
    while True:
        listToReturn.append(currentNode) #appends cheapest node for current node
        if currentNode == start: #When start node is reached runs code below
            listToReturn.reverse() #reverses entire list so the first node in the list is start node
            return listToReturn
        currentNode = currentNode.cheapestBack #moves on to the previous cheapest node and make it current node (because we start at goal node and go backwards)

if __name__ == "__main__":
    n0 = Node("a",0,0)
    n1 = Node("b",2,0)
    n2 = Node("c",3,1)
    n3 = Node("d",2,1)
    n0.addConnection([n1, n3])
    n1.addConnection([n2, n3])
    n2.addConnection(n3)


    #djikstra(n0, n2)
    print(shortestRoute(n0,n2))
