import socket
import sys
import select

#--------------------------------------VARIAVEIS------------------------------------------------------------#

SERVER_PORT = 12000
SERVER_IP   = '127.0.0.1'

#nome do jogador
nome = ""
#inicialmente o cliente encontra-se no estado em que não se registou
registo = 0
#flag para gerir os prints no ecrã
mostrar = 1

try:
  ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error:
  print("Falha ao criar o socket.")
  sys.exit()

# o select quer ficar a espera de ler o socket e ler do stdin (consola)
inputs = [ClientSocket, sys.stdin]

#--------------------------------------FUNÇÕES------------------------------------------------------------#

#Função que trata do jogo em si, recebendo um tabuleiro, o nome do adversário e uma variável, vez, que funcionará como flag para saber quem pode jogar primeiro
def Jogo(simbolo, nomeadversario, vez):  

  flag = vez

  t=["1","2","3","4","5","6","7","8","9"]

  #Função para imprimir o tabuleiro
  def verJogo(t):
    
    print (t[0] + " | " + t[1] + " | "  + t[2] + "\n" +  "----------" + "\n" + t[3] + " | " + t[4] + " | "  + t[5] + "\n" +  "----------" + "\n" + t[6] + " | " + t[7] + " | "  + t[8] + "\n")
    
  #Função para verificar vencedor. Devolve true caso a situação de empate ou vitória se verifique
  def vencedor(t, simbolo):
    
    LoserMessage = "Victoria:" + nomeadversario 
    
    DrawMessage = "Empate:" + nomeadversario
    
    if(t[0] == simbolo and t[1] == simbolo and t[2] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT))
      return True
      
    if(t[3] == simbolo and t[4] == simbolo and t[5] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT))      
      return True
    
    if(t[6] == simbolo and t[7] == simbolo and t[8] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT))
      return True
  
    if(t[0] == simbolo and t[3] == simbolo and t[6] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT)) 
      return True
    
    if(t[1] == simbolo and t[4] == simbolo and t[7] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT))  
      return True
      
    if(t[2] == simbolo and t[5] == simbolo and t[8] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT))  
      return True
    
    if(t[0] == simbolo and t[4] == simbolo and t[8] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT))  
      return True
    
    if(t[2] == simbolo and t[4] == simbolo and t[6] == simbolo):
      print("Parabéns, ganhaste!")
      ClientSocket.sendto(LoserMessage.encode(),(SERVER_IP,SERVER_PORT)) 
      return True
      
    if((t[0] == 'X' or t[0] == 'O' ) and 
       (t[1] == 'X' or t[1] == 'O' ) and 
       (t[2] == 'X' or t[2] == 'O' ) and 
       (t[3] == 'X' or t[3] == 'O' ) and 
       (t[4] == 'X' or t[4] == 'O' ) and 
       (t[5] == 'X' or t[5] == 'O' ) and
       (t[6] == 'X' or t[6] == 'O' ) and 
       (t[7] == 'X' or t[7] == 'O' ) and 
       (t[8] == 'X' or t[8] == 'O' )):
      print("Que pena, empataram!")
      ClientSocket.sendto(DrawMessage.encode(),(SERVER_IP,SERVER_PORT))
      return True
    
    return False
      
      
  #Função para realizar uma jogada
  def Jogada(jogada, simbolo):
    
    if(jogada == "1" or 
       jogada == "2" or 
       jogada == "3" or 
       jogada == "4" or 
       jogada == "5" or 
       jogada == "6" or 
       jogada == "7" or 
       jogada == "8" or 
       jogada == "9"):
      
      if(t[int(jogada)-1] == "X"):
        print("Jogada inválida!")
      elif(t[int(jogada)-1] == "O"):
        print("Jogada inválida!")
      else:
        t[int(jogada)-1] = simbolo
        return True
      
    else:
      print("Jogada inválida!")
    
    return False

#-----------------CONTINUAÇÃO DA FUNÇÃO JOGO--------------------#

  print()
  print("Começou o jogo!")
  print()  
 
  #define os simbolos dos jogadores
  if(simbolo == "X"):
    outroJogador = "O"
  else:
    outroJogador = "X" 

  verJogo(t)


  #ciclo para detectar o que é recebido no standard input ou no socket, dentro do ciclo do jogo, para tratar de todas as mensagens que são trocadas pelo servidor/cliente  
  while True:
  
    global mostrar
  
    if(mostrar == 1 ):
      print()
      print("Introduza uma jogada")
      print()
  
    ins2, outs, exs = select.select(inputs,[],[])
    #select devolve para a lista ins quem esta a espera de ler 
  
    for i in ins2:
    
      #select das mensagens vindas do standard input
      if i == sys.stdin:
      
        mostrar = 0
        
        InputMessage = sys.stdin.readline()
        
        NovaMessage = InputMessage[0:7] + nomeadversario
      
        if(InputMessage[0:6] == "Jogar:"):
          
          if(flag == 1):
            jogadavalida = Jogada((InputMessage[6]),simbolo)     
            if(jogadavalida == True):
              print()
              verJogo(t)
              flag = 0 #flag muda para 0 para não poder jogar até à vez do outro
              ClientSocket.sendto(NovaMessage.encode(),(SERVER_IP,SERVER_PORT))
              
              if(vencedor(t, simbolo) == True):
                return
              
            else:
              print("Introduza uma nova jogada")
              print()
              verJogo(t)
              
          else:
            print("Não é a tua vez de jogar!")

      #select das mensagens vindas do socket
      elif i == ClientSocket:
        
        mostrar = 1
      
        (Message,Adress) = ClientSocket.recvfrom(1024)
  
        Comandos2 = Message.decode().split()
    
        if(Comandos2[0][0:6] == "Jogar:"):
          Jogada((Comandos2[0][6]),outroJogador)
          verJogo(t)
          flag = 1
            
        #tratamento dos ok's enviados pelo servidor
        if(Comandos2[0][0:3]=="Ok:"):
          if(Comandos2[0][3:]=="Jogada"):
            print("Jogada enviada com sucesso.") 
          if(Comandos2[0][3:]=="Victoria"):
            print("Victória enviada com sucesso.")
          if(Comandos2[0][3:]=="Empate"):
            print("Empate enviado com sucesso.")             
            
            
        if(Comandos2[0][0:9]=="Victoria:"):
          print(nomeadversario + " ganhou o jogo!")
          return
        
        if(Comandos2[0][0:7]=="Empate:"):
          print("Empatou o jogo com " + nomeadversario)
          return      


#--------------------------------------CÓDIGO DO CLIENTE------------------------------------------------------------#        
print()
print("Registar:x       ->  Para registar jogador com o nome x")
print("Convidar:x       ->  Para convidar jogador com o nome x")
print("ListarJogadores  ->  Ver os jogadores registados e estados")

while True:
  
  if(mostrar == 1):
    print()
    print("Introduz um comando")
    print()
  
  ins, outs, exs = select.select(inputs,[],[])
  #select devolve para a lista ins quem esta a espera de ler
  
  for i in ins:
    
    if i == sys.stdin:
      
      mostrar = 0
      
      InputMessage = sys.stdin.readline()
      
      if(InputMessage[0:9] == "Registar:"):
        if (registo != 1):
          nome = InputMessage[9:]
          registo = 1
     
      if(registo == 1):     
          
        if(InputMessage == ("Convidar:" + nome)):
          print("Não te podes convidar!")
        
        else:
          
          ClientSocket.sendto(InputMessage.encode(),(SERVER_IP,SERVER_PORT))

        if(InputMessage == "ListarJogadores\n"):
  
          Comandos = ""  
                  
          while Comandos != "FimLista":
                  
            (Message,Adress) = ClientSocket.recvfrom(1024)
                    
            Comandos = Message.decode() 
                  
            if(Comandos != "FimLista"):
                      
              print(Comandos)        
              
      else:
        print("Tens que te registar primeiro!")
        

    elif i == ClientSocket:
      
      mostrar = 1
      
      (Message,Adress) = ClientSocket.recvfrom(1024)
  
      Comandos = Message.decode().split()
      
      #Tratamento de todos os ok's devolvidos pelo servidor
      if(Comandos[0][0:3]=="Ok:"):
        if(Comandos[0][3:]=="Registo"):
          print("Registo efectuado com sucesso.")
        if(Comandos[0][3:10]=="Aceitar"):
          print("O convite foi aceite com sucesso!")
          Jogo("X",Comandos[0][10:], 0)
        if(Comandos[0][3:]=="Convite"):
          print("O convite foi enviado!")
        if(Comandos[0][3:]=="Recusar"):
          print("O convite foi recusado com sucesso!")          
        if(Comandos[0][3:]=="Jogada"):
          print("Jogada enviada com sucesso.") 
        if(Comandos[0][3:]=="Lista"):
          print("Pedido de listagem de jogadores efectuado com sucesso.")          
        
      #Tratamento de todos os erros devolvidos pelo servidor    
      elif(Comandos[0][0:5]=="ERRO:"):
        if(Comandos[0][5:] == "NomeUsado"):
          print('Nome de registo já usado ou já te registaste.')
        if(Comandos[0][5:] == "Jogadorinexistente"):
          print('O jogador que tentou convidar não existe!')          
        if(Comandos[0][5:] == "Jogadorocupado"):
          print('O jogador está ocupado.')    
        if(Comandos[0][5:] == "ComandoDesconhecido"):
          print('Introduza um comando válido.')  
        if(Comandos[0][5:] == "Ocupado"):
          print('Só podes enviar novos convites quando te responderem.')  
        
      #Condições de tratamento quando um cliente recebe um convite
      elif(Comandos[0][0:8] == "Convite:"):
        
        #Guardar o nome do jogador adversario
        nomeconvidante = Comandos[0][8:]  
        
        print(Comandos[0][8:] + "" + " convidou-te para jogar.")
        
        print("Queres aceitar ou recusar?")
        
        #Flag para sair do ciclo while
        x = 1 
        
        while(x == 1):
          
          InputMessage = sys.stdin.readline()
          
          #Caso o jogador aceite um convite
          if(InputMessage[0:7] == "Aceitar"):

            #Geração da mensagem de aceitação
            InputMessage = "Aceitar" + ":" + nomeconvidante 
            #Envio 
            ClientSocket.sendto(InputMessage.encode(),(SERVER_IP,SERVER_PORT)) 
            
            #Vai buscar todos os convites restantes, caso os haja
            (Message,Adress) = ClientSocket.recvfrom(1024)
             
            Comandos = Message.decode().split() 
            
            #Vai buscando os restantes convites e recusa-os 
            while(Comandos[0][0:8] == "Convite:"):

              nomeconvidante = Comandos[0][8:]
              
              InputMessage2 = "Recusar" + ":" + nomeconvidante
              
              ClientSocket.sendto(InputMessage2.encode(),(SERVER_IP,SERVER_PORT)) 
              
              (Message,Adress) = ClientSocket.recvfrom(1024)
                           
              Comandos = Message.decode().split()              
            
            #Inicio do jogo para quem aceita o convite
            Jogo("X",Comandos[0][10:], 0)
            #Mudança de flag para sair do ciclo while
            x = 0
          
          #Caso o jogador queira recusar os convites, recusa um a um  
          elif(InputMessage[0:7] == "Recusar"):
            #Geração da mensagem de recusar
            InputMessage2 = "Recusar" + ":" + nomeconvidante
            #Envio             
            ClientSocket.sendto(InputMessage2.encode(),(SERVER_IP,SERVER_PORT))             
            
            x = 0
          
          #Caso tente executar outra instrução enquanto não aceita u recusa  
          else: 
            print("Tens que aceitar ou recusar o convite!")
      
      #mensagem enviada pelo servidor a avisar de pedido recusado  
      elif(Comandos[0][0:15] == "PedidoRecusado:"):
        print(Comandos[0][15:] + "" + " recusou o seu pedido para jogar.")
      
      #mensagem enviada pelo servidor a avisar de pedido aceite, iniciando o jogo  
      elif(Comandos[0][0:13] == "PedidoAceite:"):
        print(Comandos[0][13:] + "" + " aceitou o seu pedido para jogar.")
        Jogo("O", Comandos[0][13:],1) 
        

  




