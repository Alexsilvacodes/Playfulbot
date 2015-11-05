# -*- coding: utf-8 -*-
#
# 2014 Alex Silva <alexsilvaf28 at gmail.com>

import urllib, mechanize
from bs4 import BeautifulSoup
from PyQt4 import QtCore, QtGui

class PlayfulbotCore(QtCore.QObject):
	signalLogin = QtCore.pyqtSignal(bool)
	signalUserData = QtCore.pyqtSignal(dict)

	def __init__(self, user=None, password=None):
		super(PlayfulbotCore, self).__init__()
		self.user = user
		self.password = password

	def setLogin(self, user):
		self.user = user

	def setPassword(self, password):
		self.password = password

	def login(self):
		# Create Form
		form_data = {
			"user[login]": self.user,
			"user[password]": self.password
		}

		try:
			self.mbrowser = mechanize.Browser()
			self.mbrowser.set_handle_robots(False)
			self.mbrowser.set_handle_equiv(False)
			self.mbrowser.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36')]
			self.mbrowser.open("http://playfulbet.com/users/sign_in")
			self.mbrowser.select_form(nr=0)
			for key in form_data:
				self.mbrowser.form[key] = form_data[key]
			self.mainpage_loggedin = self.mbrowser.submit()

			self.parser_mainpage = BeautifulSoup(self.mainpage_loggedin.read())
			promo = self.parser_mainpage.findAll("a", {"href": "http://playfulbet.com/promociones"})
			self.connected = len(promo) > 1
			self.signalLogin.emit(self.connected)
		except mechanize.URLError, e:
			print e
			self.signalLogin.emit(False)

	def userData(self):
		try:
			self.parser_profile = BeautifulSoup(self.mbrowser.follow_link(url_regex="/usuarios"))
			user_data = {}
			print "aqui1"
			image_profile_url = self.parser_profile.findAll("img", {"class": "avatar_img"})[0]["src"]
			if "http" not in image_profile_url:
				image_profile_url = "http://playfulbet.com" + image_profile_url
			image_data = QtCore.QByteArray.fromRawData(urllib.urlopen(image_profile_url).read())
			user_data['userimage'] = image_data
			user_data['username'] = self.parser_profile.findAll("a", {"class": "user-list__title"})[0].string
			user_data['activecoins'] = self.parser_profile.findAll("b", {"class": "active-coins"})[0].string
			user_data['playedcoins'] = self.parser_profile.findAll("b", {"class": "played"})[0].string
			user_data['level'] = self.parser_profile.findAll("span", {"class": "avatar_sat"})[0].string
			user_data['levelbar'] = self.parser_profile.findAll("div", {"class": "bar-inside"})[0]["style"].split(" ")[1].replace("%", "")
			# user_data['playedtotal'] = self.parser_profile.findAll("b", {"class": "user-stats__number"})[0].string

			self.signalUserData.emit(user_data)
		except mechanize.URLError, e:
			self.userData()

	def autoBet(self):
		# Obtener numero de coins
		coins = promo[0].b.string.split(" ")[0].replace(".", "")

		# Numero de apuestas
		bet_num = int(coins) // 200

		# Bucle de paginas
		page_num = 1
		while page_num < 7 and bet_num > 0:
			# Bucle de eventos
			link_url = ""
			links = []
			for link in self.mbrowser.links(text_regex="Juega"):
				links.append(link)
			i = 0
			errors = 0
			while i < len(links) and bet_num > 0:
				link = links[i]
				# Para que no se repitan obtener solo los eventos que no se han jugado
				if link.attrs[1][1] == "btn--action" and link_url != link.url and link.text != "Juega otra vez":
					link_url = link.url
					self.mbrowser.follow_link(link)
					parser_eventpage = BeautifulSoup(self.mbrowser.response().read())
					# Buscar el porcentaje
					options = parser_eventpage.findAll("label", {"data-match": "match-bet"})
					# Si la página está caida
					if len(options) < 1:
						errors += 1
					else:
						i += 1
						# Bucle de obtención del menor
						min = 100.0
						min_option = ""
						for option in options:
							value = float(option.string)
							if value < min:
								min = value
								min_option = option['for']
						# Rellenar formulario de apuesta
						self.mbrowser.select_form(nr=2)
						self.mbrowser.form["option_id"] = [min_option.split("_")[-1]]
						self.mbrowser.form["points"] = "200"
						bet_done = self.mbrowser.submit()
						parser_eventpage = BeautifulSoup(bet_done.read())
						advice = parser_eventpage.findAll("div", {"id": "flash"})
						# print str(advice[0]).split("\">")[1].split("</")[0]
						self.mbrowser.follow_link(text_regex="Jugar")
						# Se disminuye el contador de apuestas
						bet_num -= 1
					if errors == 5:
						i += 1
				else:
					i += 1
			# Siguiente página
			page_num += 1
			self.mbrowser.follow_link(url_regex="/eventos\?page=" + str(page_num))
