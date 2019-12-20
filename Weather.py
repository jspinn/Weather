import requests
import bs4
import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.textinput import TextInput


class WeatherView(GridLayout):
    def get_time(self):
        now = datetime.datetime.now()
        time = now.strftime("%#I:%M:%S")
        return time

    def get_date(self):
        now = datetime.datetime.now()
        date = now.strftime("%D")
        return date

    def update_time(self, event):
        self.timeLabel.text = self.get_time()


    def set_weather_page(self, zip):
        page = 'https://weather.com/weather/today/l/{}:4:US'.format(zip)
        req = requests.get(page)
        req.raise_for_status()

        self.weatherPage = bs4.BeautifulSoup(req.text, "html.parser")

    def get_temp(self):
        temp = self.weatherPage.find('div', class_="today_nowcard-temp")
        return temp.text

    def get_phrase(self):
        phrase = self.weatherPage.find('div', class_="today_nowcard-phrase")
        return phrase.text

    def get_tonight(self):
        tonight = self.weatherPage.find('div', class_="today-daypart-temp")
        return tonight.text

    def get_tonight_phrase(self):
        phrase = self.weatherPage.find('span', class_="today-daypart-wxphrase")
        return phrase.text

    def today_callback(self, event):
        self.currentLabel.text = "Today"
        self.tempLabel.text = self.get_temp()
        self.phraseLabel.text = self.get_phrase()

    def tonight_callback(self, event):
        self.currentLabel.text = "Tonight"
        self.tempLabel.text = self.get_tonight()
        self.phraseLabel.text = self.get_tonight_phrase()



    def __init__(self, **kwargs):
        super(WeatherView, self).__init__(**kwargs)

        # Set weather page to parse
        self.set_weather_page('92630')

        # Initialize labels
        self.tempLabel.text = self.get_temp()
        self.phraseLabel.text = self.get_phrase()

        self.timeLabel.text = self.get_time()
        self.dateLabel.text = self.get_date()

        # Set time update intervals
        Clock.schedule_interval(self.update_time, 0.5)


        # Bind buttons
        self.tonightButton.bind(on_press=self.tonight_callback)
        self.todayButton.bind(on_press=self.today_callback)






class WeatherApp(App):

    def build(self):
        return WeatherView()



if __name__ == '__main__':
    WeatherApp().run()

