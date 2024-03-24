import dht
import machine
from machine import Pin, I2C
import time
import ssd1306

# Definir o pino ao qual o sensor DHT22 está conectado
pinDHT = 23
pinLDR = 33

# Inicializar o sensor DHT22
sensorDHT = dht.DHT22(machine.Pin(pinDHT))
sensorLDR = machine.ADC(machine.Pin(pinLDR))

# Configurar o display OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Inicializar o botão
botao_pin = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP)

# Limite de luminosidade para distinguir entre manhã e noite
limite_luminosidade = 1000

# Variável para armazenar o modo de exibição atual

modos_exibicao = ['manha_noite', 'temperatura', 'umidade']
modo_exibicao = modos_exibicao[0]

def exibir_temperatura(temperatura):
    # Limpar o display
    oled.fill(0)

    # Escrever os valores na tela
    oled.text("Temp: {:.1f} C".format(temperatura), 0, 0)
    
    # Atualizar o display
    oled.show()

def exibir_umidade(umidade):
    # Limpar o display
    oled.fill(0)

    # Escrever os valores na tela
    oled.text("Umidade: {:.1f} %".format(umidade), 0, 16)
    
    # Atualizar o display
    oled.show()

def exibir_manha_noite(luminosidade):
    periodo = "Manha" if luminosidade > limite_luminosidade else "Noite"
    # Limpar o display
    oled.fill(0)

    # Escrever os valores na tela
    # oled.text("Luminosidade: {}".format(luminosidade), 0, 0)
    oled.text("Periodo: {}".format(periodo), 0, 16)
    
    # Atualizar o display
    oled.show()

while True:
    try:
        # Realizar a leitura dos dados do sensor
        sensorDHT.measure()
        
        # Obter os valores de temperatura e umidade
        temperatura = sensorDHT.temperature()
        umidade = sensorDHT.humidity()

        # Ler o valor do sensor LDR
        luminosidade = sensorLDR.read()

        # Ler o estado do botão
        botao_pressionado = not botao_pin.value()

        # Verificar se o botão foi pressionado
        if botao_pressionado:
            if modo_exibicao == modos_exibicao[0]:
                modo_exibicao = modos_exibicao[1]
            elif modo_exibicao == modos_exibicao[1]:
                modo_exibicao = modos_exibicao[2]
            else:
                modo_exibicao = modos_exibicao[0]

        # Atualizar o modo de exibição
        if modo_exibicao == modos_exibicao[0]:
            exibir_temperatura(temperatura)
        elif modo_exibicao == modos_exibicao[1]:
            exibir_umidade(umidade)
        else:
            exibir_manha_noite(luminosidade)
    
    except OSError as e:
        print("Erro ao ler dados do sensor:", e)

      # Aguardar um curto período para evitar leituras rápidas do botão
    time.sleep(0.1)