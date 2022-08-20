#Criando estrutura global para receber os dados coletados
dados = {
    "Resolucao" : [],
    "Empresa" : [],
    "Autorizacao" : [],
    "Marca" : [],
    "Processo" : [],
    "Registro" : [],
    "Venda e Emprego" : [],
    "Vencimento" : [],
    "Apresentacao" : [],
    "Validade Produto" : [],
    "Categoria" : [],
    "Assunto Peticao" : [],
    "Expediente e Peticao" : [],
    "Versao" : []
}

def coleta_links(url_entrada):
    """"
    Função que retornará os links de  cada Resolução contidos na  pesquisa.
    Bibliotecas usadas: selenium e bs4 (BeautifulSoup).
    - selenium permitirá o acesso ao site através de um navegador. Será utilizado o navegador Google Chrome.
    - BeautifulSoup permite que façamos a busca no HTML da página para retirar as informações que queremos para essa etapa.
    """
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options

    #Abrindo o Chrome no modo headless
    opcao = Options()
    opcao.add_argument("--headless")
    #Abrindo a página
    driver = webdriver.Chrome('chromedriver',options=opcao)
    WebDriverWait(driver, timeout=3)
    driver.get(url_entrada)

    #Retirando o HTML da página para filtrar os links das publicações
    elementos=driver.find_element("id","_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_hierarchy_content").get_attribute("innerHTML")
    soup=BeautifulSoup(elementos,"html.parser")
    links=[link["href"] for link in soup.find_all("a",href=True)]

    return links

def adiciona_instancia(resolucao):
    """""
    Cria uma nova instância dentro da variável "dados".
    Função necessária uma vez que a mesma resolução possui várias instâncias dos outros campos
    """
    global dados
    dados["Resolucao"].append(resolucao)
    dados["Empresa"].append('')
    dados["Autorizacao"].append('')
    dados["Marca"].append('')
    dados["Processo"].append('')
    dados["Registro"].append('')
    dados["Venda e Emprego"].append('')
    dados["Vencimento"].append('')
    dados["Apresentacao"].append('')
    dados["Validade Produto"].append('')
    dados["Categoria"].append('')
    dados["Assunto Peticao"].append('')
    dados["Expediente e Peticao"].append('')
    dados["Versao"].append('')


def coletor_dados(publicacoes):

    """
    Função para coletar os dados de fato.
    Bibliotecas utilizadas: bs4(BeautifulSoup) e requests
    - requests permite obter o conteúdo de uma página em HTML
    """
    from bs4 import BeautifulSoup
    import requests

    global dados

    prefixo= "https://www.in.gov.br"


    #Percorrerá cada publicação para selecionar os campos que quer-se obter
    for  publicacao in publicacoes:
        pagina=requests.get(prefixo+publicacao)
        soup=BeautifulSoup(pagina.text,"html.parser")
        conteudo=soup.find('div', class_ = "texto-dou")


        #Extraíndo a Resolução e criando uma nova entrada em "dados" 
        resolucao=conteudo.find('p', class_ = 'identifica').text
        adiciona_instancia(resolucao)

        #Separando o resto do texto para extração dos outros dados
        resto_texto=conteudo.find_all('p', class_ = 'dou-paragraph')

        """"
        É necessário percorrer linha a linha, uma vez que não há id para as próximas classes
        Dividimos  cada linha pelos dois pontos, resultando no retorno do campo e do conteúdo separados
        """
        for linha in resto_texto:
            linha_unica=linha.text.split(":")
            #Tratamento de qual campo aquela linha possui, para então adicionar em dados.
            if linha_unica[0] == 'NOME DA EMPRESA':
                dados["Empresa"].pop()
                dados["Empresa"].append(linha_unica[1])
            elif linha_unica[0] == 'AUTORIZAÇÃO':
                dados["Autorizacao"].pop()
                dados["Autorizacao"].append(linha_unica[1])
            elif linha_unica[0] == 'NOME DO PRODUTO E MARCA':
                dados["Marca"].pop()
                dados["Marca"].append(linha_unica[1])
            elif linha_unica[0] == 'NUMERO DE PROCESSO':
                dados["Processo"].pop()
                dados["Processo"].append(linha_unica[1])
            elif linha_unica[0] == 'NUMERO DE REGISTRO':
                dados["Registro"].pop()
                dados["Registro"].append(linha_unica[1])
            elif linha_unica[0] == 'VENDA E EMPREGO':
                dados["Venda e Emprego"].pop()
                dados["Venda e Emprego"].append(linha_unica[1])
            elif linha_unica[0] == 'VENCIMENTO':
                dados["Vencimento"].pop()
                dados["Vencimento"].append(linha_unica[1])
            elif linha_unica[0] == 'APRESENTAÇÃO':
                dados["Apresentacao"].pop()
                dados["Apresentacao"].append(linha_unica[1])
            elif linha_unica[0] == 'VALIDADE DO PRODUTO':
                dados["Validade Produto"].pop()
                dados["Validade Produto"].append(linha_unica[1])
            elif linha_unica[0] == 'CATEGORIA':
                dados["Categoria"].pop()
                dados["Categoria"].append(linha_unica[1])
            elif linha_unica[0] == 'ASSUNTO DA PETIÇÃO':
                dados["Assunto Peticao"].pop()
                dados["Assunto Peticao"].append(linha_unica[1])
            elif linha_unica[0] == 'EXPEDIENTE DA PETIÇÃO':
                dados["Expediente e Peticao"].pop()
                dados["Expediente e Peticao"].append(linha_unica[1])
            elif linha_unica[0] == 'VERSÃO':
                dados["Versao"].pop()
                dados["Versao"].append(linha_unica[1])
            #Caso todos campos já tenham sido preenchidos, cria-se uma nova instância dentro de "dados" para a mesma Resolução
            elif linha_unica[0][0] == '_': adiciona_instancia(resolucao)


def gera_excel(nome):
    #Utilizando o pandas (e sua estrutura Data Frame) para a criação do arquivo .xlsx utilizando o nome passado como argumento
    import pandas as pds
    global data

    dataframe=pds.DataFrame(dados)
    dataframe.to_excel(nome+".xlsx")

def main():

    url_entrada='https://www.in.gov.br/consulta/-/buscar/dou?q="deferir+os+registros+e+as+petições+dos+produtos+saneantes"&s=todos&exactDate=personalizado&sortType=0&publishFrom=01-01-2022&publishTo=28-02-2022'

    publicacoes=coleta_links(url_entrada)

    coletor_dados(publicacoes)

    gera_excel("resultado")


import time
if __name__ == "__main__":
    #Mede o tempo de execução do programa
    start_time = time.process_time()
    main()
    print("--- %s seconds ---" % (time.process_time() - start_time))