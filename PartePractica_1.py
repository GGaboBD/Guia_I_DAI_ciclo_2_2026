class Locomotora:
    def __init__(self, ID_locomotora: str, modelo: str, capacidad_arrastre: float ):
        self.ID_locomotora = ID_locomotora
        self.modelo = modelo
        self.capacidad_arrastre = capacidad_arrastre

class Vagon:
    def __init__(self, ID_vagon: str, peso_vacio: float):
        self.ID_vagon = ID_vagon
        self.peso_vacio = peso_vacio

    def calcular_peso_total(self):
        pass

class VagonCargaSeca(Vagon):
    def __init__(self, ID_vagon, peso_vacio, peso_carga_actual: float):
        super().__init__(ID_vagon, peso_vacio)
        self.peso_carga_actual = peso_carga_actual

    def calcular_peso_total(self):
        return self.peso_vacio + self.peso_carga_actual


class VagonCisterna(Vagon):
    def __init__(self, ID_vagon, peso_vacio, capacidad_litros: float, densidad_liquido: float):
        super().__init__(ID_vagon, peso_vacio)
        self.capacidad_litros = capacidad_litros
        self.densidad_liquido = densidad_liquido

    def calcular_peso_total(self):
        return self.peso_vacio + (self.capacidad_litros * self.densidad_liquido)
        

class Tren:
    def __init__(self, ID_tren: str, locomotora: Locomotora):
        self.ID_tren = ID_tren
        self.locomotora = locomotora
        self._vagones = []
    

    def obtener_peso_tren(self):
        total = 0
        for vagon in self._vagones: 
            total += vagon.calcular_peso_total()
        return total
    
    def enganchar_vagon(self, vagon: Vagon):
        nuevo_peso_tren = self.obtener_peso_tren() + vagon.calcular_peso_total()

        if nuevo_peso_tren > self.locomotora.capacidad_arrastre:
            raise ValueError("Capacidad de arrastre excedida")

        conteo_cisternas = 0
        for v in self._vagones:
            if isinstance(v, VagonCisterna):
                conteo_cisternas += 1

        if isinstance(vagon, VagonCisterna):
            conteo_cisternas+=1

        peso_futuro_cisternas = 0
        for v in self._vagones:
            if isinstance(v, VagonCisterna):
                peso_futuro_cisternas += v.calcular_peso_total()
        
        if isinstance(vagon, VagonCisterna):
            peso_futuro_cisternas += vagon.calcular_peso_total()

        if conteo_cisternas > 3:
            raise ValueError("Restricción de seguridad de Vagones Cisterna violada")
        
        if nuevo_peso_tren > 0: # Evitar división por cero
            porcentaje_cisternas = peso_futuro_cisternas / nuevo_peso_tren
            if porcentaje_cisternas > 0.60:
                raise ValueError("Restricción de seguridad de Vagones Cisterna violada")
            
        self._vagones.append(vagon)

# a ver si ahora funciona