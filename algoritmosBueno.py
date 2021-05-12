#Conexión con BBDD
import bbdd
#Operaciones matemáticas (raiz)
import math

# PRE { Parametros de entrada: userId y un listado de peliculas}
# POST { Devuelve una sentencia que calcula la media de las valoraciones realizadas por userId para el listado de peliculas pasadas por parametro}
def mediaSentencia(user, pelis):
    sentencia='SELECT avg(rating) from rating WHERE userId ='+str(user)+' and ('  ##
    for i in pelis:
        sentencia+='movieId = '+str(i)+' or '
    sentencia=sentencia[:-3] # Se borra el ultimo ' or ' para obtrener una sentencia correcta y ejecutable
    sentencia+=')' # Se finaliza la sentencia para ser ejetuada
    return sentencia
# PRE { Parametros de entrada: userId, movieId, UMBRAL DE SIMILITUD(recogido de la interfaz, por defecto -1)}
# POST { Devuelve la PREDICCION sobre la pelicula yu el usuario pasados por parametros}
def prediccion(u,p,umbral=-1):
    numerador = 0
    denominador = 0
    votadas = bbdd.votadas(u)   # Consulta que devuelve las peliculas votadas por un usuario
    for i in range(len(votadas)):  # Calculamos la similitud entre las peliculas votadas por el usuario y la pelicula pasados por parametros
        similitud = sim(votadas[i][0],p)
        if similitud >= umbral:  # Se comprueba que la similitud calculada cumpla la condición
            # Si TRUE realiza la prediccion, si FLASE pasa a la siguiente iteracion (Siguiente pelicula votada)
            print(similitud,'>',umbral)
            numerador += similitud * votadas[i][1]
            denominador += similitud
    return numerador/denominador

def prediccion_vecindario(u,p,vecindario):
    numerador = 0
    denominador = 0
    votadas = bbdd.votadas(u)
    lista = []
    for i in range(len(votadas)):
        similitud = sim(votadas[i][0],p)
        lista.append((similitud, votadas[i][1]))
    lista.sort(key=lambda tup: tup[0], reverse=True)
    for i in range(0,vecindario):
        numerador += lista[i][0] * lista[i][1] 
        denominador += lista[i][0]
    return numerador/denominador

# PRE { Parametros de entrada: movieId (pelicula votada), movieId (pelicula a predecir)}
# POST { Devuelve un valor [-1 , 1] -> similitud entre ambas peliculas}
def sim(movie1,movie2):
    # Ambas listas tienen mismo tamaño y mismo orden
    # Obtenemos una lista de tuplas (rating, userId) de aquellos usuarios que han votado ambas peliculas, siendo el rating sobre la pelicula ("mid1")
    ratings1 = bbdd.sameEnery(movie1,movie2)  
    # Obtenemos una lista de tuplas (rating, userId) de aquellos usuarios que han votado ambas peliculas, siendo el rating sobre la pelicula ("mid2")
    ratings2 = bbdd.sameEnery(movie2,movie1)
    numerador=0
    denominadorIzq=0 
    denominadorDer=0
    denominador=0
    #  consulta para obtener la lista de peliculas en comun de aquellos usuarios que han votado las peliculas "movie1" y "movie2" (pasadas por parametro)
    sentencia='SELECT movieId FROM rating WHERE userId = '+str(ratings1[0][1])+' and userId IN (SELECT userId FROM rating WHERE movieId='+str(movie1)+' AND userId IN (SELECT userId FROM rating WHERE movieId='+str(movie2)+'))'
    for j in ratings1:
        #  Construimos la sentencia mediante INTERSECT para ir eliminando de la lista aquellas peliculas que no hayan visto todos los usuarios válidos
        sentencia+='INTERSECT SELECT movieId FROM rating WHERE userId = '+str(j[1])+' and userId IN (SELECT userId FROM rating WHERE movieId='+str(movie1)+' AND userId IN (SELECT userId FROM rating WHERE movieId='+str(movie2)+'))'
    pelisComunes = bbdd.commonFilms(sentencia)
    notaPonderada1 = []
    notaPonderada2 = []

    for i in range(len(ratings1)):
        print(i,'.')
        # Calculamos las valoraciones ponderadas de cada pelicula, para todos los usuarios válidos
        # Siguiendo la formula: vp = valoracion - media de valoraciones (del usuario que ha hecho esa valoración)
        notaPonderada1.append(ratings1[i][0] - bbdd.media(mediaSentencia(ratings1[i][1],pelisComunes)))
        notaPonderada2.append(ratings2[i][0] - bbdd.media(mediaSentencia(ratings2[i][1],pelisComunes)))
        # Se construye el numerador y el denominador de la formula SIMILITUD DEL COSENO
        numerador+=notaPonderada1[i]*notaPonderada2[i]
        denominadorIzq+=notaPonderada1[i]**2
        denominadorDer+=notaPonderada2[i]**2
    denominador=math.sqrt(denominadorIzq)*math.sqrt(denominadorDer)
    # Se devuelve la similitud
    return numerador/denominador

# iid=5
uid = 2
# votadas = bbdd.votadas(uid)
# noVotadas =bbdd.noVotadas(uid) 

# for i in bbdd.noVotadas(uid):
#     print(prediccion(uid,i))

# sim(1,3)
print(round(sim(1,3),2))
# la 1 y la 14
# la 1 y la 3
# la 1 y la 456
# la 1 y la 6547 pensarla

# print(round(prediccion(147,1,),2))
# usuario 53