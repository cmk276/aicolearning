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
    alumnos: numpy array con las siguientes características:
        - Debe tener el valor np.nan para los valores desconocidos
        - Puede contener valores numéricos o cadenas, que van a ser tratadas como categorías
    
    Procesado de datos
        - Si en el np.array se detectan categorías con formato de texto, se transforman a datos numéricos
        
    
    """
    def __init(self, alumnos):
        TeamMaker.__init__(self, alumnos)

    def _codificarCategorias (self):
        """Devuelve un npArray con las categorías codificadas en números"""
        
        print ("Alumnos antes de transformar", self.alumnos)
        
        print ("Tamaño del dataset",self.alumnos.shape[1])
        columnas = self.alumnos.columns
        print ("obteniendo columnas", columnas)
        print ("Tipos de las columnas", self.alumnos.dtypes)
        
        # Estimar los valores vacíos usando el valor más frequente
        #imp = SimpleImputer(strategy="most_frequent")
        #sinnan = imp.fit_transform(self.alumnos)
        #print("Quitados los NAN\n",sinnan)
        #self.alumnos[columnas] = sinnan
        
        categoriasOrdenadas = []
        categoriasNoOrdenadas = []

        for c in columnas:
            if (self.alumnos[c].dtype=="category"):
                print ("** categoría **")
                # comprobamos si es un tipo de dato ordenado
                if (self.alumnos[c].dtype.ordered):
                    print("Categoría ordenada")
                    categoriasOrdenadas.append(c)
                else:
                    print ("Categoría NO Ordenada")
                    categoriasNoOrdenadas.append(c)
        
        print ("Categorias ordenadas detectadas:")
        print (categoriasOrdenadas)

        # Obtenemos un subset de categorías ordenadas
        co = self.alumnos[categoriasOrdenadas]
        print ("SUBSET DE CATEGORIAS ORDENADAS",co)

        # Procesamos las categorías ordenadas
        enc = preprocessing.OrdinalEncoder()
        co = enc.fit_transform(co)
        print("***",co)

        self.alumnos[categoriasOrdenadas] = co
        print("=== Alumnos transformados ===",self.alumnos)


        print ("Categorias NO ordenadas detectadas:")
        print (categoriasNoOrdenadas)

        # Obtenemos un subset de categorías ordenadas
        cno = self.alumnos[categoriasNoOrdenadas]
        print ("SUBSET DE CATEGORIAS NO ORDENADAS",cno)
        # Si son categorías binarias, elimina una de las dos opciones que crea para reducir los datos    
        enc = preprocessing.OneHotEncoder(drop='if_binary',handle_unknown='infrequent_if_exist')    
        cno = enc.fit_transform(cno).toarray()
        print("===== CATEGORIAS NO ORDENADAS TRANSFORMADAS====\n")
        print(cno)   

        print ("\nCategorías utilizadas por el OneHotEncoder\n")
        print(enc.get_feature_names_out()) 
        #Añadimos a los alumnos las nuevas categorías generadas
        self.alumnos[enc.get_feature_names_out()] = cno
        #Eliminamos las categorías no ordenadas originales
        self.alumnos=self.alumnos.drop(categoriasNoOrdenadas,axis=1)
            

            # Preparamos el pipeline para trabajar con el array de alumnos

            # Estimar los valores vacíos usando el valor más frequente
            # Convertir las categorías en datos numéricos
            #steps = [("codificador", OrdinalEncoder()),("imputador", SimpleImputer(strategy="most_frequent"))]
            #enc = Pipeline(steps)
            #alumnosAordenar = enc.fit_transform(self.alumnos)
            #print ("Alumnos procesados", alumnosAordenar)

        
    def creaEquipos (self, alumnosxEquipo = 1, tipoAgrupamiento = TM_HETEROGENEO, codificarCategorias = True):
        """TMKMeans.creaEquipos: Crea equipos usando el algoritmo K-Means"""
        TeamMaker.creaEquipos(self, alumnosxEquipo)    
        
        if (len(self.equiposFijos)==0):
            #No hay equipos generados fijos
            self._inicializaEquipos(alumnosxEquipo)

            if codificarCategorias:
                # Codificamos las categorías
                alumnosAagrupar = self._codificarCategorias()
            else:
                # **** Hay que convertirlo a Numpy
                alumnosAagrupar = self.alumnos

        else:
            # Extraer solo los alumnos que no pertenecen a equipos fijados
            pass
        # Realizar el algoritmo de clustering

        if (tipoAgrupamiento == TM_HETEROGENEO):
            # Equilibrar los equipos si el tipo de agrupamiento es TM_HETEROGENEO
            print("agrupamiento Heterogeneo")
        else:
            print("Agrumapiento homogeneo")
        
