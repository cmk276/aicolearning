"""Módulo TeamMaker

Incluye la definición de clases para realizar agrupamientos de alumnos
TMRandom -> Agrupamientos aleatorios
TMKmeans -> Agrupamientos homogéneos o heterogéneos mediante el algoritmo K-means

Atributos:
alumnosxEquipo -> Indica el nº máximo de alumnos que puede haber en cada equipo (solo lectura)
alumnos -> DataSet con las características de los alumnos. Las categorías se procesarán automáticamente
equiposGenerados -> Lista que contiene los alumnos que pertenecen a cada equipo
equiposFijos -> Lista de equipos que deben permanecer en sucesivos agrupamientos
numEquipos -> Número de equipos generados
numAlumnos -> Número de alumnos incluidos en la muestra
funcLog -> Función de Log. Debe admitir dos patrámetros de tipo String: Proceso y Mensaje
verbose -> Si es True, la clase llamará a funcLog para enviar mensajes durante la ejecución
"""

from abc import ABC, abstractmethod
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from random import *

# CONSTANTES QUE DEFINEN TIPOS DE AGRUPAMIENTO
TM_NO_DEFINIDO = -2
TM_ALEATORIO = -1
TM_HOMOGENEO = 0
TM_HETEROGENEO = 1

# CLASES
class TeamMaker(ABC) :
    """Clase TeamMaker
    Clase abstracta que define la funcionalidad básica de un agrupador de alumnos.
    La clase se inicializa con un array de vectores con información sobre los alumnos a agrupar.
    Permite generar grupos, dejar unos grupos fijos (para poder reagrupar otros), intercambiar alumnos entre grupos... etc.
    Atributos:
        alumnosxEquipo -> Indica el nº máximo de alumnos que puede haber en cada equipo
        alumnos -> DataSet con las características de los alumnos. Las categorías se procesarán automáticamente
        equiposGenerados -> Lista que contiene los alumnos que pertenecen a cada equipo
        equiposFijos -> Lista de equipos que deben permanecer en sucesivos agrupamientos
        numEquipos -> Número de equipos generados
        numAlumnos -> Número de alumnos incluidos en la muestra
        funcLog -> Función de Log. Debe admitir dos patrámetros de tipo String: Proceso y Mensaje
        verbose -> Si es True, la clase llamará a funcLog para enviar mensajes durante la ejecución
    """
    @abstractmethod

#Métodos
    def __init__(self, alumnos, verbose = False, funclog = None):
        self.alumnos = alumnos
        self.equiposGenerados = []
        self.equiposFijos = []
        self.alumnosxEquipo = 0
        self.numEquipos = 0
        self.numAlumnos = 0
        self.funcLog = funclog
        self.verbose = verbose

    def crea_equipos (self, alumnosxEquipo = 1, tipoAgrupamiento = TM_NO_DEFINIDO):
        pass


    def _log(self, proceso = "", mensaje = ""):
        if (self.verbose) and (self.funcLog is not None):
            self.funcLog(proceso,mensaje)

    
    def _inicializa_equipos(self, alumnosxEquipo = 1):
        """
        Inicializa la lista equiposGenerados añadiendo un elemento por cada equipo.
        Calcula el número de equipos que deben generarse
        """
        self.numAlumnos = len(self.alumnos)
        if (alumnosxEquipo > self.numAlumnos):
            raise ValueError("_inicializa_equipos: alumnnosxEquipo es mayor que el número de alumnos")
        
        if (alumnosxEquipo > 0):
            self.alumnosxEquipo = alumnosxEquipo
            # Calculamos los equipos que hay que generar
            self.numEquipos = round (self.numAlumnos/self.alumnosxEquipo)
            # Creamos los grupos vacíos
            self.equiposGenerados = list(range(self.numEquipos))
        else:
            raise ValueError("inicializaEquipos: alumnosxEquipo debe ser un valor mayor que 0")


    def _busca_equipo(self, alumno = 0):
        """Busca el alumno en los equipos generados y devuelve una lista con el equipo en el que se
        encuentra el alumno y la posición que ocupa dentro del equipo
        """
        equipo = -1
        posicion = -1
        
        for i in range(self.numEquipos):
            try:
                #Busca si existe en ese equipo
                posicion=self.equiposGenerados[i].index(alumno)
                equipo = i
                break
            except:
                pass
        
        # Lanza excepción si no se encuentra el alumno en los equipos
        if (equipo<0):
            raise ValueError("_buscaEquipo: alumno no encontrado")
        
        return [equipo,posicion]
    
    def fija_equipos (self, equipos = [0]):
        '''Indicar qué equipos se van a quedar fijos y no se van a modificar en siguientes llamadas a crearEquipos.
        Si en la lista se envían equipos que no existen, lanza una excepción.
        '''
        # comprueba que los equipos que se han pasado como parámetro están creados
        for i in equipos:
            if i >= self.numEquipos:
                raise ValueError("fijaEquipos: No existe el equipo a fijar")
        self.equiposFijos = equipos

    def _equipo_fijo(self, equipo = 0):
        """Devuelve True si el equipo pasado como parámetro es fijo"""
        try:
            self.equiposFijos.index(equipo)
            encontrado = True
        except:
            encontrado = False
            
        return encontrado
    
    def _equipos_no_fijados(self):
        """Devuelve una lista con los equipos que no han sido fijados"""
        equiposNoFijados = []
        for i in range(self.numEquipos):
                if not self._equipo_fijo(i):
                    # El equipo no está fijado
                    equiposNoFijados.append(i)

        return equiposNoFijados
    
    def _alumnos_no_fijados(self):
        """Devuelve una lista de alumnos que pertenecen a equipos que no están fijados"""
        poblacion = []
        for i in self._equipos_no_fijados():
            for j in range(len(self.equiposGenerados[i])):
                    poblacion.append(self.equiposGenerados[i][j])
        return poblacion

    def intercambia_alumnos (self, alumno1 = 0, alumno2 = 0):
        """Intercambia los dos alumnos entre sus equipos"""
        #Busca los equipos de los alumnos
        equipoAlumno1 = self._busca_equipo(alumno1)
        equipoAlumno2 = self._busca_equipo(alumno2)

        #Intercambia las posiciones
        self.equiposGenerados[equipoAlumno1[0]][equipoAlumno1[1]] = alumno2
        self.equiposGenerados[equipoAlumno2[0]][equipoAlumno2[1]] = alumno1
  

    # Elimina la lista de equipos generados
    def elimina_equipos (self):
        self.equiposGenerados = []
        self.equiposFijos = []
        self.alumnosxEquipo = 0
        self.numEquipos = 0


class TMRandom (TeamMaker):
    """Clase TMRandom
    Clase que implementa un agrupador aleatorio de alumnos.
    Es la forma más sencilla de agrupamiento y no tiene en cuenta las características recibidas de los mismos.
    """
    def __init__(self, alumnos, verbose = False, funcLog = None):
        TeamMaker.__init__(self, alumnos, verbose, funcLog)

    def crea_equipos (self, alumnosxEquipo = 1, tipoAgrupamiento = TM_ALEATORIO):
        """TMRandom.creaEquipos: Crea equipos de forma aleatoria"""
        TeamMaker.crea_equipos(self, alumnosxEquipo)

        self._log("CREAR EQUIPOS","Inicializando el agrupamiento aleatorio")

        # Si no hay equipos fijos, los genera desde cero
        if (len(self.equiposFijos)==0):
            # inicializamos
            self._log("CREAR EQUIPOS","No hay equipos fijados")
            self._inicializa_equipos(alumnosxEquipo)
            # Creamos una lista aleatoria de alumnos
            alumnosAOrdenar = sample(list(range(self.numAlumnos)),self.numAlumnos)

            # Vamos añadiendo a cada equipo el número de alumnos que debe haber en cada uno
            for i in range(self.numEquipos):
                self.equiposGenerados[i] = alumnosAOrdenar[i*self.alumnosxEquipo:self.alumnosxEquipo+self.alumnosxEquipo*i]
        else:
            # Obtenemos una lista de alumnos que pertenecen a equipos no fijados
            poblacion = self._alumnosNoFijados()
            # Desordenamos la lista
            alumnosAOrdenar = sample(poblacion,len(poblacion))
            # Los vamos añadiendo a los equipos que no están fijos
            equiposNoFijados = self._equiposNoFijados()
            self._log("CREAR EQUIPOS","Hay equipos fijados. Creando los equipos" + str(equiposNoFijados))
            indice = 0
            for i in equiposNoFijados:
                self.equiposGenerados[i] = alumnosAOrdenar[indice*self.alumnosxEquipo:self.alumnosxEquipo+self.alumnosxEquipo*indice]
                indice +=1
        self._log("CREAR EQUIPOS","Agrupamiento aleatorio finalizado")
                

class TMKmeans (TeamMaker):
    """Clase TMKmeans
    Implementa un agrupador mediante el algoritmo K-means
    Permite realizar agrupamientos teniendo en cuenta los valores que se le pasan en el constructor
    Realiza agrupamientos homogéneos y heterogéneos en función de las características de los alumnos
    
    Datos de entrada
    alumnos: Pandas dataset con las siguientes características:
        - Debe tener el valor np.nan para los valores desconocidos
        - Las columnas que son categorías deben estar 
    
    Procesado de datos
        - Antes de realizar el agrupamiento, se procesan los datos aplicando los siguientes cambios en el pipeline
        - Columnas numéricas: se sustituye el valor nulo por el más frecuente
        - Categorías ordenadas: se aplica un OrdinalEncoder convirtiendo a categorías numéricas
        - Categorías no ordenadas: se aplica un OneHotEncoder creando nuevas columnas para cada posible valor de la categorías
            En las categorías binarias se elimina una de las dos columnas generadas.
        
    
    """
    def __init__(self, alumnos, verbose = False, funcLog = None):
        TeamMaker.__init__(self, alumnos, verbose, funcLog)
        self._datasetProcesado = False

    def _procesar_dataset(self):
        # Obtenemos las columnas de cada tipo
        self._log("CREAR EQUIPOS","Alumnos: \n" + str(self.alumnos))
        
        # Columnas numéricas
        cNumericas = selector(dtype_exclude="category")(self.alumnos)

        # Columnas que corresponden a categorías
        categorias = selector(dtype_include="category")(self.alumnos)
        
        # Obtenemos los subset de categorías ordenadas y no ordenadas
        cOrdenadas = [] 
        cNoOrdenadas = []
        for columna in categorias:
            if (self.alumnos[columna].dtype.ordered):
                cOrdenadas.append(columna)
            else:
                cNoOrdenadas.append(columna)

        # Log de categorías
        self._log("PROCESAR DATASET","Categorías ordenadas: " + str(cOrdenadas))
        self._log("PROCESAR DATASET","Categorías no ordenadas: " + str(cNoOrdenadas))
        self._log("PROCESAR DATASET","Columnas numéricas: " + str(cNumericas))
        # Preparamos el pipeline

        # Las categorías ordenadas se transforman a categorías numéricas
        transformar_cat_ordenadas = Pipeline(
            steps=[
                ("ordinalEncoder", preprocessing.OrdinalEncoder())
            ]
        )  
        # Las categorías no ordenadas se transforman convirtiendo cada posible valor
        # a una nueva columna que contendrá ceros y unos
        # En caso de ser binarias, se elimina una de las dos columnas  
        transformar_cat_no_ordenadas = Pipeline(
            steps=[
                ("oneHotEncoder", preprocessing.OneHotEncoder(drop='if_binary'))
            ]
        )
        # Las categorías numéricas se transforman eliminando los valores que faltan
        # y se sustituyen por el más frecuente de cada categoría
        transformar_cat_numericas = Pipeline(
            steps=[
                ("numericas", SimpleImputer(strategy="most_frequent"))
            ]
        )
        # Se compone el procesador de columnas con todas las transformaciones anteriores
        procesadorColumnas = ColumnTransformer(
            transformers=[
                ("numericas",transformar_cat_numericas,cNumericas),
                ("ordenadas", transformar_cat_ordenadas, cOrdenadas),
                ("noOrdenadas", transformar_cat_no_ordenadas, cNoOrdenadas),
            ]
        )
    
        # Creamos un pipeline con el procesador configurado
        self._Pipeline = Pipeline(
            steps = [
                ("procesarCategorias",procesadorColumnas),
                ("normalizar", preprocessing.Normalizer(norm="l2")),
            ]
        )
    
        # Aplicamos el pipeline
        # Creamos un nuevo Pandas DataFrame con las nuevas columnas generadas tras el pipeline
        self.alumnos = pd.DataFrame(self._Pipeline.fit_transform(self.alumnos),
                                    columns = procesadorColumnas.get_feature_names_out()
                                    )
        
        # Marcamos los alumnos como procesados
        self._datasetProcesado = True



    def _equilibrar_clusters(self, clusters, maxElementos):
        # ordenamos los clusters por tamaños
        clustersOrdenados = sorted(clusters, key=lambda x:len(x), reverse=True)
        
        icMayor = 0
        icMenor = len(clustersOrdenados)-1
        clusterMayor = clustersOrdenados[icMayor]
        clusterMenor = clustersOrdenados[icMenor]
        if (len(clusterMayor) > maxElementos):
           # Quitamos los elementos que sobran y los pasamos al
            # cluster menor
           
            sobran = len(clusterMayor) - maxElementos
            
            aMover = clusterMayor[:sobran]
            del clusterMayor[:sobran]
            clustersOrdenados[icMayor] = clusterMayor
            
            clustersOrdenados[icMenor].extend(aMover)
            
            # Llamamos recursivamente
            clustersOrdenados = self._equilibrar_clusters(clustersOrdenados,maxElementos)

        # Devolvemos la lista de clusters ordenados
        return clustersOrdenados
            
    def crea_equipos (self, alumnosxEquipo = 1, tipoAgrupamiento = TM_HETEROGENEO):
        """TMKMeans.creaEquipos: Crea equipos usando el algoritmo K-Means"""
        TeamMaker.crea_equipos(self, alumnosxEquipo)  

        msgProceso = "CREAR EQUIPOS"
        self._log(msgProceso,"Inicializando agrupamiento por K-means")  
        
        # Se procesa el dataset si no se ha hecho antes
        if (not self._datasetProcesado):
            self._log(msgProceso,"Procesando las características de los alumnos")
            self._procesar_dataset()
            self._log(msgProceso,"Características de alumnos procesadas")
            self._log(msgProceso,"DataSet Normalizado" + str(self.alumnos))
       
        if (len(self.equiposFijos)==0):
            #No hay equipos generados fijos, se procesan todos los alumnos
            self._log(msgProceso,"No hay equipos fijados")
            self._inicializa_equipos(alumnosxEquipo)
            alumnosaAgrupar = list(range(self.numAlumnos))    
        else:
            #Hay equipos fijos, solo se procesan el resto
            alumnosaAgrupar = self._alumnos_no_fijados()
            self._log(msgProceso,"Hay equipos fijados")

        self._log(msgProceso,"Alumnos no fijados "+str(alumnosaAgrupar))
        
        # Filtramos nuestro panda con los alumnos a ordenar
        npAlumnosaAgrupar = self.alumnos.iloc[alumnosaAgrupar].to_numpy()
        # Obtenemos los equipos a generar
        equiposNoFijados = self._equipos_no_fijados()
        self._log(msgProceso,"Generando equipos "+str(equiposNoFijados))

        K = len(equiposNoFijados)

        # Los vaciamos
        for e in equiposNoFijados:
            self.equiposGenerados[e] = []
        
        # Realizar el algoritmo de clustering
        self._log(msgProceso,"Inicio algoritmo KMeans")
        KM = KMeans(n_clusters=K, init='k-means++', random_state=0, n_init="auto").fit(npAlumnosaAgrupar)
        self._log(msgProceso,"Fin algoritmo KMeans")

        # Obtenemos variables tras el agrupamiento
        # En esta lista tendremos el cluster al que pertenece cada alumno
        clustersDeAlumnos = KM.labels_.tolist()
            
        clusters = list(range(K))
        for c in range(K):
            clusters[c] = []
        
        for a in range(len(alumnosaAgrupar)):
            alumno = alumnosaAgrupar[a]
            cluster = clustersDeAlumnos[a]
            clusters[cluster].append(alumno)

        if (tipoAgrupamiento == TM_HETEROGENEO):
           # Agrupamiento HETEROGÉNEO
           # Recorremos los clusters y vamos asignando
           # cada alumno a un grupo diferente
            self._log(msgProceso,"Agrupamiento heterogéneo")
            e = 0
            for c in range(len(clusters)):
                for a in clusters[c]:
                    enf = equiposNoFijados[e]
                    self.equiposGenerados[enf].append(a)
                    e = (e+1) % K
                    
            print("\nEquipos generados",self.equiposGenerados)
            self._log(msgProceso,"Equipos generados")
            
        else:
            # Agrupamiento HOMOGÉNEO:
            # Los clusters ya tienen elementos homogéneos
            # Si sobran alumnos en un equipo, hay que
            # asignarlos a otro para equilibrar el número de alumnos máximo
            
            self._log(msgProceso,"Agrupamiento homogéneo")
            
            #Equilibramos clusters
            self._log(msgProceso,"Equilibrando clusters")
            clusters = self._equilibrar_clusters(clusters,self.alumnosxEquipo)        
            self._log(msgProceso,"Clusters equilibrados")

            #Asignamos los clusters a los equipos que no estaban fijados
            for c in range(len(clusters)):
                equipo = equiposNoFijados[c]
                self.equiposGenerados[equipo] = clusters[c]
            