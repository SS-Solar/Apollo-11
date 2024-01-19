from art import text2art
import Archivos.Configuracion.Configuracion as Config
import Archivos.Procesador.Generador as Gen


def apollo11():
    mensaje = "APOLLO_11"
    arte = text2art(mensaje, font="block")
    print(arte)
    
def bienvenido():
    mensaje = "Bienvenido A"
    arte = text2art(mensaje, font="")
    print(arte)

def menu_inicial():
        bienvenido()
        apollo11()
        Config.dispositivos()
        Config.ciclo()
        nombre= input (" ¿DESEA CONTINUAR CON LOS ANTERIORES DATOS? [y/n]: ")
        if (nombre == "n"):
                opcion =0
                while ( not (opcion == 9)):
                    opcion = input ("Que informacióm desea cambiar?\n 1. Ciclo de  tiempo (s)\n 2. Eliminar Dispositivos \n 3. Añadir un nuevo dispositivo \n 4. Cambiar cantidad minima de archivos a generar \n 5. Cambiar cantidad maxima de archivos a generar \n 6. Crear copia del ultimo reporte disponible \n 9. Seguir a la generacion de archivos \n" )
                    if opcion=="1":
                        ciclo:int = input("Ingrese nuevo ciclo de tiempo: ")
                        Config.cambiar_ciclo(float(ciclo))
                    elif opcion=="2":
                        misiones = Config.misiones()
                        print("A que mision desea eliminar un dispositivo?")
                        for i,y in enumerate(misiones):
                            print(f"{i+1}. {y}")
                        mision:int = int(input ("Ingrese opcion de misión de donde desea eliminar el dispositivo: "))
                        
                        dispositivos = Config.dispositivos_mision(mision-1)
                        print("¿Cuál dispositivo desea eliminar?")
                        for j,k in enumerate(dispositivos):
                            print(f"{j+1}. {k}")
                        dispositivo:int = int(input("Ingrese opcion del dispositivo que desea eliminar: "))
                        Config.eliminar_dispositivo(misiones[mision-1],dispositivo-1)
                        #Config.cambiar_ciclo(float(ciclo))
                        #Eliminar dispositvo de mision especifica
                    elif opcion=="3":
                        #mision = int(input ("A que mision dese añadir un dispositivo?\n 1. ColonyMoon \n 2. GalaxyTwo \n 3. OrbitOne \n 4. VacMars\n"))
                        misiones = Config.misiones()
                        print("A que mision desea añadir un dispositivo?")
                        for i,y in enumerate(misiones):
                            print(f"{i+1}. {y}")
                        mision = int(input("(ingrese un número de opción): "))
                        dispositivo = input (" Ingrese el nombre del nuevo dispositivo:  ")
                        #mision_aux = Config.misiones() 
                        mision = misiones[mision-1]
                        Config.nuevo_dispositivo (mision,dispositivo)
                    elif opcion=="4":
                        cantidad_min_archivos:int = int(input ("Ingrese nueva cantidad minima de archivos a generar: "))
                        Config.cambiar_min_archivos(cantidad_min_archivos)
                    elif opcion=="5":
                        cantidad_max_archivos:int = int(input ("Ingrese nueva cantidad maxima de archivos a generar: "))
                        Config.cambiar_max_archivos(cantidad_max_archivos)
                    elif opcion=="6":
                        Config.Crear_copia()
                        print("Copia creada con exito")
                    elif opcion=="9":
                        break
                    else: 
                        print("Opcion erronea, intentalo otra vez")
                    

          
          
     

