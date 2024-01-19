"""_summary_

•	Numero de serie
•	Nombre de dispositivo
•	Numero de flota
•	Estado
•	Tipo de dispositivo
•	Hash
•	Fecha 

"""
class DatosDeIdentificacion:
    
    def __init__(self):
        self.numero_serie: float = None
        self.nombre_dispositivo: str = None
        self.numero_flota: int = None
        self.estado: str = None
        self.tipo_dispositivo: str = None
        self.hash: str = None
        self.fecha: str = None
        self.mision: str = None

#getters
@property 
def numero_serie(self) -> float:
    return self._numero_serie
@property 
def nombre_dispositivo(self) -> str:
    return self._nombre_dispositivo
@property 
def numero_flota(self) -> int:
    return self._numero_flota
@property 
def estado(self) -> str:
    return self._estado
@property 
def tipo_dispositivo(self) -> str:
    return self._tipo_dispositivo
@property 
def hash(self) -> str:
    return self._hash
@property 
def fecha(self) -> str:
    return self._fecha
@property 
def mision(self) -> str:
    return self._mision


#setters
@numero_serie.setter 
def numero_serie(self, value: float) -> None:
    self._numero_serie = value
    
@nombre_dispositivo.setter 
def nombre_dispositivo(self, value: str) -> None:
    self._nombre_dispositivo = value

@numero_flota.setter 
def numero_flota(self, value: str) -> None:
    self._numero_flota = value

@estado.setter 
def estado(self, value: str) -> None:
    self._estado = value

@tipo_dispositivo.setter 
def tipo_dispositivo(self, value: str) -> None:
    self._tipo_dispositivo = value

@hash.setter 
def hash(self, value: str) -> None:
    self._hash = value

@fecha.setter 
def fecha(self, value: str) -> None:
    self._fecha = value
    
@mision.setter 
def mision(self, value: str) -> None:
    self._mision = value