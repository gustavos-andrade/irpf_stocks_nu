# Compilador de Notas de Negociação de Ativos Nuinvest/Nubank
## Objetivo
O presente código tem como objetivo ler todas as Notas de negociação Nubank e compilar em uma prática planilha Excel para auxiliar na declaração da quantidade e preço médio dos ativos negociados em bolsa.

## Resultados
O código retorna uma planilha com a aba _Negociacoes_ que contém o registro de todas as transações organizadas por data.
A aba _Pmedio_ entrega um resumo da quantidade de ações, o valor total, o preço médio e a descrição para ser adicionada no campo _Observações_ do aplicativo da receita.
O _csv_ companies_b3 possui o Ticker, o nome e CNPJ de grande parte dos ativos listados na B3 e também pode ser muito útil para consultas.

## Funcionamento
Todas as notas devem ser adicionadas à pasta **invoice** para que o código leia e retorne a planilha.
As notas devem estar no mesmo formato do apresentado no aplicativo. Caso sejam obtidas solicitando via portal de relacionamento da Nubank, deve ser solicitado uma pasta com todas as notas no mesmo formato das obtidas pelo aplicativo.

## Importante
O código tem como simples intuito de ajudar o usuário a avaliar e comparar as métricas calculadas. **Todas as informações devem ser conferidas.**

**O usuário deve estar ciente que o código está em fase de testes e o uso é de própria responsabilidade do usuário**
