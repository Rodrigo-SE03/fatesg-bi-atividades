nome_completo = input("Digite seu nome completo\n")

for idx,sub_nome in enumerate(nome_completo.split()):
    print("--------------------\n")
    print(f"Nome {idx+1}: {sub_nome}")
    print("-Número de caracteres: ",len(sub_nome))
    print("-Posição: ",idx+1)
    print("-Invertido: ",sub_nome[::-1])
