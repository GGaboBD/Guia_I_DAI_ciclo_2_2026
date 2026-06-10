# 1. VALUE OBJECT (Objeto de Valor Inmutable)
class CuotaRecurso:
    def __init__(self, valor: float, unidad_medida: str):
        # Usamos property o los dejamos fijos para representar la inmutabilidad conceptual
        self.valor = valor
        self.unidad_medida = unidad_medida

    # El libro exige que los Value Objects se identifiquen por sus atributos, no por su ID
    def __eq__(self, tracking_object):
        if not isinstance(tracking_object, CuotaRecurso):
            return False
        return self.valor == tracking_object.valor and self.unidad_medida == tracking_object.unidad_medida


# 2. MODELO DE DOMINIO (Clase Base)
class Nodo:
    def __init__(self, cuota_inicial: CuotaRecurso):
        # MODICACIÓN: El nodo ahora tiene un Value Object rico en lugar de un string anémico
        self.cuota = cuota_inicial 
        self.capacidad_remanente = 100.0

    def procesamiento_carga_actual(self):
        raise NotImplementedError("Debe especificarse la lógica de hardware en la arquitectura hija")


# 3. HERENCIA Y POLIMORFISMO
class NodosGenerales(Nodo):
    def __init__(self, cuota_inicial: CuotaRecurso):
        super().__init__(cuota_inicial)
    
    def procesamiento_carga_actual(self):
        # Desgaste fijo del 6.5%
        self.capacidad_remanente -= 6.5


class NodosAceleracionGrafica(Nodo):
    def __init__(self, cuota_inicial: CuotaRecurso, hilos_activos: float):
        super().__init__(cuota_inicial)
        self.hilos_activos = hilos_activos
    
    def procesamiento_carga_actual(self):
        # CORRECCIÓN: El cálculo de la tasa y reducción debe ocurrir DURANTE la ejecución
        tasa = self.hilos_activos / 800.0
        self.capacidad_remanente = self.capacidad_remanente - (self.capacidad_remanente * tasa)


# 4. COMPOSICIÓN
class EnlaceFibraOptica:
    def __init__(self, identificador_canal: str, capacidad_gbps: float):
        self.identificador_canal = identificador_canal
        self.capacidad_gbps = capacity_gbps


# 5. ENTIDAD RICA (Controlador del Dominio)
class DespachadorCentral:
    def __init__(self, id_red_global: str, region: str, identificador_canal: str, capacidad_gbps: float):
        self.id_red_global = id_red_global
        self.region = region
        self._nodos = []
        self.condicion_operativa = "NORMAL"
        # Composición: El enlace físico nace estrictamente adentro
        self.enlace_fisico = EnlaceFibraOptica(identificador_canal, capacidad_gbps)

    @property
    def nodos_asignados(self):
        return tuple(self._nodos)

    def asignar_nodo(self, nodo: Nodo):
        if len(self._nodos) >= 3:
            raise ValueError("Invariante rota: Capacidad máxima de hardware sobrepasada en despachador")
        self._nodos.append(nodo)

    def procesar_nodos_global(self):
        # Guardián de seguridad en la primera línea
        if self.condicion_operativa == "EXCLUSION_CRITICA":
            raise RuntimeError("Operación ilegal: El despachador se encuentra bajo exclusión crítica")
        
        if len(self._nodos) == 0:
            return

        # CORRECCIÓN: Mandar a ejecutar el procesamiento polimórfico en cada nodo asignado
        for nodo in self._nodos:
            nodo.procesamiento_carga_actual()

        # Evaluación de métricas e Invariantes globales
        total_remanente = 0
        for nodo in self._nodos:
            total_remanente += nodo.capacidad_remanente
        
        promedio = total_remanente / len(self._nodos)

        if promedio < 35.0:
            self.condicion_operativa = "EXCLUSION_CRITICA"
            print("¡ADVERTENCIA: Umbral crítico alcanzado! Condición cambiada a EXCLUSION_CRITICA.")


#----------------------------------------------------------------------------------------
# AGREGACIÓN DE VALORES Y EJECUCIÓN EN CONSOLA (Para probar tu código)
#----------------------------------------------------------------------------------------

# 1. Creamos los objetos de valor de cuota
cuota_vcpu = CuotaRecurso(8, "vCPU")
cuota_gpu = CuotaRecurso(512, "GPU_Cores")

# Probar la igualdad del Value Object (Teoría del libro aplicada)
cuota_clon = CuotaRecurso(8, "vCPU")
print(f"¿Las cuotas son conceptualmente iguales?: {cuota_vcpu == cuota_clon}") # Debe imprimir True

# 2. Creamos las unidades de procesamiento (Nodos)
nodo_1 = NodosGenerales(cuota_vcpu)
nodo_2 = NodosAceleracionGrafica(cuota_gpu, 400.0) # 400 hilos activos implica tasa de 400/800 = 0.5 (50%)

# 3. Inicializamos el orquestador (Despachador) pasando datos de la composición
despachador = DespachadorCentral("NET-USA-01", "North Virginia", "CH-FIBER-99", 100.0)

# 4. Vinculamos los recursos
despachador.asignar_nodo(nodo_1)
despachador.asignar_nodo(nodo_2)

print(f"Nodos registrados en el clúster: {len(despachador.nodos_asignados)}")

# 5. Ejecutamos el ciclo global de procesamiento de datos y vemos cómo se desgastan las capacidades
print(f"Capacidad inicial Nodo General: {nodo_1.capacidad_remanente}%")
print(f"Capacidad inicial Nodo GPU: {nodo_2.capacidad_remanente}%")

print("\n--- Ejecutando Ciclo 1 de Procesamiento Computacional ---")
despachador.procesar_nodos_global()
print(f"Capacidad remanente Nodo General (gasto fijo 6.5): {nodo_1.capacidad_remanente}%")
print(f"Capacidad remanente Nodo GPU (gasto dinámico del 50%): {nodo_2.capacidad_remanente}%")

print("\n--- Ejecutando Ciclo 2 de Procesamiento Computacional ---")
despachador.procesar_nodos_global()
print(f"Capacidad remanente Nodo GPU (vuelve a perder el 50% de lo que le quedaba): {nodo_2.capacidad_remanente}%")

print(f"Condición operativa del sistema: {despachador.condicion_operativa}")

print("\n--- Ejecutando Ciclo 3 de Procesamiento Computacional ---")
# Aquí el promedio general caerá por debajo del 35% y se activará la exclusión crítica automáticamente
despachador.procesar_nodos_global()
print(f"Condición operativa final del sistema: {despachador.condicion_operativa}")

# Si intentáramos ejecutar un ciclo más, el guardián lanzará el RuntimeError bloqueando la terminal:
# despachador.procesar_nodos_global()