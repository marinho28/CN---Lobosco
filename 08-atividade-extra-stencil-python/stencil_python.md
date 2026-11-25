# Stencil de Python — Comandos Básicos

## 1. Variáveis e Tipos
```python
nome = "Felipe"             # str
idade = 20                  # int
altura = 1.75               # float
ativo = True                # bool
nada = None                 # NoneType

type(idade)                 # descobre o tipo
int("10")                   # converte para int
str(10)                     # converte para str
float("3.14")               # converte para float
```

## 2. Entrada e Saída
```python
print("Olá, mundo")
print("Nome:", nome, sep=" | ", end="\n")
x = input("Digite algo: ")  # sempre retorna str
```

## 3. Operadores
```python
+  -  *  /  //  %  **       # aritméticos (// divisão inteira, % resto, ** potência)
== != > < >= <=             # comparação
and  or  not                # lógicos
+= -= *= /=                 # atribuição composta
```

## 4. Estruturas Condicionais
```python
if idade >= 18:
    print("Maior de idade")
elif idade == 17:
    print("Quase lá")
else:
    print("Menor de idade")
```

## 5. Laços de Repetição
```python
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for item in [10, 20, 30]:   # percorre uma lista
    print(item)

i = 0
while i < 5:
    print(i)
    i += 1

# controle de fluxo
break                       # interrompe o laço
continue                    # pula para a próxima iteração
```

## 6. Estruturas de Dados

**Lista** (mutável, ordenada)
```python
lista = [1, 2, 3]
lista.append(4)             # adiciona no final
lista.remove(2)             # remove o valor 2
lista[0]                    # acessa por índice
lista[-1]                   # último elemento
lista[1:3]                  # slicing
len(lista)                  # tamanho
```

**Tupla** (imutável, ordenada)
```python
tupla = (1, 2, 3)
```

**Dicionário** (chave-valor)
```python
d = {"nome": "Felipe", "idade": 20}
d["nome"]                   # acessa pela chave
d["curso"] = "CComp"        # adiciona/atualiza
d.keys()                    # chaves
d.values()                  # valores
d.items()                   # pares (chave, valor)
```

**Conjunto** (sem duplicatas, sem ordem)
```python
s = {1, 2, 3}
s.add(4)
```

## 7. Funções
```python
def somar(a, b):
    return a + b

def saudacao(nome="visitante"):    # valor padrão
    return f"Olá, {nome}"

# função lambda (anônima)
dobro = lambda x: x * 2
```

## 8. Strings úteis
```python
s = "Python"
s.upper()                   # MAIÚSCULAS
s.lower()                   # minúsculas
s.strip()                   # remove espaços nas pontas
s.split(",")                # separa em lista
s.replace("P", "J")         # troca trechos
f"{nome} tem {idade} anos"  # f-string
len(s)                      # tamanho
```

## 9. Tratamento de Erros
```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Não pode dividir por zero")
finally:
    print("Executa sempre")
```

## 10. Módulos
```python
import math
math.sqrt(16)

from random import randint
randint(1, 10)
```

## 11. Compreensão de Lista (list comprehension)
```python
quadrados = [x**2 for x in range(10)]
pares = [x for x in range(10) if x % 2 == 0]
```

## 12. Classes (Orientação a Objetos, básico)
```python
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def apresentar(self):
        return f"Sou {self.nome}, tenho {self.idade} anos"

p = Pessoa("Felipe", 20)
p.apresentar()
```
