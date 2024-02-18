function calcular() {
    const vidroPeso = parseFloat(document.getElementById('vidroPeso').value) || 0;
    const papelPeso = parseFloat(document.getElementById('papelPeso').value) || 0;
    const metalPeso = parseFloat(document.getElementById('metalPeso').value) || 0;
    const plasticoPeso = parseFloat(document.getElementById('plasticoPeso').value) || 0;
  
    const pontuacaoVidro = 1;
    const pontuacaoPapel = 10;
    const pontuacaoMetal = 15;
    const pontuacaoPlastico = 25;
  
    const resultadoVidro = pontuacaoVidro * vidroPeso;
    const resultadoPapel = pontuacaoPapel * papelPeso;
    const resultadoMetal = pontuacaoMetal * metalPeso;
    const resultadoPlastico = pontuacaoPlastico * plasticoPeso;
  
    const totalGeral = resultadoVidro + resultadoPapel + resultadoMetal + resultadoPlastico;
  
    document.getElementById('totalGeral').textContent = totalGeral;
  }
  