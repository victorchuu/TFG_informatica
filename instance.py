
""" CONSTANTES """

MAX_ACTORES = 1
MAX_TESTIGOS = 25
MAX_TESTIMONIOS_POR_TESTIGO = 1

MAX_ACTORES_POR_TESTIMONIO = 1
MAX_LUGARES_POR_TESTIMONIO = 3
MAX_INTERVALO_DE_TIEMPO = 15
MAX_LONGITUD_INTERVALO = 4
PROPORCION_TESTIMONIOS_NEGADOS = 0

MAX_VERTICES = 10
MAX_ARISTAS = MAX_VERTICES*(MAX_VERTICES-1)
MAX_DISTANCIA_ARISTA = 9

NUM_CASOS = 1 # Numero de casos a crear

NO_DIRIGIDO = True;

import random

class Arista :
    
    def __init__(self, v = -1, d = -1) :
        self.vertice = v
        self.distancia = d
        
    def __gt__(self,other) :
        return self.distancia > other.distancia


class Visita :
    
    def __init__(self, p, ini, fin) :
        self.persona = p
        self.a = ini
        self.b = fin

    def __lt__(self,other) :
        return self.a < other.a


class Grafo :
    
    def __init__(self) :
        self.V = 0
        self.E = 0
        self.adyList = []
        self.floydListo = False
        self.adyMat = []
        self.camino = []
        
    def leer(self, file) :
        
        line = file.readline().split()
        self.V, self.E = int(line[0]), int(line[1])

        self.adyList = [[] for _ in range(self.V)]


        for i in range(self.E):
            line = file.readline().split()
            u = int(line[0])
            v = int(line[1])
            d = int(line[2])

            if u >= self.V or v >= self.V or d <= 0:
                print("Grafo incorrecto, arista: ",u,' --> ',v,'(',d,')')
            
            self.adyList[u].append(Arista(v,d))
            
    def escribir(self) : 
        print('Vertices: ', self.V, 'Aristas: ',self.E)
        for i in range(len(self.adyList)) :
            for arista in self.adyList[i] :
                print(i,' --> ', arista.vertice,' (', arista.distancia,')')
                
    def Floyd(self) :
        infinito = 1000000000
        V = self.V

        # Transformamos la lista de adyacencia a matriz de adyacencia
        self.adyMat = [ [infinito for _ in range(V)] for _ in range(V) ]

        for v in range(V) :
            for arista in self.adyList[v] : 
                self.adyMat[v][arista.vertice] = arista.distancia
            self.adyMat[v][v] = 0

        # Iniciamos la matriz para reconstruir caminos

        self.camino = [ [0 for _ in range(V)] for _ in range(V) ]

        for i in range(V) :
            for j in range(V) :
                self.camino[i][j] = i

        # Aplicamos el algoritmo de floyd sobre la matriz de adyacencia calculada

        for k in range(V) :
            for i in range(V) :
                for j in range(V) :
                    if self.adyMat[i][k] + self.adyMat[k][j] < self.adyMat[i][j] :
                        self.adyMat[i][j] = self.adyMat[i][k] + self.adyMat[k][j]
                        self.camino[i][j] = self.camino[k][j]
        self.floydListo = True;
                
    def dist(self, u, v) :
        if not self.floydListo :
            self.Floyd()
        return self.adyMat[u][v]


    """ Recibe una ruta que termina en el vertice src y calcula un camino para llegar a ella en tiempo t"""

    def reconstruir(self, src, dst, t, R) :
        if not self.floydListo :
            self.Floyd()
        if src != dst :
            k = self.camino[src][dst]
            self.reconstruir(src, k , 0, R);
            R.vertices.append(dst); 
            R.tiempo.append(0);
            R.dist.append(self.adyMat[k][dst])
        if t != 0 :
            R.tiempo[-1] += t - self.adyMat[src][dst]

    def grafo_random(self, V) :
        self.V = V;
        self.adyList = [[] for _ in range(V)]
        self.E = random.randint(0, min(V*(V-1) , MAX_ARISTAS) )
        if NO_DIRIGIDO and self.E % 2 == 1 :
            self.E += 1

        i = 0

        while i < self.E :
            u = random.randint(0, V-1)
            v = random.randint(0, V-1)
            repetido = u == v
            for arista in self.adyList[u] :
                if v == arista.vertice :        # TODO : Mejorar esto 
                    repetido = True;
            
            if(repetido) :  # No admitimos aristas repetidas, ni aristas de un vertice a si mismo
                continue;

            distancia = random.randint(1, MAX_DISTANCIA_ARISTA )
            i += 1
            self.adyList[u].append(Arista(v,distancia))
            if(NO_DIRIGIDO) :
                i += 1;
                self.adyList[v].append(Arista(u,distancia))
            

    def __str__(self) :

        string = str(self.V) + ' ' + str(self.E) + '\n'

        for v in range(len(self.adyList)) :
            for arista in self.adyList[v] :
                string += str(v) + ' ' + str(arista.vertice) + ' ' + str(arista.distancia) + '\n'

        return string

    

class Testimonio :
    
    def __init__(self, actores = [], lugares = [], a = 0, b = 0) :
        self.actores = actores
        self.lugares = lugares
        self.a = a
        self.b = b
        self.negado = False

    def leer(self, file) :

        self.negado = file.readline() == 'N'

        self.actores = [int(x) for x in file.readline().split()]
        del self.actores[0]
        
        self.lugares = [int(x) for x in file.readline().split()]
        del self.lugares[0]
        
        line = file.readline().split()
        self.a, self.b = int(line[0]), int(line[1])
        return self.b

    def __str__(self) :
        string = ''
        if self.negado :
            string += ('N\n')
        else :
            string += ('Y\n')

        string += str(len(self.actores))
        for elem in self.actores :
            string += ' '+str(elem)

        string += '\n'+str(len(self.lugares))
        for elem in self.lugares :
            string += ' '+str(elem)

        return string + '\n' + str(self.a) + ' ' + str(self.b) + '\n'
        
    def escribir(self) :
        if self.negado :
            neg = '┐'
        else :
            neg = ' '
        print(neg,'     Actores: ',self.actores, '     Lugares: ', self.lugares,'     Intervalo: [',self.a ,', ', self.b,']')

    def __lt__(self, other) :
        return self.a < other.a

    def testimonio_random(self, n_actores, n_lugares, a, b, MAX_ACTORES_TEST, MAX_LUGARES_TEST) :
        n = random.randint(1 , MAX_ACTORES_TEST);
        self.actores = []*n
        for i in range(n) :
            self.actores.append( random.randint(0, n_actores-1) )
        

        n = random.randint(1 , MAX_LUGARES_TEST);
        self.lugares = []*n
        for i in range(n) :
            self.lugares.append( random.randint(0, n_lugares-1) )

        self.a = a
        self.b = b
        if random.uniform(0, 1) < PROPORCION_TESTIMONIOS_NEGADOS :
            self.negado = True



class WP :
    
    def __init__(self) :
        self.grafo = Grafo()
        
        self.testimonios = []
        
        ## testimonios[i] es la lista de testimonios de la persona P_i
        self.num_actores = 0
        self.M = 0
        # M es el tiempo maximo que aparece en los testimonios
        

    def leer(self, file) :
        self.grafo.leer(file)
        
        num_testigos = int(file.readline())
    
        self.testimonios = [[] for _ in range(num_testigos)]
    
        for i in range(num_testigos) :
            num_testimonios = int(file.readline())
            
            for j in range(num_testimonios) :
                self.testimonios[i].append( Testimonio() )
                t = self.testimonios[i][j].leer(file)
                if t > self.M :
                    self.M = t

    def escribir(self) :
        self.grafo.escribir()
        print('Numero de testigos: ', len(self.testimonios))

        for i in range(len(self.testimonios)) : 
            print('El testigo ',i,' tiene ', len(self.testimonios[i]), ' testimonios')
            for testim in self.testimonios[i] :
                testim.escribir()

    def instancia_random(self) :
        V = random.randint(1, MAX_VERTICES)
        self.grafo.grafo_random(V)
        num_actores = random.randint(1, MAX_ACTORES)
        self.testigos_random( random.randint(1, MAX_TESTIGOS) , num_actores)


    def testigos_random(self, testigos, actores) :
        self.num_actores = actores
        MAX_ACTORES_TEST = min(actores     , MAX_ACTORES_POR_TESTIMONIO)
        MAX_LUGARES_TEST = min(self.grafo.V, MAX_LUGARES_POR_TESTIMONIO)

        self.testimonios = [[] for _ in range(testigos)]



        for testigo in range(testigos) :
            num_testimonios = random.randint(1 , MAX_TESTIMONIOS_POR_TESTIGO)
            tiempos = [0]*(2*num_testimonios) 
            # Creamos los tiempos de forma distinta segun la version del problema

            for i in range(num_testimonios) :
                longitud = random.randint(0 , MAX_LONGITUD_INTERVALO)
                tiempos[2*i] = random.randint(0, MAX_INTERVALO_DE_TIEMPO - longitud)
                tiempos[2*i + 1] = tiempos[2*i] + longitud

            self.testimonios[testigo] = [ Testimonio() for _ in range(num_testimonios) ]
            for j in range(num_testimonios) :
                self.M = max(self.M, tiempos[2*j + 1])
                self.testimonios[testigo][j].testimonio_random(actores,self.grafo.V,tiempos[2*j],tiempos[2*j+1],MAX_ACTORES_TEST,MAX_LUGARES_TEST)

    def __str__(self) :
        string = str(self.grafo)

        string += str(len(self.testimonios)) + '\n'

        for testigo in self.testimonios :
            string += str(len(testigo)) + '\n'
            for tes in testigo :
                string += str(tes)

        return string

def generar_archivo(nombre , casos = 1 , vertices = 10, distancia = 9, testigos = 20, testimonios_por_testigo = 1,
 M = 20, intervalo_testimonio = 5, lugares_por_testimonio = 1, proporcion_testimonios_negados = 0) :
    global MAX_VERTICES
    MAX_VERTICES = vertices

    global MAX_DISTANCIA_ARISTA
    MAX_DISTANCIA_ARISTA = distancia

    global MAX_TESTIGOS
    MAX_TESTIGOS = testigos

    global MAX_TESTIMONIOS_POR_TESTIGO
    MAX_TESTIMONIOS_POR_TESTIGO = testimonios_por_testigo

    global MAX_INTERVALO_DE_TIEMPO
    MAX_INTERVALO_DE_TIEMPO = M

    global MAX_LONGITUD_INTERVALO
    MAX_LONGITUD_INTERVALO = intervalo_testimonio

    global MAX_LUGARES_POR_TESTIMONIO
    MAX_LUGARES_POR_TESTIMONIO = lugares_por_testimonio

    global PROPORCION_TESTIMONIOS_NEGADOS
    PROPORCION_TESTIMONIOS_NEGADOS = proporcion_testimonios_negados


    string = str(casos) + '\n'

    for _ in range(casos) :
        instancia = WP()
        instancia.instancia_random()
        string += str(instancia)
            

    with open('test_cases/' + nombre,'w') as f:
        f.write(string)