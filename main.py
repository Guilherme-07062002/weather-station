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

# Limite de luminosidade para distinguir entre manhã e noite
limite_luminosidade = 1000

while True:
    try:
        # Realizar a leitura dos dados do sensor
        sensorDHT.measure()
        
        # Obter os valores de temperatura e umidade
        temperatura = sensorDHT.temperature()
        umidade = sensorDHT.humidity()

        # Ler o valor do sensor LDR
        luminosidade = sensorLDR.read()

        # Determinar se é manhã ou noite
        periodo = "Manha" if luminosidade > limite_luminosidade else "Noite"
        
        # # Exibir os dados no console
        # print("Temperatura: {}°C, Umidade: {}%, Valor LDR: {}".format(temperatura, umidade, valor_ldr))

        # Limpar o display
        oled.fill(0)

        # Escrever os valores na tela
        oled.text("Temp: {:.1f} C".format(temperatura), 0, 0)
        oled.text("Umidade: {:.1f} %".format(umidade), 0, 16)
        # oled.text("Lumi: {}".format(luminosidade), 0, 32)
        oled.text("Periodo: {}".format(periodo), 0, 48)

        # Atualizar o display
        oled.show()
    
    except OSError as e:
        print("Erro ao ler dados do sensor:", e)
    
    # Aguardar 2 segundos antes de realizar a próxima leitura
    time.sleep(2)