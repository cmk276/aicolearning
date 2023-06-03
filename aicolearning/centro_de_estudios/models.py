from django.db import models

class Persona(models.Model):
    nombre = models.CharField("nombre", max_length=50)
    apellido1 = models.CharField("primer apellido", max_length=50)
    apellido2 = models.CharField("segundo apellido", max_length=50)
    email = models.EmailField
    f_nac = models.DateField(("fecha de nacimiento"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.nombre+self.apellido1+self.apellido2
    
class Alumno(Persona):
    grupos = models.ManyToManyField("Grupo")
    def __str__(self):
        return self.nombre+self.apellido1+self.apellido2
    
class Profesor(Persona):
    dni = models.CharField("DNI", max_length=9)

class CentroDeEstudios(models.Model):
    nombre = models.CharField("centro de estudios", max_length=150)
    url = models.URLField("URL")
    observaciones = models.TextField
    alumnos = models.ManyToManyField(Alumno, through="MatriculaAlumno")
    profesores = models.ManyToManyField(Profesor, through="ProfesorEmpleado")

    def __str__(self):
        return self.nombre
    
class MatriculaAlumno(models.Model):
    centroDeEstudios = models.ForeignKey(CentroDeEstudios, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    matricula = models.CharField("matrícula", max_length=10,unique=True)
    fecha_alta = models.DateField(("fecha de alta"), auto_now=False, auto_now_add=True)
    fecha_baja = models.DateField(("fecha de baja"), auto_now=False, auto_now_add=False)

class ProfesorEmpleado(models.Model):
    centroDeEstudios = models.ForeignKey(CentroDeEstudios, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    fecha_alta = models.DateField(("fecha de alta"), auto_now=False, auto_now_add=True)
    fecha_baja = models.DateField(("fecha de baja"), auto_now=False, auto_now_add=False)

class Estudio(models.Model):
    centroDeEstudios = models.ForeignKey(CentroDeEstudios, on_delete=models.CASCADE)
    nombre = models.CharField("estudio", max_length=150)
    observaciones = models.TextField
    def __str__(self):
        return self.nombre
    
class Curso(models.Model):
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE)
    nombre = models.CharField("curso", max_length=150)
    descripcion = models.TextField("descripción")
    grupos = models.ManyToManyField("Grupo")
    def __str__(self):
        return self.nombre
    
class Asignatura(models.Model):
    cursos = models.ManyToManyField(Curso)
    nombre = models.CharField("curso", max_length=150)
    descripcion = models.TextField("descripción")
    def __str__(self):
        return self.nombre
    
class Grupo(models.Model):
    f_inicio = models.DateField(("fecha de inicio"), auto_now=False, auto_now_add=True)
    f_fin = models.DateField(("fecha de fin"), auto_now=False, auto_now_add=False)
    seccion =  models.CharField("sección", max_length=10)   
    descripcion = models.TextField("descripción")
    alumnos = models.ManyToManyField(Alumno)
    profesores = models.ManyToManyField(Profesor)
    curso_grupo = models.ForeignKey(Curso, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

