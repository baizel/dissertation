from Viz.Graph.DataSet import Node, Edge
from Viz.utils.AnimationUpdate import AnimationUpdate


def ser(obj):
    if isinstance(obj, Node):
        return obj.id
    if isinstance(obj, Edge):
        return obj.toNode
    return obj.__dict__


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
        self.displayNames = {
            self.distanceId: "All Distances",
            self.prevId: "Optimal Previous Node",
            self.QId: "Set of all nodes in Q",
            self.minUID: "Node with the smallest distance from source",
            self.neighbourID: "Neighbour of <span class='data {}raw'></>".format(self.minUID),  # Not clean but will do to show current node
        }

        self.animationEdgeIDCounter = 0

    def initDistAndPrev(self, dist, prev):
        self.animation.addToUpdateQueue(6)
        self.animation.addToUpdateQueue(7, data=AnimationUpdate.getLineData(self.distanceId, dist, "Distance", self.displayNames[self.distanceId]))
        self.animation.addToUpdateQueue(8, data=AnimationUpdate.getLineData(self.prevId, prev, "Previous", self.displayNames[self.prevId]))

    def updateDist(self, dist: dict):
        self.animation.addToUpdateQueue(11, data=AnimationUpdate.getLineData(self.distanceId, dist, "Distance", self.displayNames))

    def initQ(self, q):
        self.animation.addToUpdateQueue(12, data=AnimationUpdate.getLineData(self.QId, q, "Q", self.displayNames[self.QId]))

    def setMinU(self, minVertex):
        nodes = [{"id": minVertex.id, "color": "yellow", "label": str(minVertex.id)}]
        self.animation.addToUpdateQueue(15, data=AnimationUpdate.getLineData(self.minUID, minVertex, "Smallest Node", self.displayNames[self.minUID]), nodes=nodes)

    def removeU(self, q, source: Node):
        self.animation.addToUpdateQueue(16, data=AnimationUpdate.getLineData(self.QId, q, "Q", self.displayNames[self.QId]))

        nodes = [{"id": source.id, "color": "yellow", "label": str(source.id)}]
        neighbour = [i.toNode for i in source.neighbourEdge]
        if len(neighbour) > 0:
            nodes += [{"id": i, "color": "purple", "label": str(i)} for i in neighbour]
        self.animation.addToUpdateQueue(17, data=AnimationUpdate.getLineData(self.neighbourID, neighbour, "Neighbour node(s)", self.displayNames[self.neighbourID]), nodes=nodes)

    def findAltAndCmp(self, uDistance, vDistance, cost, sourceNode, destNode, previous, dijkSource, graph):
        self.animationEdgeIDCounter += 1

        edge = [{"id": "animation" + str(self.animationEdgeIDCounter), "from": sourceNode, "to": destNode, "label": "{} + {}".format(uDistance, cost), "color": {"color": "red"}}]
        base = sourceNode
        pathNodes = [] if base is None else [sourceNode]
        # {"id": sourceNode, "color": {"color": "red"}}
        while base is not None and base != dijkSource.id:
            base = previous[base]
            if base is not None:
                pathNodes.append(base)
        pathEdges = []
        if len(pathNodes) > 1:
            for i in range(0, len(pathNodes) - 1):
                edgeId = graph.getEdge(pathNodes[i + 1], pathNodes[i]).id
                e = {"id": edgeId, "color": {"color": "red"}, "isNew": False}
                pathEdges.append(e)

        edge += pathEdges
        self.animation.addToUpdateQueue(18, data=AnimationUpdate.getLineData(self.altAdditionID, "{} + {}".format(uDistance, cost)), edges=edge)
        self.animation.addToUpdateQueue(19, data=AnimationUpdate.getLineData(self.cmpCostID, "{} < {}".format(uDistance + cost, vDistance)))

    def setDistAndPrevToAlt(self, dist, prev):
        self.animation.addToUpdateQueue(20, data=AnimationUpdate.getLineData(self.distanceId, dist, "Distance", self.displayNames))
        self.animation.addToUpdateQueue(21, data=AnimationUpdate.getLineData(self.prevId, prev, "Previous", self.displayNames[self.prevId]))
        self.animation.addToUpdateQueue(22)

    def ret(self, dist, prev):
        self.animation.addToUpdateQueue(23)
        self.animation.addToUpdateQueue(24)
        self.animation.addToUpdateQueue(25, data=AnimationUpdate.getLineData(self.returnDataID, "Distance: {}, Previous: {}".format(dist, prev)))

    def getUpdates(self):
        return self.animation.getFrames()
