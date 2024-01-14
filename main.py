import tkinter
from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
import random

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

configFile = '.ini'
config = ConfigParser()
config.read(configFile)
apiKey = config['apiKey']['key']

# creating the game window for when user selects unit type
def gameWindow(tempUnit):
    gwin = tkinter.Toplevel()
    fileName = 'list.txt'
    file = open(fileName, 'r')
    citiesList = file.read().splitlines()
    cityRandom = citiesList[random.randint(0, (len(citiesList) - 1))]

    # collecting the weather data from the API
    def getWeather(city):
        result = requests.get(url.format(city, apiKey))
        if result:
            json = result.json()
            city = json['name']
            country = json['sys']['country']
            tempKelvin = json['main']['temp']
            tempCelcius = tempKelvin - 273.15
            tempFaren = (tempKelvin - 273.15) * 9 / 5 + 32
            icon = json['weather'][0]['icon']
            weather = json['weather'][0]['main']
            properties = (city, country, round(tempCelcius), round(tempFaren), icon, weather)
            return properties
        else:
            return None

    # Weather Properties to give image to user before answer
    weatherTuple = getWeather(cityRandom)

    # Handling after user answers
    def userAnswer():
        tempInput = userInput.get()

        # Checking which unit user wants to use
        if tempUnit == 'celsius':
            correctTemp = str(weatherTuple[2])
        else:
            correctTemp = str(weatherTuple[3])

        # This will only show after user enters their answer, bc userAnswer() needs to run
        temp['text'] = f'{weatherTuple[2]}°C, {weatherTuple[3]}°F'
        weather['text'] = weatherTuple[5]

        if tempInput == correctTemp:
            result = messagebox.askquestion(title="Question", message="Correct, do you want to keep playing?")
            if result == 'yes':
                # After 2500ms destroy the answer window
                gwin.after(2500, gwin.destroy)
            else:
                gwin.destroy()
                app.destroy()
        else:
            result = messagebox.askquestion(title="Question", message="Incorrect, do you want to keep playing?")
            if result == 'yes':
                # After 2500ms destroy the answer window
                gwin.after(2500, gwin.destroy)
            else:
                gwin.destroy()
                app.destroy()

    userInput = StringVar()
    userCity = Entry(gwin, textvariable=userInput)
    userCity.pack()
    cityLocation = Label(gwin, text=f"What is the current temperature in {cityRandom}", font=('bold', 20))
    cityLocation.pack()
    image = Label(gwin, bitmap=f'images/{weatherTuple[4]}.png')
    image.pack()
    temp = Label(gwin, text="")
    temp.pack()
    weather = Label(gwin, text="")
    weather.pack()
    searchBtn = Button(gwin, text="Submit", width=12, command=userAnswer)
    searchBtn.pack()


app = Tk()
app.title("WeatherGuessr")
app.geometry("700x350")

# Main Menu window
celsiusBtn = Button(app, text="Play game in Celsius", command=lambda: gameWindow('celsius'))
celsiusBtn.pack()
farenBtn = Button(app, text="Play game in Fahrenheit", command=lambda: gameWindow('fahrenheit'))
farenBtn.pack()

app.mainloop()
