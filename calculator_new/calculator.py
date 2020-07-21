from config import *
from math import sqrt, e, pi, factorial

class Calculator:
    def __init__(self):
        self.value = "0"
    
    def check_value(self, item):
        if item in ["(", "√", "-", "1/", e, pi] and self.value == "0": return True
        if item == "e" and self.value == "0": return False
        if item == "(" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == ")" and self.value[-1] not in numbers + [")"]: return False
        elif item == "e" and self.value[-1] not in numbers: return False
        elif item == "^" and self.value[-1] not in numbers + [")"]: return False
        elif item == "√" and self.value[-1] not in ["+", "−", "×", "÷", "^"]: return False
        elif item == "+" and self.value[-1] not in numbers + ["e", ")"]: return False
        elif item == "−" and self.value[-1] not in numbers + [")"]: return False
        elif item == "×" and self.value[-1] not in numbers + [")"]: return False
        elif item == "÷" and self.value[-1] not in numbers + [")"]: return False
        elif item == "-" and self.value[-1] not in ["e", "(", "+", "−", "×", "÷", "^"]: return False
        elif item == "." and self.value[-1] not in numbers: return False
        elif item in numbers and self.value[-1] == ")": return False
        elif item == pi and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == e and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "^2" and self.value[-1] not in numbers + [")"]: return False
        elif item == "1/" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        elif item == "%" and self.value[-1] not in numbers + [")"]: return False
        elif item == "!" and self.value[-1] not in numbers + [")"]: return False
        elif item == "10^" and self.value[-1] not in ["+", "−", "×", "÷", "√", "^"]: return False
        return True
    
    def add_value(self, item):
        if self.check_value(item):
            if self.value == "0" and item not in ["+", "−", "×", ".", "^", "÷", "!"]: self.value = item
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
        l.append(string)

        if "(" in l:
            while "(" in l or ")" in l:
                close = l.index(")")
                open = max(idx for idx, val in enumerate(l[:close]) if val == "(")
                middle = l[open + 1:close]
                del l[open + 1:close + 1]
                l[open] = middle
        
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

    def eval(self, exp):
        operations = exp.copy()
        if any(type(item) is list for item in operations):
            for i in range(len(operations)):
                answer = self.eval(operations[i])
                if "Error" in answer:
                    return answer
                operations[i] = answer
        
        # Sqrt
        while "√" in operations:
            i = operations.index("√")
            del operations[i]
            operations[i] = str(sqrt(float(operations[i])))
        
        # Indices
        while "^" in operations:
            i = operations.index("^")
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
        
        if operations[0][-2:] == ".0": operations[0] = str(round(float(operations[0]), 10))[:-2]
        if operations[0] == "inf": return "Overflow Error"
        if operations[0] == "nan": return "Math Error"
        return operations[0]

    def clear(self):
        self.value = "0"
    
    def delete(self):
        if len(self.value) == 1:
            self.clear()
        else:
            self.value = self.value[:-1]
