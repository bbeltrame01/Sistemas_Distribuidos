 
  void setup() { 
   pinMode(LED_BUILTIN, OUTPUT);
   Serial.begin(9600);
  }
    
  /**
   * Função que lê uma string da Serial
   * e retorna-a
   */
  String leStringSerial(){
    String conteudo = "";
    char caractere;
    
    // Enquanto receber algo pela serial
    while(Serial.available() > 0) {
      // Lê byte da serial
      caractere = Serial.read();
      // Ignora caractere de quebra de linha
      if (caractere != '\n'){
        // Concatena valores
        conteudo.concat(caractere);
      }
      // Aguarda buffer serial ler próximo caractere
      delay(10);
    }
      
    Serial.print("Recebi: ");
    Serial.println(conteudo);
      
    return conteudo;
  }
    
  void loop() {
    // Se receber algo pela serial
    if (Serial.available() > 0){
      // Lê toda string recebida
      String recebido = leStringSerial();
        
      if (recebido == "1"){
          printf("%s", recebido);
        digitalWrite(LED_BUILTIN, HIGH);
      }
        
      if (recebido == "0"){
        printf("%s", recebido);
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
