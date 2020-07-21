from config import *
from math import sqrt, e, pi, factorial, log, sin, cos, tan, radians

class Calculator:
    def __init__(self):
        self.value = "0"
        self.memory = "0"
        self.angle_unit = 1
    
    def mem(self, mode):
        if mode == "MC":
            self.memory = "0"
        elif mode == "M+":
            self.calc()
            self.memory = str(float(self.value) + float(self.memory))
        elif mode == "M-":
            self.calc()
            self.memory = str(float(self.value) - float(self.memory))
        elif mode == "MS":
            self.calc()
            self.memory = str(self.value)
        elif mode == "MRC":
            self.calc()
            self.value = self.memory
    
    def check_value(self, item):
        print(item, self.value[-1])
        if item in ["(", "√", "-", "1/", str(e), str(pi), "10^", "log(", "ln(", "abs(", "sin(", "cos(", "tan(", "sec(", "csc(", "cot("] and self.value == "0": return True
        if item == "e" and self.value == "0": return False
        if item == "(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^", "%", "("]: return False
        elif item == ")" and self.value[-1] not in numbers + [")"]: return False
        elif item == "e" and self.value[-1] not in numbers: return False
        elif item == "^" and self.value[-1] not in numbers + [")"]: return False
        elif item == "√" and self.value[-1] not in ["+", "−", "×", "÷", "^", "%", "("]: return False
        elif item == "+" and self.value[-1] not in numbers + ["e", ")"]: return False
        elif item == "−" and self.value[-1] not in numbers + [")"]: return False
        elif item == "×" and self.value[-1] not in numbers + [")"]: return False
        elif item == "÷" and self.value[-1] not in numbers + [")"]: return False
        elif item == "-" and self.value[-1] not in ["e", "(", "+", "−", "×", "÷", "^", "%"]: return False
        elif item == "." and self.value[-1] not in numbers: return False
        elif item in numbers and self.value[-1] == ")": return False
        elif item == str(pi) and self.value[-1] not in ["+", "−", "×", "÷", "√", "^", "%", "("]: return False
        elif item == str(e) and self.value[-1] not in ["+", "−", "×", "÷", "√", "^", "%", "("]: return False
        elif item == "^2" and self.value[-1] not in numbers + [")"]: return False
        elif item == "1/" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "%" and self.value[-1] not in numbers + [")"]: return False
        elif item == "!" and self.value[-1] not in numbers + [")"]: return False
        elif item == "10^" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "log(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "ln(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "abs(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "sin(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "cos(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "tan(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "sec(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "csc(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "cot(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        return True
    
    def add_value(self, item):
        if self.check_value(item):
            if self.value == "0" and item not in ["+", "−", "×", ".", "^", "÷", "!", "^", "%"]: self.value = item
            else: self.value += item
    
    def parse(self, exp):
        l = []
        string = ""
        for char in exp:
            if char not in ["√", "(", "÷", "×", "−", "+" , ")", "^", "%", "!"] or (len(string) and ((char == "+" or char == "-") and string[-1] == "e")):
                string += char
            else:
                if string != "":
                    l.append(string)
                    string = ""
                l.append(char)
        if string != "": l.append(string)

        if "(" in l:
            while "(" in l or ")" in l:
                close = l.index(")")
                open = max(idx for idx, val in enumerate(l[:close]) if val == "(")
                middle = l[open + 1:close]
                del l[open + 1:close + 1]
                l[open] = middle
        print(l)
        return l
    
    def calc(self):
        if self.value.count("(") != self.value.count(")") or ("(" in self.value and self.value.index("(") > self.value.index(")")):
            self.value = "Bracket Error"
            return
        
        operations = self.parse(self.value)
        try: self.value = self.eval(operations)
        except OverflowError: self.value = "Overflow Error"
        except ZeroDivisionError: self.value = "Zero Division Error"
        except ValueError: self.value = "Syntax Error"
        except Exception as e: raise e

    def eval(self, exp):
        operations = exp.copy()
        
        # Brackets
        if any(type(item) is list for item in operations):
            for i in range(len(operations)):
                if type(operations[i]) is list:
                    answer = self.eval(operations[i])
                    if "Error" in answer:
                        return answer
                    operations[i] = answer
        
        print(operations)
        
        # Functions
        while "log" in operations:
            i = operations.index("log")
            del operations[i]
            operations[i] = str(log(float(operations[i]), 10))
        
        while "ln" in operations:
            i = operations.index("ln")
            del operations[i]
            operations[i] = str(log(float(operations[i])))
        
        while "abs" in operations:
            i = operations.index("abs")
            del operations[i]
            operations[i] = str(abs(float(operations[i])))
        
        while "sin" in operations:
            i = operations.index("sin")
            del operations[i]
            if self.angle_unit: operations[i] = str(radians(float(operations[i])))
            operations[i] = str(sin(float(operations[i])))
            if float(operations[i]) < float("1e-10"): operations[i] = "0"
        
        while "cos" in operations:
            i = operations.index("cos")
            del operations[i]
            if self.angle_unit: operations[i] = str(radians(float(operations[i])))
            operations[i] = str(cos(float(operations[i])))
            if float(operations[i]) < float("1e-10"): operations[i] = "0"
        
        while "tan" in operations:
            i = operations.index("tan")
            del operations[i]
            if self.angle_unit: operations[i] = str(radians(float(operations[i])))
            operations[i] = str(tan(float(operations[i])))
            if float(operations[i]) < float("1e-10"): operations[i] = "0"
        
        while "sec" in operations:
            i = operations.index("sec")
            del operations[i]
            if self.angle_unit: operations[i] = str(radians(float(operations[i])))
            operations[i] = str(1 / cos(float(operations[i])))
            if float(operations[i]) < float("1e-10"): operations[i] = "0"
        
        while "csc" in operations:
            i = operations.index("csc")
            del operations[i]
            if self.angle_unit: operations[i] = str(radians(float(operations[i])))
            operations[i] = str(1 / sin(float(operations[i])))
            if float(operations[i]) < float("1e-10"): operations[i] = "0"
        
        while "cot" in operations:
            i = operations.index("cot")
            del operations[i]
            if self.angle_unit: operations[i] = str(radians(float(operations[i])))
            operations[i] = str(1 / tan(float(operations[i])))
            if float(operations[i]) < float("1e-10"): operations[i] = "0"
        
        # Sqrt
        while "√" in operations:
            i = operations.index("√")
            del operations[i]
            operations[i] = str(sqrt(float(operations[i])))
        
        # Indices
        while "^" in operations:
            i = max(idx for idx, val in enumerate(operations) if val == "^")
            if i == 0:
                return "Syntax Error"
            del operations[i]
            operations[i - 1] = str(float(operations[i - 1]) ** float(operations[i]))
            del operations[i]
            
        # Factorial
        while "!" in operations:
            i = operations.index("!")
            if i == 0:
                return "Syntax Error"
            del operations[i]
            operations[i - 1] = str(factorial(float(operations[i - 1])))
        
        # /*%
        while "×" in operations or "÷" in operations or "%" in operations:
            i = operations.index("×") if "×" in operations else len(operations)
            j = operations.index("÷") if "÷" in operations else len(operations)
            k = operations.index("%") if "%" in operations else len(operations)
            op = "×" if min([i, j, k]) == i else "÷" if min([i, j, k]) == j else "%"
            index = min([i, j, k])
            del operations[index]
            if op == "×": operations[index - 1] = str(float(operations[index - 1]) * float(operations[index]))
            elif op == "÷": operations[index - 1] = str(float(operations[index - 1]) / float(operations[index]))
            elif op == "%": operations[index - 1] = str(float(operations[index - 1]) % float(operations[index]))
            del operations[index]
        
        # +-
        while "+" in operations or "−" in operations:
            i = operations.index("+") if "+" in operations else len(operations)
            j = operations.index("−") if "−" in operations else len(operations)
            op = "+" if i < j else "−"
            index = i if i < j else j
            del operations[index]
            if op == "+": operations[index - 1] = str(float(operations[index - 1]) + float(operations[index]))
            else: operations[index - 1] = str(float(operations[index - 1]) - float(operations[index]))
            del operations[index]
        
        ending = ""
        if "e" in operations[0]:
            index = operations[0].index("e")
            ending = operations[0][index:]
            operations[0] = operations[0][:index]
        operations[0] += ending
        if operations[0] == "inf": return "Overflow Error"
        if operations[0] == "nan": return "Math Error"
        if int(float(operations[0])) == float(operations[0]): operations[0] = str(float(operations[0]))[:-2]
        return operations[0]

    def clear(self):
        self.value = "0"
    
    def delete(self):
        if len(self.value) == 1:
            self.clear()
        else:
            self.value = self.value[:-1]
