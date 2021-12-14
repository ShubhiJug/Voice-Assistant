import speech_recognition as sr #it recognizes speech by inputting audio, speech APIs
import pyttsx3 #it converts text to speech, it supports three TTS engines sapi5 for windows
import datetime #this provides a number of functions to deal with dates, times and time intervals yyyy-mm-dd
import wikipedia #fetches data from wikipedia 
import webbrowser #provides high level interface which allows displaying web-based documents to users
import os, sys #os provides functions for interacting with the operating system
import time #operations regarding time
import subprocess #run new apps 
import wolframalpha #an api which can compute expert level answers 
import json #script file used to store and transfer data
import requests #makes http requests to a specified url
#from pygame import mixer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyjokes #imports one liner jokes 
import re #regular expressions, imports specifies strings
import smtplib #simple mail transfer protocol client session object used to send emails to any valid emaid id 
from bs4 import BeautifulSoup as soup #pulls data out of html and xml files
import urllib #used for opening urls

from urllib.request import urlopen



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')#engine instance
engine.setProperty('voice', 'voices[0].id')

def speak(text):
	engine.say(text)
	engine.runAndWait()

def wishMe():
	hour = datetime.datetime.now().hour

	if hour>=0 and hour<12:
		speak("Hello Shubhi,Good Morning!")
		print("Hello,Good Morning")
	elif hour>=12 and hour<18:
		speak("Hello,Good Afternoon!")
		print("Hello,Good Afternoon")
	else:
		speak("Hello,Good Evening!")
		print("Hello,Good Evening")

def sendEmail(to, content):
	server=smtplib.SMTP('smtp.gmail.com')
	server.ehlo()
	server.starttls()
	server.login('your gmail address', 'your password')
	server.sendmail('your gmail address', to, content)
	server.close()

	
		
def get_audio():
	r=sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold=1
		r.adjust_for_ambient_noise(source, duration=1)
		audio=r.listen(source)
		

		try:
			said=r.recognize_google(audio)
		except Exception as e:
			speak("Pardon me, please say that again")
			said=get_audio()
		return said
		

wishMe()

def note(text):
	date=datetime.datetime.now()
	file_name=str(date).replace(":","-")+"-note.txt"
	with open(file_name,"w") as f:
		f.write(text)

	
	subprocess.Popen(["notepad.exe", file_name])






if __name__=='__main__':
	while True:
				
		said=get_audio().lower()
		if said==0:
			continue

		s=re.search("[\w\s]+bye",said)	
		if s:
			speak("Voice assistant is shutting down, Good bye")
			print("Voice assistant is shutting down, Good bye")
			sys.exit()

		x=re.search("[\w\s]+wikipedia+[\w\s]", said)			
		if x:
			said=said.replace("wikipedia", "")
			results=wikipedia.summary(said, sentences=3)
			speak("According to wikipedia")
			speak(results)
			print(results)

		y=re.search("[\w\s]+youtube", said)
		if y:
			webbrowser.open_new_tab("https://www.youtube.com")
			speak("Youtube is open now")
			time.sleep(5)

		a=re.search("[\w\s]+google",said)	
		if a:
			webbrowser.open_new_tab("https://www.google.com")
			speak("Google chrome is open now")
			time.sleep(5)

		b=re.search("[\w\s]+mail", said)	
		if b:
			webbrowser.open_new_tab("gmail.com")
			speak("Google mail is open now")
			time.sleep(5)

		c=re.search("[\w\s]+weather", said)	
		if c:
			api_key="5a43ed73d8f6fe1d266426d4857df5a2"
			base_url="https://api.openweathermap.org/data/2.5/weather?"
			speak("What is the city name")
			city_name=get_audio()
			complete_url=base_url+"appid="+api_key+"&q="+city_name
			response = requests.get(complete_url)
			x=response.json()
			if x["cod"]!="404":
				y=x["main"]
				current_temp=y["temp"]
				current_hum=y["humidity"]
				z=x["weather"]
				weather_description=z[0]["description"]
				speak(f"Currently in {city_name}"+"Temperature in kelvin unit is"+
					str(current_temp)+ "humidity in percentage is"+
					str(current_hum)+ "and its"+
					str(weather_description))
				print(f"Currently in {city_name} "+" temperature in kelvin unit is "+
					str(current_temp)+ " humidity in percentage is "+
					str(current_hum)+ " and its "+
					str(weather_description))
			else:
				speak("city not found")

		d=re.search("[\w\s]+time", said)	
		if d:
			strTime=datetime.datetime.now().strftime("%H:%M:%S")
			speak(f"the time is {strTime}")
			print(f"the time is {strTime}")

		if 'who are you'in said or 'what is your name' in said:
			speak('I am Joey version 1 point O your personal assistant. How you doin')

		e=re.search("[\w\s]+news", said)	
		if e:
			try:
				news_url="https://news.google.com/news/rss"
				Client=urlopen(news_url)
				xml_page=Client.read()
				Client.close()
				soup_page=soup(xml_page,"xml")
				news_list=soup_page.findAll("item")
				for news in news_list[:5]:
					speak(news.title.text.encode('utf-8'))
					print(news.title.text.encode('utf-8'))
			except Exception as e:
				print(e)
					

			time.sleep(5)

		f=re.search("search", said)
		if f:
			said=said.replace("search", "")
			webbrowser.open_new_tab(said)
			time.sleep(5)

		g=re.search("[\w\s]+ask+[\w\s]", said)	
		if g:
			speak('what do you want to know')
			question=get_audio()
			app_id="XJ3U28-35PUG3PXGR"
			client=wolframalpha.Client('XJ3U28-35PUG3PXGR')
			res=client.query(question)
			answer=next(res.results).text
			speak(answer)
			print(answer)

		h=re.search("[\w\s]+play+[\w\s]+music",said)
		if h:
			music_dir='E:\\music'
			songs=os.listdir(music_dir)
			print(songs)
			random=os.startfile(os.path.join(music_dir, songs[1]))

		i=re.search("[\w\s]+joke",said)
		if i:
			speak(pyjokes.get_joke())

		j=re.search("[\w\s]+reminder",said)
		if j:
			speak('what shall i remind you about?')
			reminder=get_audio()
			speak('in how many minutes')
			local_time=get_audio(float())
			local_time=local_time*60
			time.sleep(local_time)

		k=re.search("[\w\s]+note", said)
		if k:
			speak('what would you like me to write down')
			note_text=get_audio().lower()
			note(note_text)
			speak('I have made a note of that')

		

		m=re.search("launch(.*)", said)
		if m:
			appname=m.group(1)
			app_name=appname+".exe"
			subprocess.Popen(["open", "-n", "/Applications"+app_name],stdout=subprocess.PIPE)

		
		




				

	








		'''
		elif 'send a mail' in said:
			try:
				speak('what should i say?')
				content=get_audio()
				speak('whom should i send')
				to=get_audio()
				sendEmail(to, content)
				speak('mail has been sent')
			except Exception as e:
				print(e)
				speak('I am not able to send this mail')
			'''	



			
		   

#elif 'take notes' in said:
		#	subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
		'''
		elif 'search youtube' in said:
			PATH = "C:\Program Files (x86)\chromedriver.exe"
			driver= webdriver.Chrome(PATH)

			driver.get("https://www.youtube.com/")
			search=driver.find_element_by_name("s")
			say=get_audio()
			search.send_keys(say)
			search.send_keys(Keys.RETURN)
		'''
		
					


			
			#notes=get_audio()


#send email
#play music from comp lib
#get directions
#set reminders


time.sleep(3)			











			

		
