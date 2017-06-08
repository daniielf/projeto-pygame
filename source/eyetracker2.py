# new project
import math
import constants  # Obter configuracao padroes do experimento
import random  # Obter funcoes de aleatoriedade
from pygaze import libscreen  # Criar Display e telas para o experimento
from pygaze import eyetracker  # Capturar o posicionamento visual do usuario e criar logs dos resultado
from pygaze import liblog  # Criar logs de saida com os resultados do experimento
from pygaze import libinput  # Obter interacao do usuario atraves do mouse e teclado
from pygaze import libtime  # Obter a latencia do usuario em relacao aos estimulos

display = libscreen.Display()  # Obtendo um Display para a exibicao do experimento
tracker = eyetracker.EyeTracker(display)  # Obtendo um EyeTracker para a captura ocular atraves do display passado
log = liblog.Logfile()  # Obtendo um Log para geracao dos resultados em um arquivo .txt
keyboard = libinput.Keyboard()  # Obtendo um Keyboard para a interecao com o teclado ("space")

instructionScreen = libscreen.Screen()  # Obtendo uma tela para exibir as instrucoes do experimento
instructionScreen.draw_text(text="Experimento 1: Mantenha o cursos no centro e aperte ESPACO", colour=(0, 0, 255), fontsize=24)  # Configurando um texto para a tela de instrucoes

waitScreen = libscreen.Screen()  # Obtendo uma tela de espera entre os estimulos
waitScreen.draw_fixation(fixtype="cross", pw=3)  # Desenhando uma cruz no centro da tela de 3px

circleObject = libscreen.Screen()  # Obtendo uma tela para a geracao de estimulos
circleSize = 100 # Tamanho do Circulo
mouseTry = libscreen.Screen()
trySize = 5

feedback = {}  # Criando um vetor de telas para ser usado no feedback do resultado
feedback[0] = libscreen.Screen()  # Obtendo a primeira tela para o vetor
feedback[0].draw_text(text="Errado!", colour=(255, 0, 0), fontsize=24)  # Configurando um texto para a tela de feedback negativa
feedback[1] = libscreen.Screen()  # Obtendo a segunda tela para o vetor
feedback[1].draw_text(text="Correto!", colour=(0, 255, 0), fontsize=24)  # Configurando um texto para a tela de feedback positiva

tracker.calibrate()  # Configurando e estabelecendo coneccao com o EyeTracker esse metodo chama libtime.expstart()

#if tracker.connected():  # Verifica se a coneccao com o EyeTracker foi bem sucedida
tracker.start_recording()  # Inicia a gravacao do experimento no arquivo de log do EyeTracker
display.fill(instructionScreen)  # Ativando a tela instrucoes no display
display.show() # Exibindo a tela ativada no display
keyboard.get_key()  # Esperando ate que a tecla espaco seja pressionada

#log.write(["Count", "Posicao", "PosicaoInicial", "PosicaoFinal", "Latencia", "Resultado"])  # Escrevendo no arquivo log o titulo do arquivo

for count0 in range(0,1):  # Rodando o experimento 3 vezes

	flag = False  # Variavel boolena usada para saber se a posicao ocular esta no centro da tela
	display.fill(waitScreen)  # Ativando a tela espera no display
	display.show()  # Exibindo a tela ativada no display

	tracker.status_msg("Trial: %d" % count0)  # Escreve uma mesagem de status no arquivo de log do EyeTracker com o numero da rodada no experimento
	display.fill(waitScreen)  # Ativando a tela espera no display
	display.show()  # Exibindo a tela ativada no display
	libtime.pause(1000)  # Pausando o experimento por 1 segundo

	position = (int(constants.DISPSIZE[0]*random.uniform(0.0, 1.0)), int(constants.DISPSIZE[1]*random.uniform(0.0, 1.0)))  # Calculando aleatoriamente a posicao do circulo do estimulo que sera exibida na tela
	circleObject.draw_circle(pos=position, r = circleSize, fill=True)  # Desenha um circulo preenchido na tela estimulo		

	display.fill(circleObject);  # Ativando a tela estimulo no display
	saccInicial = display.show();  # Exibindo a tela ativada no display e obtendo o tempo atual

	saccFinal, mouseStartPosition = tracker.wait_for_saccade_start()  # Esperando ate que comece o deslocamento ocular
	tempoFinal, positionInicial, mouseFinalPosition = tracker.wait_for_saccade_end()  # Esperando ate que termine o deslocamento ocular

	startTime = libtime.get_time()
	endTime = 0
	while not(flag):  # Enquando a posicao ocular na tela nao estiver no centro
		x,y = tracker.sample()
		distanceFromCircle = math.sqrt(((position[0] - x)**2) + ((position[1] - y)**2))
		
		if (distanceFromCircle <= 100):
			flag = True
			endTime = libtime.get_time()
	

	
	libtime.pause(500)
	circleObject.clear()# Limpando a tela para o proximo estimulo
	resultado = endTime - startTime	
	#log.write([count0, position, mouseStartPosition, mouseFinalPosition, saccFinal-saccInicial, resultado])  # Escrevendo no arquivo log os dados obtidos nessa rodada do experimento
	#display.fill(feedback[resultado])  # Ativando a tela de feedback correspondente do resultado no display
	resultScreen = libscreen.Screen()  # Obtendo uma tela para exibir as instrucoes do experimento
	time = str(resultado) + " ms"
	resultScreen.draw_text(text=time , colour=(0, 0, 255), fontsize=24)  # Configurando um texto para a tela de instrucoes
	display.fill(resultScreen)
	
	display.show()
	libtime.pause(2500)  # Exibindo a tela ativada no display
tracker.stop_recording()  # Para a gravacao dos dados no arquivo log do EyeTracker
log.close()  # Fecha o arquivo de log
tracker.close()  # Fecha a coneccao com o Eye Tracker
display.close()  # Fecha a coneccao com o display
libtime.expend()  # Termina o experimento
