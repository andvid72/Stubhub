from bs4 import BeautifulSoup
import re
#----------------------
def get_seats(html_content,list_seats,stacker):
	# obtiene html
	soup = BeautifulSoup(html_content, "lxml") #HTML de la etiqueta id="listings-container" y todo lo que tiene dentro

	# seat class
	html_string = str(soup.div.div).replace('\n','') # HTML de la primera etiqueta de clase 'clase con el fin de obtener el string del nombre de la clase dinamica
	match = re.search('(?<=class=")(.*?)(?= )', html_string); clase0 = match.group(1) if match else None
	match = re.search(rf"\b{clase0} \b(.*?)(?= )", html_string); clase1 = match.group(1) if match else None
	clase = 'div.' + clase0 + '.' + clase1
	html_class =soup.select(clase) #lista con todas las tags con clase 'clase'

	# verifica que se hayan obtenido nuevos asientos
	if len(html_class) == stacker: 
		return(list_seats,stacker)

	# loop buscando asientos
	session_stacker = stacker
	for y in range(session_stacker,len(html_class)):
		# seat
		seat = str(html_class[y])
		session_stacker += 1

		#Score
		match = re.search(r"(?<=)(\d\.\d)(?=\<)", seat)
		Score = match.group(0) if match else None

		#Section
		match = re.search(r'(?<=Section )(.*?)(?=\<)', seat)
		Section = match.groups(1)[0] if match else None

		#Row
		match = re.search(r'(?<=Row )(.*?)(?=\<)', seat)
		Row = match.groups(1)[0] if match else None

		#Price
		match = re.search(r'(?<=\$)(.*?)(?=\")', seat)
		Price = match.group(0).replace(",", "") if match else None

		#evaluacion
		if not Section and not Row and not Price: 
			continue
		list_seats.append([Section,Row,Price,Score])
		# list_seats.append([Section,Row,Seats,Zone,Price,Score])
		stacker = session_stacker

	return(list_seats,stacker)
#----------------------
# def script_executor():







