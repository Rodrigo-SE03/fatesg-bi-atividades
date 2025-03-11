nome_completo = input("Digite seu nome completo\n")
pos = 1
for sub_nome in nome_completo.split():
    print("--------------------")
    print(sub_nome)
    print("Posição no nome: ",pos)
    print("Número de caracteres: ",len(sub_nome))
    print("Nome invertido: ",sub_nome[::-1])
    pos+=1
