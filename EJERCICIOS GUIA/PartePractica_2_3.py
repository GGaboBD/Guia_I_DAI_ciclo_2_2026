class Dispositivo:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.energia_restante = 100.0
    
    def actualizar_ciclo(self):
        raise NotImplementedError("Las clases hijas deben implementar actualizar_ciclo")

class LucesAutomaticas(Dispositivo):
    def __init__(self, nombre):
        super().__init__(nombre)

    def actualizar_ciclo(self):
        self.energia_restante -= 2.5


class AireAcondicionado(Dispositivo):
    def __init__(self, nombre, temperatura: float):
        super().__init__(nombre)
        self.temperatura = temperatura

    def actualizar_ciclo(self):
        factor = self.temperatura/100
        self.energia_restante = self.energia_restante - (self.energia_restante*factor)
    
        

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
        self.estado = "NORMAL"

    @property
    def dispositivos(self):
        return tuple(self._dispositivos)
    
    def vincular_dispositivo(self, dispositivo):
        if len(self._dispositivos) >= 4:
            raise ValueError("Maxima cantidad de dispositivos vinculados alcanzada")
        self._dispositivos.append(dispositivo)

    def ejecutar_ciclo_global(self):
        if self.estado == "MODO_AHORRO_CRITICO":
            raise RuntimeError("Central bloqueada por seguridad energética")

        for dispositivo in self._dispositivos:
            dispositivo.actualizar_ciclo()
        print("Evaluando reglas de seguridad...")

        if len(self._dispositivos) == 0:
            return
        total_energia = 0 

        aire_peligroso = False

        for disp in self._dispositivos:
            if isinstance(disp, AireAcondicionado):
                if disp.temperatura > 40.0:
                    aire_peligroso = True


        for disposit in self._dispositivos: 
            total_energia += disposit.energia_restante
        promedio_energia = total_energia/len(self._dispositivos)
        
        condicion_A = promedio_energia < 15.0
        condicion_B = self.tarjeta_red.frecuencia_ghz > 5.0 and aire_peligroso == True

        if condicion_A or condicion_B:
            self.estado = "MODO_AHORRO_CRITICO"

