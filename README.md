# Sistema de Irrigação Inteligente - FarmTech Solutions

## Instruções para rodar código python:
instalar a biblioteca oracledb
instalar a biblioteca pandas
importar biblioteca os

Adicionar o usuário e senha na conexão do banco de dados.

## Instruções para rodar código C++:
instalar a biblioteca DHT sensor library
instalar a biblioteca DHT22

## Sobre o Projeto
Este projeto foi desenvolvido como parte do primeiro semestre da faculdade de IA, onde criamos um sistema de irrigação inteligente para a empresa FarmTech Solutions. Na terceira fase do projeto, usamos sensores e um microcontrolador para monitorar o solo e automatizar a irrigação de acordo com as condições atuais. Tudo isso foi feito em um ambiente de simulação, usando o Wokwi, uma plataforma online para testar o hardware.

## Contexto
A ideia é conectar sensores ao microcontrolador ESP32 para ler níveis de umidade, pH, fósforo (P) e potássio (K) no solo. Usamos substituições criativas para alguns sensores:
- Botões para simular os sensores de nutrientes P e K
- LDR (sensor de luz) para simular o pH
- DHT22 para medir a umidade do solo

Com esses dados, o ESP32 controla um relé (representando uma bomba de irrigação) e liga ou desliga a irrigação automaticamente, dependendo das condições do solo.

## Funcionalidades do Projeto
- **Monitoramento em tempo real:** Coleta e análise dos dados de umidade, pH, P e K.
- **Irrigação Automática:** O relé liga a irrigação quando os níveis de umidade, nutrientes ou pH precisam de ajuste.
- **Banco de Dados:** Armazenamento dos dados dos sensores e histórico de irrigação em um banco de dados Oracle, onde podemos adicionar, ler, atualizar e deletar dados (funções CRUD).

## Componentes do Projeto
- **ESP32:** Processa os dados dos sensores e controla o relé.
- **Sensores Simulados:**
  - DHT22: Monitora a umidade do solo.
  - LDR: Representa a leitura de pH.
  - Botões: Simulam os sensores de fósforo (P) e potássio (K).
- **Relé:** Representa a bomba de irrigação.
- **Banco de Dados Oracle:** Armazena os dados dos sensores e do sistema de irrigação.

## Lógica de Decisão para Irrigação
A lógica de irrigação foi definida pelo grupo e funciona da seguinte maneira:
- Umidade abaixo de 30%: Irrigação ligada.
- Botão de P ou K pressionado (indicando falta de nutrientes): Irrigação ligada.

## Imagens do circuito
![image](https://github.com/user-attachments/assets/3e70c754-bc6e-4956-9604-3a58894b19eb)
![image](https://github.com/user-attachments/assets/f97a2b7f-f2fa-465c-8288-7a8903490d66)


