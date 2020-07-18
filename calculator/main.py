from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class Calculator(BoxLayout):
    value = "0"
    out = ObjectProperty(None)
    memory = 0

    def __init__(self, **kwargs):
        super(Calculator, self).__init__(**kwargs)

    def mem(self, item):
        if item == "M+":
            if "Error" in self.out.text:
                return
            self.memory += float(self.value)
        elif item == "M-":
            if "Error" in self.out.text:
                return
            self.memory -= float(self.value)
        elif item == "MRC":
            self.value = str(self.memory)
            if self.value[-2:] == ".0": self.value = self.value[:-2]
            self.out.text = self.value
    
    def check_value(self, item):
        if self.value == "0":
            if item not in (")", "^", "e"):
                return True
        else:
            if item == "(":
                if self.value[-1] in ("÷", "×", "−", "+", "√", "^", "("):
                    return True
            elif item == ")":
                if self.value[-1] not in ("÷", "×", "−", "+", ".", "√", "(", "^"):
                    return True
            elif item == "^":
                if self.value[-1] in list(map(str, list(range(10)))) + [")", "f"]:
                    return True
            elif item == "e":
                if self.value[-1] in list(map(str, list(range(10)))):
                    return True
            elif item == "√":
                if self.value[-1] in ("×", "−", "+", "÷", "^"):
                    return True
            elif item == "-":
                if self.value[-1] in ("×", "−", "+", "÷", "^", "e"):
                    return True
            elif item == "+":
                if self.value[-1] not in ("√", "(", "÷", "×", "−", "+", ".", "^"):
                    return True
            elif item == "7":
                if self.value[-1] != ")":
                    return True
            elif item == "8":
                if self.value[-1] != ")":
                    return True
            elif item == "9":
                if self.value[-1] != ")":
                    return True
            elif item == "−":
                if self.value[-1] not in ("√", "(", "÷", "×", "−", "+", ".", "^", "e"):
                    return True
            elif item == "4":
                if self.value[-1] != ")":
                    return True
            elif item == "5":
                if self.value[-1] != ")":
                    return True
            elif item == "6":
                if self.value[-1] != ")":
                    return True
            elif item == "×":
                if self.value[-1] not in ("√", "(", "÷", "×", "−", "+", ".", "^", "e"):
                    return True
            elif item == "1":
                if self.value[-1] != ")":
                    return True
            elif item == "2":
                if self.value[-1] != ")":
                    return True
            elif item == "3":
                if self.value[-1] != ")":
                    return True
            elif item == "÷":
                if self.value[-1] not in ("√", "(", "÷", "×", "−", "+", ".", "^", "e"):
                    return True
            elif item == "0":
                if self.value[-1] != ")":
                    return True
            elif item == ".":
                if self.value[-1] in list(map(str, list(range(10)))):
                    return True
        
        return False

    def change_value(self, item):
        if self.check_value(item):
            self.value = item if self.value == "0" and item not in ("×", "−", "+", ".") else self.value + item
            self.out.text = self.value
    
    def clear(self):
        self.value = "0"
        self.out.text = self.value
    
    def delete(self):
        if "Error" in self.value:
            self.value = "0"
            self.out.text = self.value
            return
        self.value = self.value[:-1]
        if not self.value:
            self.value = "0"
        self.out.text = self.value
    
    def parse(self):
        l = []
        string = ""
        for char in self.value:
            if char not in ("√", "(", "÷", "×", "−", "+" , ")", "^") or (len(string) and ((char == "+" or char == "-") and string[-1] == "e")):
                string += char
            else:
                if string != "":
                    l.append(string)
                    string = ""
                l.append(char)
        l.append(string)

        if l.count("(") != l.count(")"): self.value = "Bracket Syntax Error"; return None
        if "(" in l or ")" in l:
            if l.index("(") > l.index(")"): self.value = "Bracket Syntax Error"; return None
        
        if "(" in l:
            while "(" in l or ")" in l:
                close = l.index(")")
                open_ = max(idx for idx, val in enumerate(l[:close]) if val == "(")
                middle = l[open_ + 1:close]
                del l[open_ + 1:close + 1]
                l[open_] = middle
            return l
        else:
            return l
    
    def calc(self):
        steps = self.parse()
        if steps == None:
            self.out.text = self.value
            self.value = "0"
            return
        try: self.value = self.evaluate(steps)
        except OverflowError: self.value = "Overflow Error"
        except ZeroDivisionError: self.value = "Math Error"
        except (ValueError, IndexError) as e:
            print(e.args)
            self.value = "Syntax Error"
        self.out.text = self.value
        if "Error" in self.value: self.value = "0"
    
    def evaluate(self, l):
        steps = l.copy()
        if any(isinstance(x, list) for x in steps):
            for item in steps:
                if type(item) is list:
                    index = steps.index(item)
                    result = self.evaluate(item)
                    steps[index] = result
        
        l = steps
        del steps
        
        # Sqrt
        while "√" in l:
            index = l.index("√")
            l.pop(index)
            l[index] = str(float(l[index]) ** (1/2))
        
        # Indices
        while "^" in l:
            index = l.index("^")
            l.pop(index)
            l[index - 1] = str(float(l[index - 1]) ** float(l.pop(index)))
        
        # Minus
        while "-" in l:
            index = l.index("-")
            l.pop(index)
            l[index] = str(float(l[index]) * -1)
        
        # Mult and Div
        while "÷" in l or "×" in l:
            which, index = self.getfromlist(l, ("÷", "×"))
            if which == "÷":
                divident = l[index - 1]
                divisor = l[index + 1]
                l.pop(index - 1)
                l.pop(index)
                l[index - 1] = str(float(divident) / float(divisor))
            elif which == "×":
                mult1 = l[index - 1]
                mult2 = l[index + 1]
                l.pop(index - 1)
                l.pop(index)
                l[index - 1] = str(float(mult1) * float(mult2))
        
        # Add and Sub
        while "+" in l or "−" in l:
            which, index = self.getfromlist(l, ("+", "−"))
            if which == "+":
                x1 = l[index - 1]
                x2 = l[index + 1]
                l.pop(index - 1)
                l.pop(index)
                l[index - 1] = str(float(x1) + float(x2))
            elif which == "−":
                x1 = l[index - 1]
                x2 = l[index + 1]
                l.pop(index - 1)
                l.pop(index)
                l[index - 1] = str(float(x1) - float(x2))
        
        l = str(float(l[0]))
        if l[-2:] == ".0": l = l[:-2]
        return l
    
    def getfromlist(self, l, options):
        if options[0] not in l:
            return options[1], l.index(options[1])
        if options[1] not in l:
            return options[0], l.index(options[0])
        x1 = l.index(options[0])
        x2 = l.index(options[1])
        if x1 < x2:
            return options[0], x1
        return options[1], x2

class CalculatorApp(App):
    def build(self):
        self.value = "0"
        return Calculator()
    
    def on_pause(self):
        return True

if __name__ == "__main__":
    CalculatorApp().run()
