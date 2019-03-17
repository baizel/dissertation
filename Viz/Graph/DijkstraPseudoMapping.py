import json

from Viz.Graph.DataSet import Node, Edge
from Viz.utils.AnimationUpdate import AnimationUpdate

def ser(obj):
    if isinstance(obj, Node):
        return obj.id
    if isinstance(obj, Edge):
        return obj.toNode
    return obj.__dict__


class NodeOptions:
    def __init__(self, ids: []):
        self.ids = []


class DijkstraPseudoMapping:
    def __init__(self):
        self.animation = AnimationUpdate("Dijkstra.txt")
        self.distanceId = "distID"
        self.prevId = "prevID"
        self.QId = "qID"
        self.minUID = "minUID"
        self.neighbourID = "neighbourID"
        self.altAdditionID = "altAdditionID"
        self.cmpCostID = "cmpCostID"
        self.returnDataID = "returnDataID"
        self.animationEdgeIDCounter = 0

    def initDistAndPrev(self, dist, prev):
        self.animation.addToUpdateQueue(6)
        self.animation.addToUpdateQueue(7, data={"lineData": [self.distanceId, "distance: {}".format(self.__sanitise(dist))]})
        self.animation.addToUpdateQueue(8, data={"lineData": [self.prevId, "previous: {}".format(self.__sanitise(prev))]})

    def updateDist(self, dist: dict, source: int):
        self.animation.addToUpdateQueue(11, data={"lineData": [self.distanceId, "distance: {}".format(self.__sanitise(dist))]})

    def initQ(self, q):
        self.animation.addToUpdateQueue(12, data={"lineData": [self.QId, "Q: {}".format(self.__sanitise(q))]})

    def setMinU(self, minVertex):
        self.animation.addToUpdateQueue(15, data={"lineData": [self.minUID, "Smallest Node: {}".format(self.__sanitise(minVertex))]})

    def removeU(self, q, neighbour):
        self.animation.addToUpdateQueue(16, data={"lineData": [self.QId, "Q: {}".format(self.__sanitise(q))]})
        nodes = None
        if len(neighbour) > 0:
            nodes = [{"id": i, "color": "purple", "label": str(i)} for i in neighbour]

        self.animation.addToUpdateQueue(17, data={"lineData": [self.neighbourID, "neighbour node(s): {}".format(self.__sanitise(neighbour))]}, nodes=nodes)

    def findAltAndCmp(self, uDistance, vDistance, cost, sourceNode, destNode):
        self.animationEdgeIDCounter += 1
        edge = [{"id": "animation" + str(self.animationEdgeIDCounter), "from": sourceNode, "to": destNode, "label": "{} + {}".format(uDistance, cost)}]
        self.animation.addToUpdateQueue(18, data={"lineData": [self.altAdditionID, "{} + {}".format(uDistance, cost)]}, edges=edge)

        self.animation.addToUpdateQueue(19, data={"lineData": [self.cmpCostID, "{} < {}".format(uDistance + cost, vDistance)]})  # Alt = uDist+cost

    def setDistAndPrevToAlt(self, distance, prev):
        self.animation.addToUpdateQueue(20, data={"lineData": [self.distanceId, "distance: {}".format(self.__sanitise(distance))]})
        self.animation.addToUpdateQueue(21, data={"lineData": [self.prevId, "previous: {}".format(self.__sanitise(prev))]})
        self.animation.addToUpdateQueue(22)

    def ret(self, dist, prev):
        self.animation.addToUpdateQueue(23)
        self.animation.addToUpdateQueue(24)
        self.animation.addToUpdateQueue(25, data={"lineData": [self.returnDataID, "Distance: {}, Previous: {}".format(dist, prev)]})

    def getUpdates(self):
        return dict(**self.animation.getFrames())

    @staticmethod
    def __sanitise(data):
        if isinstance(data, set):
            return "{}" if len(data) == 0 else data
        if isinstance(data, Node):
            return data.id
        if isinstance(data, Edge):
            return "Error"
        return data
