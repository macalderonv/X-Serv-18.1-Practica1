#!/usr/bin/python3
import webapp
import urllib.parse

def form(): 
    respuesta = "<html><body>" + "<form id='formulario' action='' method='POST'>"+ "<h2>Acortar URLs:</h2>" + "<label>URL: </label>" + "<input type='text' name='url' style='color:grey'/>"+ '<input type="submit" value="Acortar">'+"</body></html>"
    return respuesta

class Web_acortadora_de_URLs(webapp.webApp):


    def parse(self, request):
        listaurls = (request.split()[0], request.split()[1], request) 
        return listaurls 

    def process(self, parsedRequest):
        try:
            urls = open('urls.csv', 'r')
            listaurls = urls.read()
            urls.close()
            try:
                contador = int(listaurls.split("/")[-2].split("<")[0]) + 1
                primero = 0
            except IndexError or ValueError :
                contador = 0
                primero = 1
        except IOError:
            urls = open('urls.csv', 'w')
            listaurls = ''
            contador = 0
            primero = 1
            urls.close()
        
        print(parsedRequest[0])
        if parsedRequest[0] == "GET":
            if parsedRequest[1] == "/":
                return ('200 OK', '<html><body>' + form() + "<br>" +listaurls + '</html></body>')
            elif "localhost:1234" + parsedRequest[1] + "<" in listaurls:
                url = listaurls.split('>' + 'localhost:1234' + parsedRequest[1] + "<")[0]
                url = url.split('=')[-1]
                return('302 Found', "<html>""<head><meta http-equiv='Refresh' content=" + "3;url=" + url + "></head>""<body><h1>Te estamos redirigiendo...</h1></body>""</html>")
            else:
                return ("404 Not Found", "<html><body><h2>" + "Recurso no encontrado" + "</html></body></h2>")

	
        elif parsedRequest[0] == "POST":
            url = parsedRequest[2].split("\r\n\r\n")[1].split("=")[1]
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            if url not in listaurls:
                link = "localhost:1234/" + str(contador)
                contador = contador + 1
                urls = open("urls.csv", 'a')
                urls.write("<br><b></b><a href=" + url + ">" + url + "</a> <b> --> </b> <a href=" + url + ">" + link + "</a><br>")
                urls.close()
            else:
                urls = open('urls.csv', 'r')

                print("lista: " + listaurls)

                link = listaurls.split(url + '>')[-1].split('<')[0]
                urls.close()

                print("link: " + link)
            return("200 OK", "<html><body><b></b><a href=" + url + ">" + url + "</a><b> --> </b><a href=" + url + ">" + link + "</a></body></html>")


        else:
            return ("404 Not Found", "<html><body><h2>" + "Recurso no encontrado" + "</html></body></h2>")	
                           

if __name__ == "__main__":
    testWebApp = Web_acortadora_de_URLs("localhost", 1234)
