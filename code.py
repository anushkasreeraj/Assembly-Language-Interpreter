import tkinter as tk
from tkinter import messagebox, scrolledtext

# ------------------- Interpreter Core ------------------- #
class MiniAssemblyInterpreter:
    def __init__(self):
        self.registers = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0}
        self.halted = False
        self.pc = 0
        self.carry = 0
        self.output = []

    def parse_value(self, val):
        val = val.strip()
        if val in self.registers:
            return self.registers[val]
        try:
            return int(val)
        except ValueError:
            raise Exception(f"Invalid value or register: {val}")

    def execute_instruction(self, line):
        tokens = line.strip().split()
        if not tokens or self.halted:
            return

        instr = tokens[0].upper()

        if instr == "MOV":
            reg = tokens[1].rstrip(',')
            val = tokens[2]
            if reg not in self.registers:
                raise Exception(f"Invalid register: {reg}")
            self.registers[reg] = self.parse_value(val)

        elif instr == "ADD":
            reg = tokens[1].rstrip(',')
            val = tokens[2]
            if reg not in self.registers:
                raise Exception(f"Invalid register: {reg}")
            result = self.registers[reg] + self.parse_value(val)
            self.carry = 1 if result > 255 else 0  # Simulate 8-bit overflow
            self.registers[reg] = result

        elif instr == "SUB":
            reg = tokens[1].rstrip(',')
            val = tokens[2]
            if reg not in self.registers:
                raise Exception(f"Invalid register: {reg}")
            result = self.registers[reg] - self.parse_value(val)
            self.carry = 1 if result < 0 else 0
            self.registers[reg] = result

        elif instr == "MUL":
            reg = tokens[1].rstrip(',')
            val = tokens[2]
            if reg not in self.registers:
                raise Exception(f"Invalid register: {reg}")
            self.registers[reg] *= self.parse_value(val)

        elif instr == "DIV":
            reg = tokens[1].rstrip(',')
            val = tokens[2]
            if reg not in self.registers:
                raise Exception(f"Invalid register: {reg}")
            self.registers[reg] //= self.parse_value(val)

        elif instr == "PRN":
            reg = tokens[1]
            if reg not in self.registers:
                raise Exception(f"Invalid register: {reg}")
            self.output.append(f"{reg} = {self.registers[reg]}")

        elif instr == "JMP":
            addr = int(tokens[1])
            self.pc = addr - 1  # Adjust for auto-increment

        elif instr == "JC":
            addr = int(tokens[1])
            if self.carry == 1:
                self.pc = addr - 1

        elif instr == "HLT":
            self.halted = True
            self.output.append("Program halted.")

        else:
            raise Exception(f"Unknown instruction: {instr}")

    def execute_program(self, code):
        self.registers = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0}
        self.halted = False
        self.carry = 0
        self.output = []
        self.pc = 0
        lines = code.strip().split('\n')
        while self.pc < len(lines) and not self.halted:
            try:
                self.execute_instruction(lines[self.pc])
                self.pc += 1
            except Exception as e:
                raise Exception(f"Error on line {self.pc + 1}: {e}")
        return "\n".join(self.output)

# ------------------- Theme Management ------------------- #
def set_theme(theme):
    colors = {
        "light": {
            "bg": "#f0f0f0",
            "text_bg": "#ffffff",
            "text_fg": "#000000",
            "output_bg": "#e8f5e9",
            "output_fg": "green",
            "label_fg": "#000000",
            "button_bg": "#4CAF50",
            "button_fg": "#ffffff"
        },
        "dark": {
            "bg": "#2e2e2e",
            "text_bg": "#3c3f41",
            "text_fg": "#f8f8f2",
            "output_bg": "#1e1e1e",
            "output_fg": "#98c379",
            "label_fg": "#ffffff",
            "button_bg": "#5c6370",
            "button_fg": "#ffffff"
        },
        "blue": {
            "bg": "#dceefb",
            "text_bg": "#ffffff",
            "text_fg": "#003366",
            "output_bg": "#e1f5fe",
            "output_fg": "#0277bd",
            "label_fg": "#003366",
            "button_bg": "#0288d1",
            "button_fg": "#ffffff"
        }
    }

    c = colors[theme]

    window.configure(bg=c["bg"])
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=c["bg"], fg=c["label_fg"])
        elif isinstance(widget, tk.Button):
            if widget['text'] == "Exit":
                continue  # keep Exit red
            widget.configure(bg=c["button_bg"], fg=c["button_fg"])
        elif isinstance(widget, scrolledtext.ScrolledText):
            if widget == output_display:
                widget.configure(bg=c["output_bg"], fg=c["output_fg"])
            else:
                widget.configure(bg=c["text_bg"], fg=c["text_fg"])

theme_order = ["light", "dark", "blue"]
current_theme_index = 0
current_theme = theme_order[current_theme_index]

def toggle_theme():
    global current_theme_index, current_theme
    current_theme_index = (current_theme_index + 1) % len(theme_order)
    current_theme = theme_order[current_theme_index]
    set_theme(current_theme)

# ------------------- GUI Setup ------------------- #
def run_interpreter():
    code = code_input.get("1.0", tk.END)
    interpreter = MiniAssemblyInterpreter()
    try:
        output = interpreter.execute_program(code)
        output_display.config(state='normal')
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, output if output else "Execution complete (no output).")
        output_display.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

# Create main window
window = tk.Tk()
window.title("Mini Assembly Interpreter")
window.geometry("640x580")

# Widgets
label_code = tk.Label(window, text="Mini Assembly Language Interpreter:", font=("Arial", 10, "bold"))
label_code.pack(pady=5)

code_input = scrolledtext.ScrolledText(window, width=75, height=16)
code_input.pack(padx=10, pady=5)

 #Preload test code
code_input.insert(tk.END, """MOV R1, 250
ADD R1, 10
JC 7
PRN R1
MOV R2, 100
PRN R2
HLT
MOV R3, 1
PRN R3""")

btn_run = tk.Button(window, text="Run", command=run_interpreter, font=("Arial", 10, "bold"))
btn_run.pack(pady=10)

label_output = tk.Label(window, text="Output:", font=("Arial", 10, "bold"))
label_output.pack()

output_display = scrolledtext.ScrolledText(window, width=75, height=10, state='disabled')
output_display.pack(padx=10, pady=5)
# Frame to hold both buttons side-by-side
btn_frame = tk.Frame(window, bg=window["bg"])
btn_frame.pack(pady=10)

btn_theme = tk.Button(btn_frame, text="Change Theme", command=toggle_theme, font=("Arial", 10))
btn_theme.pack(side=tk.LEFT, padx=10)

btn_exit = tk.Button(btn_frame, text="Exit", command=window.destroy, font=("Arial", 10), bg="red", fg="white")
btn_exit.pack(side=tk.LEFT, padx=10)



# Apply initial theme
set_theme(current_theme)

# Run the GUI loop
window.mainloop()


