from Mapa import Mapa

M=Mapa()
#metodo que lea y rellene la lista de ciudades
def rellenamatriz(mapa):
    if not mapa.ciudades:
        print("no hay ciudades lista vacia")
        exit()
    else:
        for i in range(len(mapa.ciudades)):
            for j in range(i+1,len(mapa.ciudades)):
                    mapa.matriz_distancias[i][j]=mapa.calculadistancia(mapa.ciudades[i],mapa.ciudades[j])
                    mapa.matriz_distancias[j][i] = mapa.calculadistancia(mapa.ciudades[i], mapa.ciudades[j])

