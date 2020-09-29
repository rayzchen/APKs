from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from config import *
from calculator import Calculator

for i in range(1, len(calcs) + 1):
    Builder.load_file("layout/calc" + str(i) + ".kv")

class Base(BoxLayout):
    def __init__(self, root):
        super(Base, self).__init__()
        self.root = root
        self.pages = list(reversed(self.children))
        first = True
        for child in self.pages:
            self.remove_widget(child)
        self.page = 0
        self.add_widget(self.pages[0])
        self.calculator = Calculator()
    
    def next_page(self):
        if self.page < len(self.pages) - 1:
            self.remove_widget(self.pages[self.page])
            self.page += 1
            self.add_widget(self.pages[self.page])
    
    def prev_page(self):
        if self.page > 0:
            self.remove_widget(self.pages[self.page])
            self.page -= 1
            self.add_widget(self.pages[self.page])
    
    def add_value(self, item):
        if item == "[i]e[/i]": item = "E"
        self.calculator.add_value(item)
        self.root.out.text = self.calculator.value.replace("E", "[i]e[/i]")
    
    def calc(self):
        if "Error" not in self.root.out.text:
            self.calculator.calc()
            self.root.out.text = self.calculator.value
            print(self.calculator.value)
            if "Error" in self.calculator.value:
                self.calculator.value = "0"
    
    def mem(self, memory):
        self.calculator.mem(memory)
        self.root.out.text = self.calculator.value
    
    def delete(self):
        self.calculator.delete()
        self.root.out.text = self.calculator.value
    
    def clear(self):
        self.calculator.clear()
        self.root.out.text = self.calculator.value

class Root(BoxLayout):
    label_text = ObjectProperty(None)
    out = ObjectProperty(None)
    unit = ObjectProperty(None)
    def __init__(self):
        super(Root, self).__init__()
        self.base = Base(self)
        self.add_widget(self.base)
        self.angle_unit = 1 # Degrees
    
    def prev(self):
        self.base.prev_page()
        self.label_text.text = calcs[self.base.page]
    
    def next(self):
        self.base.next_page()
        self.label_text.text = calcs[self.base.page]
    
    def switch(self):
        self.angle_unit = 1 - self.angle_unit
        self.base.calculator.angle_unit = self.angle_unit
        if self.angle_unit: self.unit.text = "DEG"
        else: self.unit.text = "RAD"

class CalculatorApp(App):
    def build(self):
        return Root()

CalculatorApp().run()
