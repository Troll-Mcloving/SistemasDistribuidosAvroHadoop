#!python3
#encoding=utf-8


import os
from pathlib import Path
import xml.etree.ElementTree as ElementTree
import colorama
from pprint import pprint
from Print import Print
import json
import bisect
import sys
colorama.init()


# o arquivo que faremos a
# leitura está em
pathSrc = Path('ICMC/teste-01-database.xml')


class Database:

     # as maneiras de como os dados deve ser mantidos na hora da comparação entre configFiles
    manterDados = {
        'novosDados': set([ # set, pois trabalha mais rápido do que uma list
            # aqui, os dados novos repetidos são apagados,
            # e são mantidos apenas os que não estavam presentes
            'colaboradores', 'formacao_academica', 'projetos_pesquisa', 'premios_titulos', 'artigos_em_periodicos', 'livros_publicados', 'capitulos_livros', 'trabalho_completo_congresso', 'resumo_expandido_congresso', 'resumo_congresso', 'producao_bibliografica', 'trabalhos_tecnicos', 'producao_tecnica', 'orientacao_doutorado_em_andamento', 'orientacao_mestrado_em_andamento', 'orientacao_doutorado_concluido', 'orientacao_mestrado_concluido', 'orientacao_tcc_concluido', 'orientacao_iniciacao_cientifica_concluido', 'organizacao_evento', 'orientacao_especializacao_concluido', 'orientacao_tcc_em_andamento', 'produto_tecnologico', 'supervisao_pos_doutorado_concluido', 'orientacao_outros_tipos_concluido', 'supervisao_pos_doutorado_em_andamento', 'producao_artistica', 'orientacao_iniciacao_cientifica_em_andamento', 'artigos_em_revista', 'processo_tecnica', 'texto_em_jornal', 'orientacao_outros_tipos_em_andamento', 'participacao_evento', 'apresentacao_trabalho'
        ]),
        'maisNovo': [
            # aqui ficam os dados que não são necessários para comparação
            'identificacao', 'idiomas', 'endereco', 'area_atuacao'
        ],

        'movidos': [
            # aqui ficam tuplas de campos que terão os elementos movidos, ou seja
            # devo analisar essas tuplas
            ('orientacao_doutorado_em_andamento', 'orientacao_doutorado_concluido'),
            ('orientacao_iniciacao_cientifica_em_andamento', 'orientacao_iniciacao_cientifica_concluido'),
            ('orientacao_mestrado_em_andamento', 'orientacao_mestrado_concluido'),
            ('supervisao_pos_doutorado_em_andamento', 'supervisao_pos_doutorado_concluido'),
            ('orientacao_outros_tipos_em_andamento', 'orientacao_outros_tipos_concluido'),
            ('artigos_em_revista', 'artigos_em_periodicos')
            # esse é o versa do de cima
            # houve apenas um caso em todo o caso de teste
            # ('artigos_em_periodicos', 'artigos_em_revista')
        ],
    }

    # campos que serão analisados para dizer se os dict são parecidos
    camposImportantes = set(['titulo', 'nome', 'descricao', 'titulo_trabalho'])
    # aqui vão os campos para não analisarmos
    # costumava ser 'autores', mas eu resolvi deixar vazio
    # deve ser do tipo set
    camposNaoAnalisar = set(['ano', 'Data', 'ano_inicio', 'ano_conclusao'])


    def __init__(self, path):
        self.path = path


    def loadXml(self):
        xmlFilePath = self.path
        print(colorama.Fore.YELLOW+'Carregando arquivo xml:'+colorama.Fore.RESET, xmlFilePath)
        if not os.path.exists(str(xmlFilePath)):
            print('O arquivo XML "%s" não existe.' % str(xmlFilePath))
            print('Por favor, rode o scriptLattes para esse arquivo de configuração: %s' % str(self.filePath))
            sys.exit(0)


        # no xml que o scriptLattes gera
        # o caracter & não é substituido por
        # &amp;
        # vamos verificar se existe o text &amp;
        # se não, vamos substituir todos os
        # & por &amp;
        with open(str(xmlFilePath), 'r', encoding='utf-8') as file:
            fileContent = file.read()

        if '&amp;' not in fileContent:
            # esse arquivo precisa trocar & por &amp;
            fileContent = fileContent.replace('&', '&amp;')
            # agora é só salvar no arquivo
            with open(str(xmlFilePath), 'w', encoding='utf-8') as file:
                file.write(fileContent)


        self.xml = ElementTree.parse(str(xmlFilePath))
        self.data_processamento = self.xml.getroot().attrib['data_processamento']
        return self.xml


    def loadJsonFromXml(self):
        root = self.xml.getroot()
        self.json = {}

        def childText(child):
            '''Retorna a string existente dentro de um child
            exemplo: <child>Oi, texto! <i>ComoVai</i>, <b>Por que deixaram isso?</b></child>
            retorna: Oi, texto! ComoVai, Por que deixaram isso?'''
            return "".join(child.itertext())

        def childNomeComum(xml):
            children = xml.getchildren()
            if len(children) < 2:
                return ''
            elif children[0].tag == children[1].tag:
                return children[0].tag
            return ''

        def _xmlToJson(xml, profundidade=1):
            result = {}
            if not xml.getchildren():
                # se for o último filho, retorna seu valor
                return childText(xml)

            # eu tenho filhos!!
            if profundidade >= 4:
                # mas provavelmente, meu filho é um <i> ou <b>
                return childText(xml)


            # se não for filho, retorna um dicionário
            for child in xml:
                if result.get(child.tag):
                    # se já existe esse elemento dentro de result
                    # soma-se o resultado ao vetor
                    result[child.tag] += [_xmlToJson(child, profundidade+1)]
                else:
                    # se não, cria um novo vetor
                    result[child.tag] = [_xmlToJson(child, profundidade+1)]
            return result


        def compactJson(json):
            '''Os valores de json estão sempre em listas
            esta função deixa o que é lista como lista
            e o que não deve ser lista, como elemento único'''
            # apos ter recebidos todos os parametros
            # deixa o que é lista, e retira a lista de qm precisa
            tratarComoLista = Database.manterDados['novosDados'].union(['colaboradores', 'idiomas', 'area_atuacao'])
            for child in tratarComoLista:
                # verifica se child esta em json
                if child in json:
                    # apenas ovtem o elemento correto
                    json[child] = list(json[child][0].values())[0]
                    # os elementos desse json são um array, deixa como valores simples
                    if child in ['colaboradores', 'idiomas', 'area_atuacao']:
                        continue
                    for i in json[child]:
                        for filho in i:
                            i[filho] = i[filho][0]
                else:
                    # cria um novo elemento para ter sempre todos os elementos para comparar
                    json[child] = []
            # agora, compara os childs se não são listas
            def naoSaoListas(json):
                if isinstance(json, str):
                    # cheguei numa string já, não preciso continuar
                    return
                for child in json:
                    if child not in tratarComoLista:
                        json[child] = json[child][0]
                        # chama recursivo para os filhos dele
                        naoSaoListas(json[child])
            naoSaoListas(json)

        for pesquisador in root:
            i = pesquisador.attrib['id'] # deve ser tratado como string

            Print.back('Analisando: %s Data: %s' % (i, self.data_processamento))

            # para evitar o caso de 0001
            # se tornar 1, porque é inteiro
            self.json[i] = _xmlToJson(pesquisador)
            compactJson(self.json[i])

            # antes eu imprimia os idLattes nesse ponto
            # porém, é muito rápida a leitura
            # nem vale a pena imprimir
            # self.printPesquisador(i)

        Print.back('XML Data %s => Completado' % self.data_processamento)
        Print.endBack()
        return self.json




db = Database(pathSrc)
if os.path.exists('json.js'):
    with open('json.js', 'r', encoding='utf-8') as file:
        db.json = json.load(file)
else:
    db.loadXml()
    db.loadJsonFromXml()

    # vamos salvar o arquivo para análise
    # este é o json traducional como conhecemos
    with open('json.js', 'w', encoding='utf-8') as file:
        file.write(json.dumps(db.json,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
                ensure_ascii=False
            ))

# aqui, os dados produzidos pelo arquivo JSON sao escritos em formato de grafo,
# onde cada linha eh no formato source_id distance dest_id:dest_id:dest_id....
# note que  nao estamos interessados em arestas com peso, mas somente as ligacoes
# entre os nos

def getKey(item):
	return item[0]

nodes = list(sorted(db.json))
for i in sorted(db.json):
	for j in sorted(db.json[i]["colaboradores"]):
		found = 0
		if i != j:
			for k in nodes:
				if k == j:
					found = 1
			if found != 1:
				bisect.insort(nodes, j)
source = []
target = []
for i in sorted(db.json):
	for j in sorted(db.json[i]["colaboradores"]):
		first = -1
		second = -1
		for k in range (0, len(nodes)):
			if nodes[k] == i:
				first = k
			if nodes[k] == j:
				second = k
		if first != second:
			source.insert(len(source), first)
			source.insert(len(source), second)
			target.insert(len(target), second)
			target.insert(len(target), first)

final = []
for i in range (0, len(source)):
	temp = [source[i], target[i]]
	t = tuple(temp)
	final.insert(len(final), t)

# print(source)
# print(target)

final = sorted(final, key=getKey)

for j in range (0, len(nodes)):
	f = open("./Data/LattesGraph" + str(j) + ".txt", 'w')
	a = -1
	for i in final:
		if a != i[0]:
			a = i[0]
			if a != 0:
				f.write("\n")
			if a != j:
				f.write(str(i[0]) + " 1000 " + str(i[1]) + ":")
			else:
				f.write(str(i[0]) + " 0 " + str(i[1]) + ":")
		else:
			f.write(str(i[1]) + ':')

# # agora vem a parte com o avro
# from pprint import pprint
# import avro
# import avro.schema
# from avro.datafile import DataFileReader, DataFileWriter
# from avro.io import DatumReader, DatumWriter
#
#
# # vamos ver os campos possíveis
# pesquisadores = db.json
#
# # vamos ler o esquema
# schema = avro.schema.Parse(open("Pesquisador.avsc").read())
#
#
# writer = DataFileWriter(open("Pesquisador.avro", "wb"), DatumWriter(), schema)
# for p in pesquisadores:
#     # gravando os colaboradores
#     writer.append({"colaboradores": ', '.join(pesquisadores[p]['colaboradores']), "id": p})
# writer.close()
