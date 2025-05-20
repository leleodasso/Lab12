import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}


    def getNazioni(self):
        return DAO.getNazioni()

    def buildGraph(self, nazione, anno):
        self._graph.clear()
        residenti = DAO.getResidenti(nazione)
        self._graph.add_nodes_from(residenti) #aggiungo i nodi

        for r in residenti: #popolo l'idMap
            self._idMap[r.Retailer_code] = r


        for r1 in residenti:    #aggiungo gli archi
            for r2 in residenti:
                if r1 != r2:
                    temp = DAO.getProdottiComuni(r1.Retailer_code,r2.Retailer_code, anno)
                    if temp is not None and temp[0] > 0:
                        self._graph.add_edge(r1,r2, weight=temp)

    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)