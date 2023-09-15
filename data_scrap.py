from bs4 import BeautifulSoup as bs
import httpx
import json
import datetime
# import re
# import cloudscraper
# scraper = cloudscraper.create_scraper()

def get_farmacias(output_raw = False):
	api_url = "https://farmaciasdeturnotandil.com.ar/api/turno"
	response = httpx.get(api_url).text
	data = json.loads(response)
	
	if output_raw:
		return data

	# farm_1 = data["deTurnoAhora"][0][]
	farmacias = """'{f_nombre1}' direccion: {f_direcc1}, 
		'{f_nombre2}' direccion: {f_direcc2}, 
		'{f_nombre3}' direccion: {f_direcc3}
	""".format(
		f_nombre1 = data["deTurnoAhora"][0]["nombre"],
		f_direcc1 = data["deTurnoAhora"][0]["direccion"],
		f_nombre2 = data["deTurnoAhora"][1]["nombre"],
		f_direcc2 = data["deTurnoAhora"][1]["direccion"],
		f_nombre3 = data["deTurnoAhora"][2]["nombre"],
		f_direcc3 = data["deTurnoAhora"][2]["direccion"]
	)
	return farmacias

def get_clima(output_raw = False):
	
	def degrees_to_cardinal(deg):
		# dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
		dirs = ["Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste", "Oeste", "Noroeste"]
		ix = int((deg + 11.25)/22.5)
		return dirs[ix % 8]

	api_url = "https://api.openweathermap.org/data/2.5/weather?lat=-37.3164338&lon=-59.1156571&units=metric&lang=es&appid=74bda5d816b2de1112d0252d333765aa"
	response = httpx.get(api_url).text
	data = json.loads(response)

	if output_raw:
		return data

	clima = """{desc}, Temp: {temp}°C, Sensasion Termica: {sens}, Viento: {wind}km\\h
	Detalles:
		Temp Max: {temp_max}, Temp Min: {temp_min}
		Humedad: {humd}%
		Viento: {wind}km\\h {dire}
		Ciudad: Tandil
	""".format(
		desc = data["weather"][0]["description"],
		temp = data["main"]["temp"],
		humd = data["main"]["humidity"],
		wind = data["wind"]["speed"],
		dire = degrees_to_cardinal(data["wind"]["deg"]),
		temp_max = data["main"]["temp_max"],
		temp_min = data["main"]["temp_min"],
		sens = data["main"]["feels_like"]
	)
	return clima

def get_fecha_hora():
	return datetime.datetime.now()

def get_precio_dolar():

	url = "https://www.dolar.blue/"
	response = httpx.get(url).text
	soup = bs(response, "lxml")
	dolars = soup.find_all("p", class_="price-blue")
	dolar = dolars[2].text
	dolar = dolar.replace("'", "")
	return dolar