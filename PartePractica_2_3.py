class TarjetaRed:
    def __init__(self, direccion_mac: str, frecuencia_ghz: float):
        self.direccion_mac = direccion_mac
        self.frecuencia_ghz = frecuencia_ghz

class CentralHUB:
    def __init__(self, ID_central: str, nombre_habitacion: str, direccion_mac: str, frecuencia_ghz: float ):
        self.ID_central = ID_central
        self.nombre_habitacion = nombre_habitacion
        self._dispositivos = []
        self.tarjeta_red = TarjetaRed(direccion_mac, frecuencia_ghz)

    @property
    def dispositivos(self):
        return tuple(self._dispositivos)