class Sensor:
    def __init__(self, modelo: str):
        self.modelo = modelo
        self.bateria_restante = 100.0

    def registrar_lectura(self):
        raise NotImplementedError("El metodo registrar_lectura() debe implementarse en las clases hijas")

class SensorCorriente(Sensor):
    def __init__(self, modelo):
        super().__init__(modelo)

    def registrar_lectura(self):
        self.bateria_restante -= 4.5

class SensorPresion(Sensor):
    def __init__(self, modelo, profundidad_metros: float):
        super().__init__(modelo)
        self.profundidad_metros = profundidad_metros

    def registrar_lectura(self):
        factor = self.profundidad_metros/500.0
        self.bateria_restante = self.bateria_restante - (self.bateria_restante * factor)
    

class TransmisorRadio:
    def __init__(self, frecuencia_mhz: float, potencia_vatios: float):
        self.frecuencia_mhz = frecuencia_mhz
        self.potencia_vatios = potencia_vatios



class BoyaMarina: #Estacion flotante
    def __init__(self, ID_registro: str, coordenadas: str, frecuencia_mhz: float, potencia_vatios: float):
        self.ID_registro = ID_registro
        self.coordenadas = coordenadas
        self.estado = "OPERATIVA"
        self._sensores = []
        self.transmisor_radio = TransmisorRadio(frecuencia_mhz, potencia_vatios)

    @property
    def mostrar_sensores(self):
        return tuple(self._sensores)


    def registrar_sensor(self, sensor: Sensor):
        if len(self._sensores) >= 3:
            raise ValueError("Capacidad maxima de sensores alcanzada")

        self._sensores.append(sensor)

    def ejecutar_muestreo_global(self):
        if self.estado == "SISTEMA_CRITICO":
            raise RuntimeError("Energia maxima alcanzada. Sistema critico activado")
        
        if len(self._sensores) == 0:
            return

        for sensor in self._sensores:
            sensor.registrar_lectura()
        

        total = 0
        for sen in self._sensores:
            total += sen.bateria_restante
        
        promedio = total/len(self._sensores)

        if promedio < 25.0:
            self.estado = "SISTEMA_CRITICO"