class Nodo:
    def __init__(self, unidad_medida):
        self.unidad_medida = unidad_medida
        self.capacidad_computo = 100.0

    def procesamiento_carga_actual(self):
        raise NotImplementedError("ejecutar procesamiento_carga_actual() en clases hijas")

class NodosGenerales(Nodo):
    def __init__(self, unidad_medida):
        super().__init__(unidad_medida)
    
    def procesamiento_carga_actual(self):
        self.capacidad_computo -= 6.5

class NodosAceleracionGrafica(Nodo):
    def __init__(self, unidad_medida, hilos_activos:float):
        super().__init__(unidad_medida)
        self.hilos_activos = hilos_activos
    
        tasa = hilos_activos/800.0

        self.capacidad_computo = self.capacidad_computo - (self.capacidad_computo * tasa)
    

class ConexionFibraOptica:
    def __init__(self, ID_canal_fibra_optica: str, capacidad_transmision: float):
        self.ID_canal_fibra_optica = ID_canal_fibra_optica
        self.capacidad_transmision = capacidad_transmision
        pass


class DespachadorCentral:
    def __init__(self, ID_red_global: str, region: str, ID_canal_fibra_optica: str, capacidad_transmision: float):
        self.ID_red_global = ID_red_global
        self.region = region
        self._nodos_procesamiento = []
        self.condicion_operativa = "NORMAL"
        self.conexion_fibra_optica = ConexionFibraOptica(ID_canal_fibra_optica, capacidad_transmision)

    @property
    def mostrar_nodo(self):
        return tuple(self._nodos_procesamiento)

    def agregar_nodo_procesamiento(self, nodo: Nodo):
        if len(self._nodos_procesamiento) >= 3:
            raise ValueError("Capacidad maxima de nodos alcanzada")

        self._nodos_procesamiento.append(nodo)

    def procesar_nodos_global(self):
        if self.condicion_operativa == "EXCLUSION_CRITICA":
            raise RuntimeError("Ya se encuentra en modo de exclusion critica")
        
        if len(self._nodos_procesamiento) == 0:
            return
        
        total = 0
        for nodo in self._nodos_procesamiento:
            total += nodo.capacidad_computo
        
        promedio = total/len(self._nodos_procesamiento)

        if promedio < 35.0:
            self.condicion_operativa = "EXCLUSION_CRITICA"