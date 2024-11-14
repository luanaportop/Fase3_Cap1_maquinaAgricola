#include <DHT.h>  // Inclui a biblioteca para trabalhar com o sensor DHT (temperatura e umidade)

// Definição dos pinos
#define PINO_DHT 19          // Pino do DHT22 (Sensor de Temperatura e Umidade)
#define TIPO_DHT DHT22       // Tipo do sensor DHT (especificamente o DHT22)
#define PINO_LDR 32          // Pino analógico para o "sensor de umidade" (simulado pelo LDR)
#define PINO_RELE 26         // Pino digital para o controle do relé (controle da bomba)
#define PINO_POTASSIO 33     // Pino digital para o botão de potássio
#define PINO_FOSFORO 25      // Pino digital para o botão de fósforo

// Criação de um objeto da classe DHT para inicializar e controlar o sensor DHT
DHT dht(PINO_DHT, TIPO_DHT);

// Definição de um limite para o nível de umidade do solo
const int LIMITE_UMIDADE_SOLO = 1800; // Ajuste o valor conforme necessário para o nível de umidade desejado

void setup() {
  // Inicialização da comunicação serial para o monitor serial
  Serial.begin(115200);

  // Inicializa o sensor DHT
  dht.begin();

  // Configura os pinos do LDR e do relé
  pinMode(PINO_LDR, INPUT); // Configura o pino do LDR como entrada
  pinMode(PINO_RELE, OUTPUT); // Configura o pino do relé como saída

  // Configura os pinos dos botões com resistores pull-up internos
  pinMode(PINO_POTASSIO, INPUT_PULLUP);  // Configura o botão de potássio como entrada com resistor pull-up
  pinMode(PINO_FOSFORO, INPUT_PULLUP);   // Configura o botão de fósforo como entrada com resistor pull-up

  // Inicializa o estado do relé (bomba) como desligado
  digitalWrite(PINO_RELE, LOW);

  delay(800); // Aguarda 2 segundos para o sensor DHT22 estabilizar após a inicialização
}

void loop() {
  // Leitura do "sensor de umidade do solo", que está sendo simulado pelo LDR
  int valorUmidadeSolo = analogRead(PINO_LDR); // Lê o valor do LDR (quanto menor o valor, maior a umidade)

  // Leitura dos valores de temperatura e umidade do sensor DHT22
  float temperatura = dht.readTemperature();  // Lê a temperatura
  float umidade = dht.readHumidity();       // Lê a umidade relativa

  // Leitura dos botões de potássio e fósforo
  bool potassioPresente = digitalRead(PINO_POTASSIO) == HIGH; // Verifica se o botão de potássio está pressionado
  bool fosforoPresente = digitalRead(PINO_FOSFORO) == LOW;   // Verifica se o botão de fósforo está pressionado

  // Controle da bomba de água com base na umidade do solo
  bool bombaLigada = false; // Variável para armazenar o estado da bomba
  if (valorUmidadeSolo < LIMITE_UMIDADE_SOLO) {  // Se a umidade do solo estiver abaixo do limite
    digitalWrite(PINO_RELE, HIGH);  // Liga a bomba (relé)
    bombaLigada = true; // Marca a bomba como ligada
  } else {
    digitalWrite(PINO_RELE, LOW);   // Desliga a bomba (relé)
    bombaLigada = false; // Marca a bomba como desligada
  }

  // Exibe todas as leituras e o status no monitor serial
  Serial.println("===== Leitura dos Sensores =====");
  Serial.print("Valor da Umidade do Solo: ");
  Serial.println(valorUmidadeSolo); // Exibe o valor de umidade do solo

  // Verifica se houve erro na leitura do sensor DHT
  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Falha ao ler o sensor DHT!"); // Caso a leitura falhe
  } else {
    // Exibe os valores de temperatura e umidade
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.println(" °C");

    Serial.print("Umidade Relativa: ");
    Serial.print(umidade);
    Serial.println(" %");
  }

  // Exibe os estados dos botões de potássio e fósforo
  Serial.print("Potássio: ");
  Serial.println(potassioPresente ? "Presente" : "Ausente");

  Serial.print("Fósforo: ");
  Serial.println(fosforoPresente ? "Presente" : "Ausente");

  // Exibe o estado da bomba de água
  Serial.print("Bomba de Água: ");
  Serial.println(bombaLigada ? "Ligada" : "Desligada");

  // Finaliza a leitura com uma linha de separação
  Serial.println("===============================");
  Serial.println();

  // Aguarda 10 segundos antes de realizar a próxima leitura
  delay(10000); // Intervalo de 10 segundos entre as leituras
}