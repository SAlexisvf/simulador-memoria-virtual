import math
from sys import set_asyncgen_hooks

M = [None] * 2048
S = [None] * 4096

PAGINA_TAM = 16
MEMORIA_TAM = 2048
SWAP_MEMORIA_TAM = 4096
ESTRATEGIA = False

pagProcess = {}
pagSwap = {}
fifoSwap = []
lruSwap = []

tiempoActual = 0
erroresPag = 0
swapsTotales = 0

def siguiente():
    sig = fifoSwap.pop() if ESTRATEGIA else lruSwap.pop()
    if(ESTRATEGIA):
        fifoSwap.insert(0, sig)
    else:
        lruSwap.insert(0, sig)
    return sig

def actualizaLRU(pagina):
    lruSwap.remove(pagina)
    lruSwap.insert(0, pagina)

def encontrarMarcoEnMemoriaSwap():
    for i in range(0,SWAP_MEMORIA_TAM,PAGINA_TAM):
        if(S[i] == None):
            return i
    return -1

def encontrarMarcoEnMemoria():
    for i in range(0,MEMORIA_TAM,PAGINA_TAM):
        if(M[i] == None):
            return i
    return -1

def cargarPagAlMarco(indice, proc, pagina):
    temp = None
    if proc != None and pagina != None:
        temp = [proc,pagina]
    for i in range(0, PAGINA_TAM):
        M[indice + i] = temp

def cargarPagAlSwap(indice, proc, pagina):
    temp = None
    if proc != None and pagina != None:
        temp = [proc,pagina]
    for i in range(0, PAGINA_TAM):
        S[indice + i] = temp

def swap(pagNueva, procNuevo, sigFrame):
    global tiempoActual
    global erroresPag

    procViejo, pagVieja = M[sigFrame]

    disponible = encontrarMarcoEnMemoriaSwap()
    if disponible == -1:
        return False

    cargarPagAlSwap(disponible, procViejo, pagVieja)

    if procViejo not in pagSwap:
        pagSwap[procViejo] = {}

    pagSwap[procViejo][pagVieja] = disponible

    del pagProcess[procViejo][pagVieja]

    cargarPagAlMarco(sigFrame, procNuevo, pagNueva)
    pagProcess[procNuevo][pagNueva] = sigFrame

    tiempoActual = tiempoActual + 20
    return True

def process(n, p):
    global erroresPag
    global swapsTotales
    global tiempoActual
    print('Running instruction P with parameters {}, {}'.format(n,p))

    if n <= 0 or n > 2048 or p < 0 or p in pagProcess:
        return
    
    marcos = []

    i = 0
    pagActual = 0
    pagProcess[p] = {}
    pagProcess[p]["inicio"] = tiempoActual
    cantPag = math.ceil(n / PAGINA_TAM)

    while pagActual < cantPag:
        if PAGINA_TAM <= i and pagActual < cantPag:
            sig = siguiente()
            swapeado = swap(pagActual,p,sig)
            if not swapeado:
                return
            pagActual += 1
            swapsTotales += 1
            marcos.append(math.floor(sig/PAGINA_TAM))
        
        while i < MEMORIA_TAM:
            if M[i] == None:
                marcos.append(math.floor(i/PAGINA_TAM))
                pagProcess[p][pagActual] = i
                if(ESTRATEGIA):
                    fifoSwap.insert(0,i)
                else:
                    lruSwap.insert(0,i)
                cargarPagAlMarco(i,p,pagActual)
                pagActual = pagActual + 1
                tiempoActual = tiempoActual + 10
                break
            
            i = i + PAGINA_TAM
    
    print("Frames ", marcos, " were assigned to the process ", p)
        



def access(d, p, m):
    global swapsTotales
    global tiempoActual
    global erroresPag
    global pagProcess
    print('Running instruction A with parameters {}, {}, {}'.format(d, p, m))

    if not p in pagProcess or d < 0 or d > len(pagProcess[p]) * PAGINA_TAM or (m != 0 and m != 1):
        print("Instruction failed, parameters not valid")
        return

    pagina = math.floor(d/PAGINA_TAM)
    fraccion, none = math.modf(d/PAGINA_TAM)
    disp = int(round(fraccion, 4) * 16)

    if pagina not in pagProcess[p]:
        if pagina not in pagSwap[p]:
            return

        sig = encontrarMarcoEnMemoria()
        erroresPag += 1

        if sig == -1:
            sig = siguiente()
            swapeado = swap(pagina, p, sig)
            if not swapeado:
                return
            else:
                swapsTotales = swapsTotales + 2
        else:
            cargarPagAlMarco(sig, p, pagina)
            pagProcess[p][pagina] = sig
            tiempoActual = tiempoActual + 11
            if ESTRATEGIA:
                fifoSwap.insert(0, sig)
            else:
                lruSwap.insert(0, sig)
            swapsTotales = swapsTotales + 1
        
        temp = pagSwap[p][pagina]
        cargarPagAlSwap(temp, None, None)
        del pagSwap[p][pagina]
    
    elif ESTRATEGIA == False:
        actualizaLRU(pagProcess[p][pagina])
    
    tiempoActual = tiempoActual + 1

    marco = pagProcess[p][pagina]
    dir = marco + disp
    print("Virtual Address: ", d, "Real Address:" , dir)
        

def free(p):
    global fifoSwap
    global lruSwap
    global pagProcess
    global pagSwap
    global tiempoActual
    print('Running instruction L with parameters {}'.format(p))

    if(pagProcess[p] == None) or "final" in pagProcess[p]:
        return
    paginas = pagProcess[p]

    for i in paginas:
        if i != "inicio":
            cargarPagAlMarco(paginas[i], None, None)
    if ESTRATEGIA:
        fifoSwap = [i for i in fifoSwap if i not in paginas.values()]
    else:
        lruSwap = [i for i in lruSwap if i not in paginas.values()]
    pagMarcos = [math.floor(paginas[i]/PAGINA_TAM ) for i in paginas.keys() if i != 'inicio']
    swapeado = {}

    if p in pagSwap:
        swapeado = pagSwap[p]
        for i in swapeado:
            cargarPagAlMarco(swapeado[i], None, None)
        
        marcosSwap = [math.floor(i/PAGINA_TAM) for i in swapeado.values()]
        print ("Frames", marcosSwap, "were freed from the swap area")
        del pagSwap[p]
    tiempoActual = tiempoActual + (len(paginas) + len(swapeado) - 1)
     
    pagProcess[p]["final"] = tiempoActual

def comment(c):
    print('Running instruction C with parameters {}'.format(c))

def finalize():
    global pagProcess
    global pagSwap
    global lruSwap
    global fifoSwap
    global erroresPag
    global swapsTotales
    global tiempoActual
    print('Running instruction F')
    procesos = 0
    promedioTurnaround = 0
    if len(pagProcess) == 0:
        return
    valores = [i for i in pagProcess if "final" not in pagProcess[i]]
    print(len(valores))
    if len(valores) > 0:
        for i in sorted(valores):
            if "final" not in pagProcess[i]:
                free(i)
    print("End:")
    for i in sorted(pagProcess.keys()):
        procesos = procesos + 1
        turnaround = (pagProcess[i]["final"] - pagProcess[i]["inicio"])/10
        print("Process: ", i, "Turnaround: ", turnaround)
        promedioTurnaround = promedioTurnaround + turnaround
    
    promedioTurnaround = promedioTurnaround / procesos

    print("Average Turnaroud:", promedioTurnaround)
    print("Page Faults:", erroresPag)
    print("Swaps:", swapsTotales)

    if ESTRATEGIA:
        fifoSwap = []
    else:
        lruSwap = []
    
    M = [None] * 2048
    S = [None] * 4096
    pagProcess = {}
    pagSwap = {}

    tiempoActual = 0
    erroresPag = 0
    swapsTotales = 0


def end():
    print('Running instruction E')
    print('Ending')
    exit()
