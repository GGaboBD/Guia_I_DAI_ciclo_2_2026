class Dron:
    def __init__(self, modelo:str ):
        self.modelo = modelo
        self.bateria_restante = 100.0

    def volar_ciclo(self):
        raise NotImplementedError("Se debe aplicar en las clases hijas el metodo volar_ciclo")

class DronLiviano(Dron):
    def __init__(self, modelo):
        super().__init__(modelo)
    
    def volar_ciclo(self):
        self.bateria_restante -= 5.5


class DronPesado(Dron):
    def __init__(self, modelo, peso_carga_kg: float):
        super().__init__(modelo)
        self.peso_carga_kg = peso_carga_kg

    def volar_ciclo(self):
        factor = self.peso_carga_kg/10
        self.bateria_restante = self.bateria_restante - (self.bateria_restante * factor)





class AntenaSatelital:
    def __init__(self, codigo_satelite: str, ancho_banda_mbps: float):
            self.codigo_satelite = codigo_satelite
            self.ancho_banda_mbps = ancho_banda_mbps



class EstacionDespacho:
    def __init__(self, ID_estacion: str, nombre_ciudad: str, codigo_satelite: str, ancho_banda_mbps: float):
        self.ID_estacion = ID_estacion
        self.nombre_ciudad = nombre_ciudad
        self._drones = []
        self.antena_satelital = AntenaSatelital(codigo_satelite, ancho_banda_mbps)
        self._estado = "DISPONIBLE"

    def validacion_drones(self, dron: Dron):
        if len(self._drones) >= 3:
            raise ValueError("Capacidad maxima de drones por estacion alcanzada")

        self._drones.append(dron)
        
    @property
    def inventario_drones(self):
        return tuple(self._drones)
    
    def despachar_vuelo_global(self):
        if self._estado == "ALERTA_BATERIA":
            raise RuntimeError("Los drones no pueden despegar debido a la baja bateria")

        for dron in self._drones:
            dron.volar_ciclo()
        
        total_bateria = 0

        for batery in self._drones:
            total_bateria += batery.bateria_restante
        promedio = total_bateria/len(self._drones)

        if promedio < 20.0:
            self._estado = "ALERTA_BATERIA"