"""Módulo TeamMaker

Incluye la definición de clases para realizar agrupamientos de alumnos
TMRandom -> Agrupamientos aleatorios
TMKmeans -> Agrupamientos homogéneos o heterogéneos mediante el algoritmo K-means

Atributos:
alumnosxEquipo -> Indica el nº máximo de alumnos que puede haber en cada equipo (solo lectura)

Tipos de agrupamiento:
TM_HETEROGENEUS = Agrupamiento heterogéneo
TM_HOMOGENEUS = Agrupamiento homogéneo
"""
from abc import ABC, abstractmethod
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
#from sklearn.preprocessing import OrdinalEncoder
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from random import *

# CONSTANTES
TM_HOMOGENEO = 0
TM_HETEROGENEO = 1

# CLASES
class TeamMaker(ABC) :
    """Clase TeamMaker
    Clase abstracta que define la funcionalidad básica de un agrupador de alumnos.
    La clase se inicializa con un array de vectores con información sobre los alumnos a agrupar.
    Permite generar grupos, dejar unos grupos fijos (para poder reagrupar otros), 
    intercambiar alumnos entre grupos... etc.
    """

#Métodos
    def __init__(self, alumnos):
        self.alumnos = alumnos
        self.equiposGenerados = []
        self.equiposFijos = []
        self.alumnosxEquipo = 0
        self.numEquipos = 0
        self.numAlumnos = 0

    
    def _inicializaEquipos(self, alumnosxEquipo = 1):
        """
        Inicializa la lista equiposGenerados añadiendo un elemento por cada equipo.
        Calcula el número de equipos que deben generarse
        """
        self.numAlumnos = len(self.alumnos)
        if (alumnosxEquipo > self.numAlumnos):
            raise ValueError("inicializaEquipos: alumnnosxEquipo es mayor que el número de alumnos")
        
        if (alumnosxEquipo > 0):
            self.alumnosxEquipo = alumnosxEquipo
            # Calculamos los equipos que hay que generar
            self.numEquipos = round (self.numAlumnos/self.alumnosxEquipo)
            # Creamos los grupos vacíos
            self.equiposGenerados = list(range(self.numEquipos))
        else:
            raise ValueError("inicializaEquipos: alumnosxEquipo debe ser un valor mayor que 0")


    def _buscaEquipo(self, alumno = 0):
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
    
        
    def creaEquipos (self, alumnosxEquipo = 1):
        pass

    
    def fijaEquipos (self, equipos = [0]):
        '''Indicar qué equipos se van a quedar fijos y no se van a modificar en siguientes llamadas a crearEquipos.
        Si en la lista se envían equipos que no existen, lanza una excepción.
        '''
        # comprueba que los equipos que se han pasado como parámetro están creados
        for i in equipos:
            if i >= self.numEquipos:
                raise ValueError("fijaEquipos: No existe el equipo a fijar")
        self.equiposFijos = equipos

    def _equipoFijo(self, equipo = 0):
        """Devuelve True si el equipo pasado como parámetro es fijo"""
        try:
            self.equiposFijos.index(equipo)
            encontrado = True
        except:
            encontrado = False
            
        return encontrado
    
    def _equiposNoFijados(self):
        """Devuelve una lista con los equipos que no han sido fijados"""
        equiposNoFijados = []
        for i in range(self.numEquipos):
                if not self._equipoFijo(i):
                    # El equipo no está fijado
                    equiposNoFijados.append(i)

        return equiposNoFijados
    
    def _alumnosNoFijados(self):
        """Devuelve una lista de alumnos que pertenecen a equipos que no están fijados"""
        poblacion = []
        for i in self._equiposNoFijados():
            for j in range(len(self.equiposGenerados[i])):
                    poblacion.append(self.equiposGenerados[i][j])
        return poblacion

    def intercambiaAlumnos (self, alumno1 = 0, alumno2 = 0):
        """Intercambia los dos alumnos entre sus equipos"""
        #Busca los equipos de los alumnos
        equipoAlumno1 = self._buscaEquipo(alumno1)
        equipoAlumno2 = self._buscaEquipo(alumno2)

        #Intercambia las posiciones
        self.equiposGenerados[equipoAlumno1[0]][equipoAlumno1[1]] = alumno2
        self.equiposGenerados[equipoAlumno2[0]][equipoAlumno2[1]] = alumno1
  

    # Elimina la lista de equipos generados
    def eliminaEquipos (self):
        self.equiposGenerados = []
        self.equiposFijos = []
        self.alumnosxEquipo = 0
        self.numEquipos = 0


class TMRandom (TeamMaker):
    """Clase TMRandom
    Clase que implementa un agrupador aleatorio de alumnos.
    Es la forma más sencilla de agrupamiento y no tiene en cuenta las características recibidas de los alumnos.
    """
    def __init__(self, alumnos):
        TeamMaker.__init__(self, alumnos)

    def creaEquipos (self, alumnosxEquipo = 1):
        """TMRandom.creaEquipos: Crea equipos de forma aleatoria"""
        TeamMaker.creaEquipos(self, alumnosxEquipo)
        # Si no hay equipos fijos, los genera desde cero
        if (len(self.equiposFijos)==0):
            # inicializamos
            self._inicializaEquipos(alumnosxEquipo)
            # Creamos una lista aleatoria de alumnos
            alumnosAOrdenar = sample(list(range(self.numAlumnos)),self.numAlumnos)

            # Vamos añadiendo a cada equipo el número de alumnos que hay en cada uno
            for i in range(self.numEquipos):
                self.equiposGenerados[i] = alumnosAOrdenar[i*self.alumnosxEquipo:self.alumnosxEquipo+self.alumnosxEquipo*i]
        else:
            # Obtenemos una lista de alumnos que pertenecen a equipos no fijados
            poblacion = self._alumnosNoFijados()
            # Desordenamos la lista
            alumnosAOrdenar = sample(poblacion,len(poblacion))
            # Los vamos añadiendo a los equipos que no están fijos
            equiposNoFijados = self._equiposNoFijados()
            indice = 0
            for i in equiposNoFijados:
                self.equiposGenerados[i] = alumnosAOrdenar[indice*self.alumnosxEquipo:self.alumnosxEquipo+self.alumnosxEquipo*indice]
                indice +=1
                

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
    def __init__(self, alumnos):
        TeamMaker.__init__(self, alumnos)
        self._datasetProcesado = False

    def _procesarDataset(self):
        # Obtenemos las columnas de cada tipo
        
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
                ("procesarCategorias",procesadorColumnas)
            ]
        )
    
        # Aplicamos el pipeline
        # Creamos un nuevo Pandas DataFrame con las nuevas columnas generadas tras el pipeline
        self.alumnos = pd.DataFrame(self._Pipeline.fit_transform(self.alumnos),
                                    columns = procesadorColumnas.get_feature_names_out()
                                    )
        
        # Marcamos los alumnos como procesados
        self._datasetProcesado = True

    def creaEquipos (self, alumnosxEquipo = 1, tipoAgrupamiento = TM_HETEROGENEO, codificarCategorias = True):
        """TMKMeans.creaEquipos: Crea equipos usando el algoritmo K-Means"""
        TeamMaker.creaEquipos(self, alumnosxEquipo)    
        
        # Se procesa el dataset si no se ha hecho antes
        if (not self._datasetProcesado):
            print("\nProcesando dataset")
            self._procesarDataset()
       
        if (len(self.equiposFijos)==0):
            #No hay equipos generados fijos, se procesan todos los alumnos
            print("\nNo hay equipos fijos\n")
            self._inicializaEquipos(alumnosxEquipo)
            alumnosaAgrupar = list(range(self.numAlumnos))    
        else:
            #Hay equipos fijos, solo se procesan el resto
            alumnosaAgrupar = self._alumnosNoFijados()

        print("\nAlumnos a mezclar: ", alumnosaAgrupar)
        
        # Filtramos por los alumnos a ordenar
        npAlumnosaAgrupar = self.alumnos.iloc[alumnosaAgrupar].to_numpy()
        # Obtenemos los equipos a generar
        K = len(self._equiposNoFijados())
        print("\n Alumnos a Agrupar: ",npAlumnosaAgrupar)
        print("\nEquipos a generar ",K)

        # Realizar el algoritmo de clustering
        KM = KMeans(n_clusters=K, init='k-means++', random_state=0, n_init="auto").fit(npAlumnosaAgrupar)

        # Obtenemos variables tras el agrupamiento
        # En esta lista tendremos el cluster al que pertenece cada alumno
        clustersDeAlumnos = KM.labels_.tolist()
        
        # Creamos la lista de clusters
        clusters = list(range(K))
        for c in range(K):
            clusters[c] = []
        
        for alumno in range(len(npAlumnosaAgrupar)):
            cluster = clustersDeAlumnos[alumno]
            clusters[cluster].append(alumno)
            
        print ("clusters asignados: ",clusters)


        if (tipoAgrupamiento == TM_HETEROGENEO):
           # Agrupamiento HETEROGÉNEO
           # Hay que ir repartiendo a los alumnos por
           # diferentes equipos
            
            print("agrupamiento Heterogeneo")
        else:
            # Agrupamiento HOMOGÉNEO:
            # Los clusters ya tienen elementos homogéneos
            # Si sobran alumnos en un equipo, hay que
            # asignarlos a otro
            print("Agrumapiento homogeneo")
        
