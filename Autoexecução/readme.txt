Os dados dos pesquisadores do ICMC foram obtidos com a ferramente scriptLattes.
Após a execução dessa ferramenta, convertemos o arquivo XML para um formato JSON,
mais apropriado para a execução do Avro. Definimos o nosso schema de modo a
armazenar os colaboradores e o ID de cada pesquisador e salvamos nesse arquivo,
todos os pesquisadores com seus devidos colaboradores.Para a execução no Apache
Giraph, durante a criação dos arquivos do Avro, o arquivo DataSimpleGraph.txt
sera usado como input do job do Giraph.
