#coding: utf-8
'''
v1_string = input()
v1 = v1_string.split(' ')
v2_string = input()
v2 = v2_string.split(' ')
resp = float(input())
soma = 0

aux2 = []
for i in range(len(v1)):
    if v1[i] == '':
        del(v1[i])
for i in range(len(aux2)):
    del v1[i]

aux2 = []
for i in range(len(v2)):
    if v2[i] == '':
        aux2.append(i)

for i in range(len(aux2)):
    del v2[i]

if len(v1) != len(v2):
    print("Erro nos dados de entrada")

else:
    for i in range(len(v1)):
        print(v1, v2)
        soma += float(v1[i]) * float(v2[i])

    if soma == resp:
        print("Sim")
    else:
        print("Não")
'''
''''''
x = int(input())
tri = []

for i in range(x+2):
    linha = []
    for j in range(i):
        if j == 0 or j == i-1:
            linha.append(1)
        else:
            linha.append(tri[len(tri)-1][j] + tri[len(tri)-1][j-1])
    if len(linha) != 0:
        tri.append(linha)

for i in tri:
    for j in i:
        print(j, end=' ')
    print()



