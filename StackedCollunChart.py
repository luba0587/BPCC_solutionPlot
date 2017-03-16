import numpy as np
import matplotlib.pyplot as plt

# variáveis globais
W = 0
fator = 1.0
data = []
files_instancias = []
inst_name = ''
itens = [0]
bins = [0]
n = 1
w_i = [0]
c_i = [0]
K = 0
solucao = []

# leitura das instâncias
def leitura_instancias():
    global files_instancias
    data = []
    file_inst = open('instance_names.txt','r')
    for line in file_inst:
        words = line.split()
        data.append(words)
    file_inst.close()

    for i in range(len(data)):
        files_instancias.append(data[i])

# leitura dos arquivos de dados
def leitura_dados(file):
    global W, itens, w_i, c_i, inst_name, n, heuristics
    W = 0
    fator = 0
    itens = [0]
    bins = [0]
    w_i = [0]
    c_i = [0]
    solucao = []

    print('\nprocessando instância ' + file + ' ...')
    inst_name = file

    data = []
    diretorio = "SaidasHI\\"
    file = open(diretorio + file,'r')
    linha_itens = 1
    for line in file:
        words = line.split()
        data.append(words)
    file.close()

    # leitura do fator, capacidade dos bins, número de bins e quantidade de itens (esses últimos em ordem inversa)
    linha_itens = 5
    fator = float(data[0][0])
    W = int(data[1][0])
    K = int(data[3][1])
    n = int(data[2][0])
    heuristics = data[3][0] #leio o tipo de heurística adotada tb
    itens[0] = n
    bins[0] = K

    # criação do array solucao
    for k in range(0,K+1):
        solucao.append([0])

    # leitura dos itens e pesos (lembrar que inverti ordem de categoria e peso!)
    bin_k = 1
    for i in range(linha_itens,len(data)):
        itens.append(int(data[i][0]))
        w_i.append(int(data[i][1]))
        c_i.append(int(data[i][2]))
        bin_k = int(data[i][3])
        solucao[bin_k][0] += int(data[i][2])
        solucao[bin_k].append(int(data[i][0]))

        # calcula o peso total dos itens na posição zero do vetor (lembrar que inverti a ordem das colunas!)
        w_i[0] += float(data[i][1])
    
    #inclui o tipo de heuristica no grafico da solucao
    Formata_dados(solucao,'Graficos/' + str(inst_name[:-4]) + 'W' + str(W) + '.png','Gráfico da solução para a ' + str(inst_name[:-4] + ' com ' + str(heuristics) ), W)

# formata os dados solução
def Formata_dados(solucao, FileName, GrafTitle, W):
    global itens, w_i, c_i
    sol_Bin = []
    sol_Itens = []
    sol_Classe = []
    
    for k in range(1,len(solucao)):
        solucao[k][::-1]
        sol_Bin.append(k)
    
    for i in range(len(itens)):
        sol_Itens.append([])
        sol_Classe.append(0)
        for k in range(len(solucao)-1):
            sol_Itens[i].append(0)

    item = 0
    for k in range(len(solucao)-1):
        ocup = int(solucao[k+1][0])
        for i in range(1,len(solucao[k+1])):
            sol_Itens[item][k] = ocup
            sol_Classe[item] = c_i[solucao[k+1][i]]
            ocup -= w_i[solucao[k+1][i]]
            item += 1

    # plota o gráfico de barras empilhadas
    BPPChart(sol_Bin,sol_Itens,sol_Classe,W,FileName,GrafTitle)

# plota o gráfico de barras empilhadas
def BPPChart(Bin,Itens,Classe,W,FileName,GrafTitle):    
    
    N = len(Bin)
    colors = ['c','r','b','g','y','m','darkblue','salmon','crimson','brown','fuchsia','c','r','b','g','y','m','darkblue','salmon','crimson','brown','fuchsia','c','r','b','g','y','m','darkblue','salmon','crimson','brown','fuchsia','c','r','b','g','y','m','darkblue','salmon','crimson','brown','fuchsia']
    ind = np.arange(N)    # the x locations for the groups
    width = 0.5       # the width of the bars: can also be len(x) sequence

    fig = plt.figure(GrafTitle)
    pl = []

    plt.clf()

    for p in range(len(Bin)):
        pl.append(plt.bar(p, W, 0.75, align='center', color='grey', label = str(p)))

    for p in range(len(Itens)):
        # o índice da cor recebe o valor da classe de conflitos do item
        i = Classe[p]
        pl.append(plt.bar(ind, Itens[p], width, align='center', color=colors[i], label = str(p)))

    plt.xlabel('Bins')
    plt.title(GrafTitle)
    plt.xticks(ind, Bin)
    fig.set_size_inches(27.0,10.5)

    fig.savefig(FileName)


# Main
leitura_instancias()

for f in range(len(files_instancias)):
    leitura_dados(str(files_instancias[f][0]))
