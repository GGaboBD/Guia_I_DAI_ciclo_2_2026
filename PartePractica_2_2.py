from abc import abstractmethod

class TarjetaRed:
    def __init__(self, direccion_mac: str, frecuencia_ghz: str):
        self.direccion_mac = direccion_mac
        self.frecuencia_ghz = frecuencia_ghz

class Dispositivo(ABC):
    def __init__(self, modelo: str):
        self.modelo = modelo
        self.energia = 100.0

    @abstractmethod
    def consumir_energia(self, temperatura_ambiente: float):
        #cada equipo consume energia segun su propia naturaleza o ambiente creo
        pass



class LuzInteligente(Dispositivo):
    def consumir_energia(self, temperatura_ambiente):
        self.energia = max(0.0, self.energia - 2.5)

class AireAcondicionado(Dispositivo):
    def __init__(self, modelo):
        super().__init__(modelo)

    def consumir_energia(self, temperatura_ambiente: float):
        factor_consumo = 1.0 - (temperatura_ambiente * 0.0008)
        self.energia = max(0.0, self.energia * factor_consumo)




class CentralHub:
    def __init__(self, ID_central: str, nombre: str):
        self.ID_central = ID_central
        self.nombre = nombre
        self._dispositivos = []
        pass