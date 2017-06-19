import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[1;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[1;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

def printCores(n, texto, cor) :
  n=str(n)
  print(cor + n + RESET, cor + texto + RESET)

def adicionar(descricao, extras):
  if descricao  == '' :
    return False
  else:
    primeiroEx=""
    segundoEx=""
    for x in extras:
      if dataValida(x) or horaValida(x):
        primeiroEx+=x+" "
      elif prioridadeValida(x):
        primeiroEx+=x.upper()+" "
      elif contextoValido(x) or projetoValido(x):
        segundoEx+=x+" "
    novaAtividade=primeiroEx+descricao+" "+segundoEx
   
  try: 
    fp = open("todo.txt", 'a')
    fp.write(novaAtividade+"\n")
    fp.close()
    fp=open("todo.txt",'r')
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + "todo.txt")
    print(err)
    return False
 
  return True

def prioridadeValida(pri):
  alfabeto="ABCDEFGHIJKLMNOPKRSTUVWXYZ"
  if len(pri)!=3:
    return False
  elif pri[0]!="(" and pri[2]!=")":
    return False
  for letra in alfabeto:
    if pri[1].upper()==letra:
      return True
  return False

def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    hora=int(horaMin[0])+int(horaMin[1])
    minuto=int(horaMin[2])+int(horaMin[3])
    if (hora>23 or hora<0)or (minuto<0 or minuto>59):
      return False
    return True

def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):
    return False
  else:
    dia=int(data[0])+int(data[1])
    mes=int(data[2])+int(data[3])
    ano=data[4]+data[5]+data[6]+data[7]
    if mes<1 or mes>12:
      return False
    elif (mes==1 or mes==3 or mes==5 or mes==6 or mes==7 or mes==8 or mes==10 or mes==12) and (dia<1 or dia>31):
      return False
    elif (mes==4 or mes==6 or mes==9 or mes==1) and (dia<1 or dia>30):
      return False
    elif mes==2 and (dia<1 or dia>29):
      return False
    return True

def projetoValido(proj):
  if len(proj)<2:
    return False
  elif proj[0]!="+":
    return False
  return True

def contextoValido(cont):
  if len(cont)<2:
    return False
  elif cont[0]!="@":
    return False
  return True

def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True
  
def organizar(linhas):
  itens = []
  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    
    l = l.strip() 
    tokens = l.split()
    if len (tokens)==1:
      desc=tokens[0]
    else:
      if len(tokens)!=0:
        i=0
        if len(tokens)==2:
            if dataValida(tokens[i]):
              data=tokens.pop(i)
            elif horaValida(tokens[i]) and len(tokens)>1 :
              hora=tokens.pop(i)            
            elif prioridadeValida(tokens[i]) and len(tokens)>1:
              pri=tokens.pop(i)
            elif len(tokens)>1:
              i=i+1
              if contextoValido(tokens[i]) and len(tokens)>1:
                contexto=tokens.pop(i)            
              elif projetoValido(tokens[i]) and len(tokens)>1:
                projeto=tokens.pop(i)
            for x in tokens:
              desc=desc+x+" "
            desc=desc[:len(desc)-1]+desc[len(desc)-1:].replace(" ","")
        else:
         i=0
         limite=0
         if dataValida(tokens[0]) and limite==0:
            data=tokens.pop(0)
            limite=limite+1
         if horaValida(tokens[0]) and limite<=1: 
            hora=tokens.pop(0)
            if data!="":
              limite=limite+1
            else:
              limite=limite+2
         if prioridadeValida(tokens[0]) and limite<=2 and len(tokens)>1:
            pri=tokens.pop(0)
            limite=limite+3
         else:
            limite=limite+3
         limite=0   
         i=len(tokens)-2
         if i==0:
           i=1
         if i==-1:
           limite=1000
         while i<len(tokens) and limite!=(1000) :
                if contextoValido(tokens[i]):
                  if contexto=="":
                    contexto=tokens.pop(i)
                  else:
                    temp=contexto
                    contexto=tokens[i]
                    tokens[i]=temp
                if i<len(tokens) and projetoValido(tokens[i]):
                  if projeto=="":
                    projeto=tokens.pop(i)
                  else:
                    temp=projeto
                    projeto=tokens[i]
                    tokens[i]=temp
                i=i+1
         for x in tokens:
           desc=desc+x+" "
 
    itens.append((desc, (data, hora, pri, contexto, projeto)))
 
  return itens

def listar(lista):
  atividades=organizar(lista)
  i=0
  n=1
  atividades=ordenarPorDataHora(atividades)
  atividades=ordenarPorPrioridade(atividades)
  while i<len(atividades):
    at=''
    if atividades[i][1][0]!="":
      temp=atividades[i][1][0]+" "
      at=at+temp[0]+temp[1]+"/"+temp[2]+temp[3]+"/"+temp[4]+temp[5]+temp[6]+temp[7]+" "
    if atividades[i][1][1]!="":
      temp=atividades[i][1][1]+" "
      at=at+temp[0]+temp[1]+":"+temp[2]+temp[3]+" "
    if atividades[i][1][2]!="":
      at=at+atividades[i][1][2]+" "
    at=at+atividades[i][0]
    if atividades[i][1][3]!="":
      at=at+atividades[i][1][3]+" "
    if atividades[i][1][4]!="":
      at=at+atividades[i][1][4]+" "
    if temPrioridade(atividades[i]):
      if atividades[i][1][2][1].upper()=="A":
        printCores(n,at,GREEN + BOLD)
      elif atividades[i][1][2][1].upper()=="B":
        printCores(n,at,BLUE)
      elif atividades[i][1][2][1].upper()=="C":
        printCores(n,at,CYAN)
      elif atividades[i][1][2][1].upper()=="D":
        printCores(n,at,YELLOW)
      else:
        print(n,at)
    else:
      if at!="":
        print(n,at)
    i=i+1
    n=n+1

def temData (tupla):
  if tupla[1][0]!="":
    return True
  else:
    return False

def temHora (tupla):
  if tupla[1][1]!="":
    return True
  else:
    return False

def ordenarPorDataHora(itens):
  i=0
  while i<len(itens):
    j=0
    while j<len(itens)-1:
      if temData(itens[j])==False and temData(itens[j+1])==True:
        temp=itens[j]
        itens[j]=itens[j+1]
        itens[j+1]=temp
      j=j+1
    i=i+1
  i=0
  while i<len(itens):
    j=0
    while j<len(itens)-1 and temData(itens[j+1])==True:
      data1=itens[j][1][0]
      data2=itens[j+1][1][0]
      ano1=int(data1[4]+data1[5]+data1[6]+data1[7])
      ano2=int(data2[4]+data2[5]+data2[6]+data2[7])
      mes1=int(data1[2]+data1[3])
      mes2=int(data2[2]+data2[3])
      dia1=int(data1[0]+data1[1])
      dia2=int(data2[0]+data2[1])
      if temHora(itens[j]):
        hora1=int(itens[j][1][1])
      if temHora (itens[j+1]):
        hora2=int(itens[j+1][1][1])
      if ano1>ano2:
        temp=itens[j]
        itens[j]=itens[j+1]
        itens[j+1]=temp
      elif ano1==ano2:
        if mes1>mes2:
          temp=itens[j]
          itens[j]=itens[j+1]
          itens[j+1]=temp
        elif mes1==mes2:
          if dia1>dia2:
            temp=itens[j]
            itens[j]=itens[j+1]
            itens[j+1]=temp
          elif dia1==dia2:
            if temHora(itens[j]) and temHora(itens[j+1]):
              if hora1>hora2:
                temp=itens[j]
                itens[j]=itens[j+1]
                itens[j+1]=temp
      j=j+1
    i=i+1

  i=0
  while i<len(itens):
    j=0
    while j<len(itens)-1:
      if temData(itens[j])==False and temHora(itens[j+1])==True:
        temp=itens[j]
        itens[j]=itens[j+1]
        itens[j+1]=temp
      j=j+1
    i=i+1
  i=0
  while i<len(itens):
    j=0
    while j<len(itens)-1:
      if temData(itens[j])==False and temHora(itens[j+1])==True:
        if temHora(itens[j]) and temHora(itens[j+1]):
          hora1=int(itens[j][1][1])
          hora2=int(itens[j+1][1][1])
          if hora1>hora2:
            temp=itens[j]
            itens[j]=itens[j+1]
            itens[j+1]=temp
      j=j+1
    i=i+1  
  return itens

def temPrioridade (tupla):
  if tupla[1][2]!="":
    return True
  else:
    return False
   
def ordenarPorPrioridade(itens):
  i=0
  while i<len(itens):
    j=0
    while j<len(itens)-1:
      if temPrioridade(itens[j])==False and temPrioridade(itens[j+1])==True:
        temp=itens[j]
        itens[j]=itens[j+1]
        itens[j+1]=temp
      j=j+1
    i=i+1
  i=0
  while i<len(itens):
    j=0
    while j<len(itens)-1 and temPrioridade(itens[j+1]):
      pri1=itens[j][1][2][1]
      pri2=itens[j+1][1][2][1]
      if pri1>pri2:
        temp=itens[j]
        itens[j]=itens[j+1]
        itens[j+1]=temp
      j=j+1
    i=i+1
  return itens

def fazer(num):
  f=open(ARCHIVE_FILE,"a+")
  f2=open(TODO_FILE)
  atividades=f2.readlines()
  if num>0 and num<=len(atividades):
    done=remover(num)
    at=''
    if done[1][0]!="":
      at=at+done[1][0]+" "
    if done[1][1]!="":
      at=at+atividades[1][1]+" "
    if done[1][2]!="":
      at=at+done[1][2]+" "
    at=at+done[0]
    if done[1][3]!="":
      at=at+done[1][3]+" "
    if done[1][4]!="":
      at=at+done[1][4]+" "
    f.write(at+"\n")
  else: print("Número inválido!")
           
def remover(num):
  f=open(TODO_FILE)
  tarefas=f.readlines()
  tarefas=organizar(tarefas)
  tarefas=ordenarPorDataHora(tarefas)
  tarefas=ordenarPorPrioridade(tarefas)
  if num>0 and num <=len(tarefas):
    done=tarefas.pop(num-1)
    atualizarTodo(tarefas)
    return done
  else: print("Numero invalido!!!")
  

def atualizarTodo (atividades):
  f=open(TODO_FILE,"w")
  i=0
  while i<len(atividades):
    at=''
    if atividades[i][1][0]!="":
      at=at+atividades[i][1][0]+" "
    if atividades[i][1][1]!="":
      at=at+atividades[i][1][1]+" "
    if atividades[i][1][2]!="":
      at=at+atividades[i][1][2]+" "
    at=at+atividades[i][0]
    if atividades[i][1][3]!="":
      at=at+atividades[i][1][3]+" "
    if atividades[i][1][4]!="":
      at=at+atividades[i][1][4]+" "
    f.write(at+"\n")
    i=i+1
  f.close()
  f=open(TODO_FILE)
  tarefas=f.readlines()
  listar(tarefas)
  
def priorizar(num, prioridade):
  if soDigitos(num):
    num=int(num)
    prioridade=prioridade.upper()
    prioridade="("+prioridade+")"
    f=open(TODO_FILE)
    tarefas=f.readlines()
    tarefas=organizar(tarefas)
    tarefas=ordenarPorDataHora(tarefas)
    tarefas=ordenarPorPrioridade(tarefas)
    if prioridadeValida(prioridade):
      if num>0 and num<=len(tarefas):
        tarefa=(tarefas[num-1][0],(tarefas[num-1][1][0],tarefas[num-1][1][1],prioridade,tarefas[num-1][1][3],tarefas[num-1][1][4]))
        tarefas[num-1]=tarefa
        atualizarTodo(tarefas)
      else: print("Numero invalido!")
    else:  print("Prioridade invalida!!!")
  else: print("Numero invalido!!!")

def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) 
    comandos.pop(0)
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1])
  elif comandos[1] == LISTAR:
    f=open(TODO_FILE)
    tarefas=f.readlines()
    listar(tarefas)      
  elif comandos[1] == REMOVER:
    if soDigitos(comandos[2]):
      n=int(comandos[2])
      remover(n)
    else: print("Número inválido!!!")
  elif comandos[1] == FAZER:
    if soDigitos(comandos[2]):
        n=int(comandos[2])
        fazer(n)
    else: print("Número inválido!!!")   
  elif comandos[1] == PRIORIZAR:
    alfabeto=("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if comandos[3].upper() in alfabeto:
      priorizar(comandos[2],comandos[3])
    else: print("Prioridade invalida!")
  else :
    print("Comando inválido.")

processarComandos(sys.argv)
