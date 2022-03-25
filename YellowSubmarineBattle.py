import turtle
import random

#Setup da tela e carregamento das imagens

tela = turtle.Screen()
tela.bgcolor('lightblue')
tela.tracer(False)
inimigo = r'boat_small.gif'
jogador = r'submarino2.gif'
agua = r'agua.gif'
tela.addshape(inimigo)
tela.addshape(jogador)
tela.addshape(agua)

#Função que desenha as bordas do jogo

def borda():
    pen = turtle.Turtle()
    pen.ht()
    pen.up()
    pen.pensize(200)
    pen.color('#E3CF57')
    pen.goto(-700,-450)
    pen.down()
    pen.setx(700)
    pen.sety(450)
    pen.setx(-700)
    pen.sety(-450)

#Definição da classe dos obstáculos(barcos)

class Obstaculo(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.up()
        self.right(90)
        self.shape(inimigo)
        self.velocidade = 1

    #Funções que animam os obstáculos em diferentes direções
    
    def animar_down(self):
        self.seth(-90)
        if self.ycor() > -450:
            self.forward(self.velocidade)
        else:
            self.sety(450)
        tela.ontimer(self.animar_down,50)
    
    def animar_up(self):
        self.seth(90)
        if self.ycor() < 450:
            self.forward(self.velocidade)
        else:
            self.sety(-450)
        tela.ontimer(self.animar_up,50)

    def animar_right(self):
        self.seth(0)
        if self.xcor() < 750:
            self.forward(self.velocidade)
        else:
            self.setx(-750)
        tela.ontimer(self.animar_right,50)

    def animar_left(self):
        self.seth(180)
        if self.xcor() > -750:
            self.forward(self.velocidade)
        else:
            self.setx(750)
        tela.ontimer(self.animar_left,50)

    #Funções para movimentação da posição dos obstáculos (usadas na construção de paredes)
    
    def eixox(self,x):
        self.setx(x)
    
    def eixoy(self,y):
        self.sety(y)

    def subir(self,dist):
        self.right(180)
        self.forward(dist)
        self.right(180)

#Definição da classe 'linhas de visão', a qual pertence a mira do submarino

class Linhas_de_visao(turtle.Turtle):
    def __init__(self,robo):
        turtle.Turtle.__init__(self)
        self.angulo = robo.heading()
        self.ht()
        self.color('black')
        self.pensize(5)
        self.goto(robo.pos())
        self.seth(self.angulo)
        self.comp = 40
        self.forward(self.comp)
        self.robo = robo
        self.shot = 10
        self.atirar()

    #Função que altera o ângulo da mira

    def mudar_angulo(self):
        self.clear()
        self.angulo = self.robo.heading()
        self.seth(self.angulo)
        self.forward(self.comp)

    #Função que faz com que a mira acompanhe o movimento do submarino

    def pra_frente(self):
        self.clear()
        self.up()
        self.goto(self.robo.pos())
        self.down()
        self.forward(self.comp)

    #Funções que geram o efeito de tiro

    def atirar(self):
        if self.shot < 3:
            self.color('yellow')
            self.pensize(10)
            self.shot += 1
        else:
            self.color('black')
            self.pensize(5)
        tela.ontimer(self.atirar,50)
  
    def shoot(self):
        self.shot = 0

#Definição da classe parede, que contem uma lista de obstáculos (ou barcos) alinhados

class Parede:
    def __init__(self,orientacao,localizacao,blocos,inicio = 0,intervalo = 100):
        self.parede = []
        self.orientacao = orientacao
        for i in range(blocos):
            self.parede.append(Obstaculo())
            if orientacao == 'vertical':
                self.parede[-1].eixoy(inicio)
                self.parede[-1].eixox(localizacao)
                self.parede[-1].subir(i * intervalo)
            elif orientacao == 'horizontal':
                self.parede[-1].eixox(inicio)
                self.parede[-1].eixoy(localizacao)
                self.parede[-1].left(90)
                self.parede[-1].subir(i * intervalo)
                self.parede[-1].right(90)

    #Função que inicializa a animação da parede
    
    def animar(self,speed,direcao):
        if direcao == 'down':
            for bloco in self.parede:
                bloco.velocidade = speed
                bloco.animar_down()
        if direcao == 'up':
            for bloco in self.parede:
                bloco.velocidade = speed
                bloco.animar_up()
        if direcao == 'right':
            for bloco in self.parede:
                bloco.velocidade = speed
                bloco.animar_right()
        if direcao == 'left':
            for bloco in self.parede:
                bloco.velocidade = speed
                bloco.animar_left()
        
#Definição da classe 'tiro', usada para o tiro do submarino

class Tiro(turtle.Turtle):
    def __init__(self,robo,linha):
        turtle.Turtle.__init__(self)
        #self.ht()
        self.color('red')
        self.shape('circle')
        self.up()
        self.goto(2000,2000)
        self.robo = robo
        self.linha = linha
        self.speed = 0
        self.mover()

    #Funções que executam a animação do tiro

    def atirar(self):
        self.goto(self.robo.pos())
        self.seth(self.linha.angulo)
        self.speed = 20

    def mover(self):
        self.forward(self.speed)
        tela.ontimer(self.mover,5)

#Definição da classe 'power', a qual pertence a bolinha azul que aumenta os tiros disponíveis do submarino

class Power(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color('blue')
        self.up()
        self.shape('circle')
        self.turtlesize(2)
        x = random.randint(-590,591)
        y = random.randint(-340,341)
        self.goto(x,y)

    #Função que joga a bolinha em um local aleatório da tela

    def change(self):
        x = random.randint(-590,591)
        y = random.randint(-340,341)
        self.goto(x,y)

#Definição da classe 'texto' à qual pertencem os textos na lateral da tela que indicam os parametros

class Texto(turtle.Turtle):
    def __init__(self,parametro,valor,altura,cor,modo):
        turtle.Turtle.__init__(self)
        self.modo = modo
        self.valor = valor
        self.parametro = parametro
        self.ht()
        self.up()
        self.color(cor)
        self.sety(altura)
        self.setx(-750)
        self.write(self.parametro + ': ' + str(self.valor),font=('Courier',20,self.modo))

    #Função que modifica o parametro indicado pelo texto

    def mudar_valor(self,valor):
        self.valor = valor
        self.clear()
        self.write(self.parametro + ': ' + str(self.valor),font=('Courier',20,self.modo))

#Função que inicializa a fase 1

def set_1():

    #Primeiro os objetos 'parede' são criados

    parede1 = Parede('horizontal',0,5,450,200)
    parede2 = Parede('horizontal',-200,4,intervalo = 200)
    parede3 = Parede('horizontal',200,3,200,150)
    parede4 = Parede('horizontal',300,2,400)

    #Em seguida a animação deles é inicializada

    parede1.animar(15,'down')
    parede2.animar(5,'up')
    parede3.animar(10,'up')
    parede4.animar(20,'down')

    #Por fim, todos eles são armazenados em uma lista que é retornada pela função

    paredes = [parede1,parede2,parede3,parede4]
    return paredes

#Função que inicializa a fase 2

def set_2():
    parede1 = Parede('horizontal',0,3,250,300)
    parede2 = Parede('vertical',-200,4,-200,200)
    parede3 = Parede('vertical',0,4,-100,200)
    parede4 = Parede('vertical',500,3,-300)
    parede5 = Parede('vertical',500,3,100)

    parede1.animar(15,'up')
    parede2.animar(10,'down')
    parede3.animar(10,'up')
    parede4.animar(20,'left')
    parede5.animar(20,'left')

    paredes = [parede1,parede2,parede3,parede4,parede5]
    return paredes

#Função que inicializa a fase 3

def set_3():
    parede1 = Parede('vertical',-300,4,0,200)
    parede2 = Parede('vertical',-100,4,-350,200)
    parede3 = Parede('vertical',100,4,0,200)
    parede4 = Parede('vertical',300,4,-350,200)
    parede5 = Parede('vertical',500,4,0,200)

    parede1.animar(5,'down')
    parede2.animar(10,'up')
    parede3.animar(15,'down')
    parede4.animar(20,'up')
    parede5.animar(25,'down')

    paredes = [parede1,parede2,parede3,parede4,parede5]
    return paredes

#A partir daqui são inicializados os parâmetros necessários para o funcionamento do jogo.

fase = 1
pontuacao = 0
fase1 = True
fase2 = True

#A água é inserida na tela

water = turtle.Turtle()
water.up()
water.shape(agua)

#A fase 1 é inicializada e a lista de paredes é armazenada em uma variável

todas_paredes = set_1()

#O jogador é inicializado

robo1 = turtle.Turtle()
robo1.shape(jogador)
robo1.speed(0)
robo1.up()
robo1.goto(-500,0)

#A mira do submarino é inicializada

linha1 = Linhas_de_visao(robo1)

#O tiro é inicializado

tiro1 = Tiro(robo1,linha1)

#O powerup é inicializado

power = Power()

#A borda é desenhada

borda()

#Os parametros iniciais do jogador são inicializados

speedx = 0
speedy = 0
tiros = 10
vidas = 15

#Os textos laterais são escritos

texto_vidas = Texto('Vidas',vidas,50,'red','bold')
texto_tiros = Texto('Tiros',tiros,-50,'blue','bold')
texto_fase = Texto('Fase',fase,300,'black','italic')
texto_pontos = Texto('Score',pontuacao,250,'green','italic')

#Aqui são definidas as funções executadas ao longo do jogo, que alteram os parametros do jogador

#Função executada quando a seta direita é pressionada

def right():
    global speedx
    speedx += 0.2
    if 0 < robo1.heading() <= 180:
        robo1.right(10)
    elif 180 < robo1.heading() < 360:
        robo1.left(10)
    linha1.mudar_angulo()

#Função executada quando a seta esquerda é pressionada

def left():
    global speedx
    speedx -= 0.2
    if 0 <= robo1.heading() < 180:
        robo1.left(10)
    elif 180 < robo1.heading() < 360:
        robo1.right(10)
    linha1.mudar_angulo()

#Função executada quando a seta 'cima' é pressionada

def up():
    global speedy
    speedy += 0.2
    if 90 < robo1.heading() <= 270:
        robo1.right(10)
    elif 270 < robo1.heading() < 360 or 0 <= robo1.heading() < 90:
        robo1.left(10)
    linha1.mudar_angulo()

#Função executada quando a seta 'baixo' é pressionada

def down():
    global speedy
    speedy -= 0.2
    if 90 <= robo1.heading() < 270:
        robo1.left(10)
    elif 270 < robo1.heading() < 360 or 0 <= robo1.heading() < 90:
        robo1.right(10)
    linha1.mudar_angulo()

#Função que executa o tiro

def tiro():
    global tiros
    if tiros > 0:
        linha1.shoot()
        tiro1.atirar()
        tiros -= 1
        texto_tiros.mudar_valor(tiros)

#Função que traz o jogador de volta ao ponto inicial (quando ele é ferido ou passa de fase)

def restart(player,linha):
    global speedx
    global speedy
    speedx = 0
    speedy = 0
    player.goto(-500,0)
    player.seth(0)
    linha.mudar_angulo()

#Função que é executada se o jogador fica sem vidas (derrota)

def derrota(player,linha,tiro):
    player.ht()
    player.goto(5000,5000)
    tiro.ht()
    game_over = turtle.Turtle()
    game_over.up()
    game_over.ht()
    game_over.goto(-370,-100)
    game_over.color('green')
    game_over.write('GAME OVER',font=('Courier',100,'bold'))

#Função que é executada se o jogador zera o jogo

def vitoria(player,linha,tiro):
    player.ht()
    player.goto(5000,5000)
    tiro.ht()
    vit = turtle.Turtle()
    vit.up()
    vit.ht()
    vit.goto(-300,-100)
    vit.color('green')
    vit.write('PARABÉNS',font=('Courier',100,'bold'))

#Aqui são executadas as funções que fazem o turtle aceitar o input do usuário

tela.listen()
tela.onkeypress(right,'Right')
tela.onkeypress(left,'Left')
tela.onkeypress(up,'Up')
tela.onkeypress(down,'Down')
tela.onkeypress(tiro,'space')

#A partir daqui começa o 'mainloop' do jogo, um código que é executado infinitamente enquanto o jogo está aberto.

while True:

    #Primeiro é verificado se o jogador tem vidas

    if vidas <= 0:

        #Caso ele não tenha a função 'derrota' é executada

        derrota(robo1,linha1,tiro1)

    #Em seguida é verificado se o jogador venceu o jogo

    if pontuacao == 51:

        #Se sim, a função 'vitória é executada

        vitoria(robo1,linha1,tiro1)

    #É verificado se o jogador tem pontos para passar para a fase 2 e se ele ainda está na fase 1

    if pontuacao == 14:
        if fase1:

            #Caso ambos sejam verdadeiros a fase 2 é inicializada e todos os parâmetros necessários são modificados

            fase1 = False
            restart(robo1,linha1)
            tiros = 15
            fase = 2
            todas_paredes = set_2()
            borda()
            texto_tiros.mudar_valor(tiros)
            texto_fase.mudar_valor(fase)
            texto_pontos.mudar_valor(pontuacao)
            texto_vidas.mudar_valor(vidas)

    #É verificado se o jogador tem pontos para passar para a fase 3 e se ele ainda está na fase 2

    if pontuacao == 31:
        if fase2:

            #Caso ambos sejam verdadeiros a fase 3 é inicializada e todos os parâmetros necessários são modificados

            fase2 = False
            restart(robo1,linha1)
            tiros = 20
            fase = 3
            todas_paredes = set_3()
            borda()
            texto_tiros.mudar_valor(tiros)
            texto_fase.mudar_valor(fase)
            texto_pontos.mudar_valor(pontuacao)
            texto_vidas.mudar_valor(vidas)

    #As atuais posições x e y do jogador são armazenadas em variáveis

    x = robo1.xcor()
    y = robo1.ycor()

    #Ele é movido para uma nova posição com base na posição atual e na velocidase atual em x e em y

    robo1.goto(x + speedx,y + speedy)

    #As variáveis de posição são atualizadas

    x = robo1.xcor()
    y = robo1.ycor()

    #A posição da mira é atualizada

    linha1.pra_frente()

    #É verificado se o jogador atingiu um powerup

    if robo1.distance(power) <= 50:

        #Se sim, o powerup é movido para outro local e o número de tiros disponíveis ao jogador aumenta

        power.change()
        tiros += 10
        texto_tiros.mudar_valor(tiros)

    #É verificado se o jogador atingiu uma borda do mapa
    #Caso tenha atingido a velocidade horizontal ou vertical do jogador é revertida

    if x <= -570 or x >= 570:
        speedx = -speedx
    if y <= -320 or y >= 320:
        speedy = -speedy

    #Para cada obstáculo no mapa é feito o seguinte:

    for parede in todas_paredes:
        for elemento in parede.parede:

            #É verificado se o obstáculo atingiu o jogador

            if robo1.distance(elemento) <= 60:

                #se tiver atingido o jogador volta ao ponto inicial e perde uma vida

                speedx = 0
                speedy = 0
                restart(robo1,linha1)
                vidas -= 1
                texto_vidas.mudar_valor(vidas)

                #É verificado se o obstáculo foi atingido por um tiro

            if elemento.distance(tiro1) <= 30:

                #Caso tenha sido o tiro e o obstáculo são removidos da tela e a pontuação aumenta em 1

                elemento.goto(5000,4500)
                tiro1.goto(-5000,-5000)
                pontuacao += 1
                texto_pontos.mudar_valor(pontuacao)
    
    #A tela é atualizada

    tela.update()





