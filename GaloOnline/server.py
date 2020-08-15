import socket

#---------------------------------------INICIALIZACOES------------------------------------------#

ServerSocket_PORT=12000

ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ServerSocket.bind(('',12000))

addrs   = {} # dict: nome -> endereco. Ex: addrs["user"]=('127.0.0.1',17234)
clients = {} # dict: endereco -> nome. Ex: clients[('127.0.0.1',17234)]="user"
estados = {}


#Variavel que vai guardar o numero de jogadores no sistema
NumeroJogadores = 0


#-------------------------------------------FUNCOES---------------------------------------------#

def Registar(name,addr):
  '''Regista um jogador com o nome 'name' e o endereço 'addr' e mete-o na lista local'''
  
  Resposta = "Ok:Registo"
  Erro = "ERRO:NomeUsado"
  
  
  if not name in addrs and not addr in clients:

    global NumeroJogadores
    
    addrs[name] = addr
    clients[addr] = name
    estados[name] = "Livre"
    NumeroJogadores= NumeroJogadores + 1 
    ServerSocket.sendto(Resposta.encode(),addr)
    
  else:
    
    ServerSocket.sendto(Erro.encode(),addr)
    
    
def ListarJogadores(num, addr):
  '''Devolve uma lista com todos os nomes dos jogadores, sendo enviado um jogador de cada vez a que faz o pedido'''

  global addrs
  global estados
  
  Resposta = "FimLista"
  
  while num-1 >= 0:
    
    Nome = list(addrs)[num-1]
    
    RespondMessage = "Nome:" + Nome + " " + "Estado:" + str(estados[Nome])
  
    ServerSocket.sendto(RespondMessage.encode(),addr)
    
    num = num - 1
    
  ServerSocket.sendto(Resposta.encode(),addr)
  
def Convidar(nome,addr):
  '''Convida o jogador com o nome "nome", e é também fornecido o endereço de quem convida, para poder manter informação sobre quem enviou o convite'''
  
  Erro1 = "ERRO:Jogadorinexistente"
  Erro2 = "ERRO:Jogadorocupado"
  
  Mensagem = "Ok:Convite"
  
  
  
  if nome in addrs:
    
    #endereço do nome a enviar
    address = addrs[nome]
    
    #verifica se o jogador que quer convidar está livre
    if(estados[nome] == "Livre"):
      
      #muda o estado de quem convida para ocupado
      estados[clients[addr]] = "Ocupado"
      
      ServerSocket.sendto(Mensagem.encode(),addr)
      
      MensagemConvite = "Convite:" + clients[addr]
      
      #Envia a mensagem para o jogador que se quer convidar
      ServerSocket.sendto(MensagemConvite.encode(),address)
      
    else:
      #Erro caso o jogador esteja ocupado
      ServerSocket.sendto(Erro2.encode(),addr)
    
  else:
    
    #Erro caso o jogador não exista na lista
    ServerSocket.sendto(Erro1.encode(),addr)
  
 
   
    
def Aceitar(nome,Adress):
  '''Aceita o convite'''
  
  Mensagem = "Ok:Aceitar" + nome
        
  #Envia a mensagem de confirmaçao para o cliente que enviou o pedido
  ServerSocket.sendto(Mensagem.encode(),Adress)  
  
  #endereço do nome a enviar
  address = addrs[nome]  
  
  MensagemConvite = "PedidoAceite:" + clients[Adress]
  
  #Envia a mensagem para o jogador que se quer convidar
  ServerSocket.sendto(MensagemConvite.encode(),address)
  
  estados[nome] = "Ocupado"
  
  estados[clients[Adress]] = "Ocupado"
  
def Recusar(nome,Adress):
  '''Recusa o convite'''
  
  Mensagem = "Ok:Recusar"
        
  #Envia a mensagem de confirmaçao para o cliente que enviou o pedido
  ServerSocket.sendto(Mensagem.encode(),Adress)  
  
  #endereço do nome a enviar
  address = addrs[nome]  
  
  MensagemConvite = "PedidoRecusado:" + clients[Adress]
  
  estados[nome] = "Livre"
    
  estados[clients[Adress]] = "Livre"  
  
  #Envia a mensagem para o jogador que se quer convidar
  ServerSocket.sendto(MensagemConvite.encode(),address)

#--------------------------------------CORPO DO PROGRAMA----------------------------------------#

while True:
  
  (Message,Adress) = ServerSocket.recvfrom(1024)
  
  Comandos = Message.decode().split()
  
  print(Comandos)
  
  if(Comandos[0][0:9]=="Registar:"):
    Registar(Comandos[0][9:],Adress)
    
  elif(Comandos[0]=="ListarJogadores"):   
    ListarJogadores(NumeroJogadores, Adress)
    
  elif(Comandos[0][0:9]=="Convidar:"):
    if(estados[clients[Adress]] == "Livre"):   
      Convidar(Comandos[0][9:], Adress) 
    else:
      #Mensagem enviada pelo servidor aquando de duplo convite pelo mesmo jogador
      ErroOcupado = "ERRO:Ocupado"
      ServerSocket.sendto(ErroOcupado.encode(),Adress)      
  
  elif(Comandos[0][0:8] == "Aceitar:"):
    Aceitar(Comandos[0][8:],Adress)

  elif(Comandos[0][0:8] == "Recusar:"):
    Recusar(Comandos[0][8:],Adress)

  elif(Comandos[0][0:6] == "Jogar:"):
    Ok = "Ok:Jogada"
    ServerSocket.sendto(Ok.encode(),Adress)
    nome = Comandos[0][7:]
    addr = addrs[nome]
    ServerSocket.sendto(Comandos[0].encode(),addr)
    
  elif(Comandos[0][0:9] == "Victoria:"):
    Ok = "Ok:Victoria" 
    ServerSocket.sendto(Ok.encode(),Adress)
    #mudança do estado do jogador para livre
    estados[clients[Adress]] = "Livre"
    nome = Comandos[0][9:]
    addr = addrs[nome]
    #mudança para o outro jogador mudar o seu estado para livre
    estados[nome] = "Livre"
    ServerSocket.sendto(Comandos[0].encode(),addr)
    
  elif(Comandos[0][0:7] == "Empate:"):
    Ok = "Ok:Empate" 
    ServerSocket.sendto(Ok.encode(),Adress)
    #mudança do estado do jogador para livre
    estados[clients[Adress]] = "Livre"
    nome = Comandos[0][7:]
    addr = addrs[nome]
    #mudança para o outro jogador mudar o seu estado para livre
    estados[nome] = "Livre"
    ServerSocket.sendto(Comandos[0].encode(),addr)     
      
      
  else:
    #Caso a mensagem introduzida seja um comando desconhecido
    Mensage = "ERRO:ComandoDesconhecido"
      
    ServerSocket.sendto(Mensage.encode(),Adress) 

ServerSocket.close()
