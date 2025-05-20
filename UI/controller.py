import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        lista_nazioni = self._model.getNazioni()
        lista_anni = [2015,2016,2017,2018]
        for nazione in lista_nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(nazione))
        for anno in lista_anni:
            self._view.ddyear.options.append(ft.dropdown.Option(str(anno)))



    def handle_graph(self, e):
        nazione = self._view.ddcountry.value
        anno = self._view.ddyear.value
        if nazione is None or anno is None:
            self._view.create_alert("Selezionare il Dropdown")
        self._model.buildGraph(nazione, anno)
        self._view.txt_result.clean()
        num_nodi = self._model.getNumNodi()
        num_archi = self._model.getNumArchi()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {num_nodi} Numero di archi: {num_archi}"))
        self._view.update_page()


    def handle_volume(self, e):
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Numero di volume: {self._model.getVolume()}"))


    def handle_path(self, e):
        pass
