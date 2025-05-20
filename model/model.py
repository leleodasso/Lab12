import copy

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


    def getListaVolumi(self):
        lista = []
        for nodo in self._graph.nodes:
            conta = 0
            for vicino in self._graph.neighbors(nodo):
                conta = conta + self._graph.edges[(nodo, vicino)]['weight'][0]
            if conta != 0:
                lista.append((nodo, conta))
                print(f"{nodo}: {conta}")
        lista_ordinata = sorted(lista, key = lambda x : x[1], reverse = True)
        #questa lista è composta da tutte tuple con coppie, nodo --> valore archi .... decrescente
        return lista_ordinata


    def getCamminoOttimo(self, numArchi):
        self._bestPath = []
        self._bestObjFun = 0

        parziale = [] #la lista di nodi da visitare inizialmente vuota

        self._ricorsione(numArchi, parziale)

        return self._bestPath, self._bestObjFun

    def _ricorsione(self, numArchi, parziale):

        if len(parziale) >= 2:
            if (len(parziale) > numArchi + 1 ): #se ho sforato con la dimensione esco
                return
            if parziale[-1] == parziale[0]: #se l'ultimo elemento di parziale è l'elemento iniziale (ciclo)
                if len(parziale) == numArchi + 1: # controllo che devo utilizzare esattamente un numero di archi pari a numArchi
                    if self._getOgjFun(parziale) > self._bestObjFun:
                        self._bestPath = copy.deepcopy(parziale)
                        self._bestObjFun = self._getOgjFun(copy.deepcopy(parziale))

        #se parziale non è una soluzione possibile
        #posso ancora aggiungere dei nodi
        #partendo dall'ultimo nodo aggiunto, prendo i vicini e aggiungo un nodo alla volta
        #infine faccio ripartire la ricorsione

        if len(parziale) == 0: #inizializzo parziale
            for nodo in self._graph.nodes:
                parziale.append(nodo)
                self._ricorsione(numArchi, parziale)
                parziale.pop()
        else:
            for n in self._graph.neighbors(parziale[-1]):#i vicini dell'ultimo nodo
                if self.is_admissible(parziale,numArchi, n) == True:
                    parziale.append(n) #ne aggiungo uno alla volta a parziale
                    self._ricorsione(numArchi, parziale)
                    print(f"pariale: {parziale}")
                    parziale.pop()


    def _getOgjFun(self, listaOfNodes):
        #sommo i valori dei pesi di tutti gli archi
        objVal = 0
        for i in range (0,len(listaOfNodes)-1):
            objVal += self._graph[listaOfNodes[i]][listaOfNodes[i+1]]["weight"][0]
        return objVal

    def is_admissible(self, parziale, numArchi, nuovo_nodo):
        if nuovo_nodo == parziale[0] and len(parziale) == numArchi:
            return True
        if nuovo_nodo not in parziale:
            return True
        return False



