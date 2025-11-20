import tkinter as tk
from tkinter import font

class Kalkulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Modern")
        self.root.geometry("340x520")
        self.root.minsize(320, 500)
        self.root.resizable(True, True)
        
        # Warna tema modern (Dark Mode)
        self.bg_color = "#1e1e1e"
        self.display_bg = "#2d2d2d"
        self.button_bg = "#3d3d3d"
        self.button_hover = "#4d4d4d"
        self.operator_bg = "#ff9500"
        self.operator_hover = "#ffaa22"
        self.equal_bg = "#4CAF50"
        self.equal_hover = "#66BB6A"
        self.text_color = "#ffffff"
        self.preview_color = "#888888"
        
        self.root.configure(bg=self.bg_color)
        
        # Variabel untuk menyimpan input dan hasil
        self.display = tk.StringVar()
        self.display.set("0")
        self.preview = tk.StringVar()
        self.preview.set("")
        
        # Font modern (diperkecil untuk layout compact)
        self.display_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.button_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.preview_font = font.Font(family="Segoe UI", size=11)
        
        # Frame untuk display dengan padding minimal
        display_frame = tk.Frame(root, bg=self.display_bg)
        display_frame.grid(row=0, column=0, columnspan=4, padx=8, pady=10, sticky="nsew", ipady=8)
        display_frame.grid_propagate(False)
        
        # Preview result (di atas)
        self.preview_label = tk.Label(
            display_frame, 
            textvariable=self.preview, 
            font=self.preview_font, 
            anchor="e", 
            justify="right", 
            fg=self.preview_color,
            bg=self.display_bg
        )
        self.preview_label.pack(fill="x", padx=10, pady=(5, 5))
        
        # Layar display utama
        self.entry = tk.Entry(
            display_frame, 
            textvariable=self.display, 
            font=self.display_font, 
            justify="right", 
            bd=0,
            bg=self.display_bg,
            fg=self.text_color,
            insertbackground=self.text_color
        )
        self.entry.pack(fill="both", expand=True, padx=3, pady=2)
        self.entry.bind("<Return>", lambda e: self.on_button_click("="))
        self.entry.bind("<BackSpace>", lambda e: self.on_key_backspace())
        self.entry.bind("<Escape>", lambda e: self.clear())
        
        # Frame untuk tombol
        buttons_frame = tk.Frame(root, bg=self.bg_color)
        buttons_frame.grid(row=1, column=0, columnspan=4, padx=8, pady=8, sticky="nsew")
        
        # Tombol-tombol dengan layout modern (5x4)
        buttons = [
            ('C', 0, 0, self.clear, self.button_bg),
            ('CE', 0, 1, self.on_key_backspace, self.button_bg),
            ('←', 0, 2, self.on_key_backspace, self.button_bg),
            ('/', 0, 3, lambda: self.on_button_click('/'), self.operator_bg),
            
            ('7', 1, 0, lambda: self.on_button_click('7'), self.button_bg),
            ('8', 1, 1, lambda: self.on_button_click('8'), self.button_bg),
            ('9', 1, 2, lambda: self.on_button_click('9'), self.button_bg),
            ('*', 1, 3, lambda: self.on_button_click('*'), self.operator_bg),
            
            ('4', 2, 0, lambda: self.on_button_click('4'), self.button_bg),
            ('5', 2, 1, lambda: self.on_button_click('5'), self.button_bg),
            ('6', 2, 2, lambda: self.on_button_click('6'), self.button_bg),
            ('-', 2, 3, lambda: self.on_button_click('-'), self.operator_bg),
            
            ('1', 3, 0, lambda: self.on_button_click('1'), self.button_bg),
            ('2', 3, 1, lambda: self.on_button_click('2'), self.button_bg),
            ('3', 3, 2, lambda: self.on_button_click('3'), self.button_bg),
            ('+', 3, 3, lambda: self.on_button_click('+'), self.operator_bg),
            
            ('0', 4, 0, lambda: self.on_button_click('0'), self.button_bg),
            ('.', 4, 1, lambda: self.on_button_click('.'), self.button_bg),
            ('=', 4, 2, lambda: self.on_button_click('='), self.equal_bg),
            ('√', 4, 3, self.sqrt_calc, self.operator_bg),
        ]
        
        for (text, row, col, command, bg_color) in buttons:
            self.create_button(buttons_frame, text, row, col, command, bg_color)
    
    def create_button(self, parent, text, row, col, command, bg_color):
        """Buat tombol dengan styling modern"""
        btn = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            command=command,
            bg=bg_color,
            fg=self.text_color,
            bd=0,
            relief="flat",
            activebackground=self.operator_hover if bg_color == self.operator_bg else (self.equal_hover if bg_color == self.equal_bg else self.button_hover),
            activeforeground=self.text_color,
            padx=15,
            pady=20,
            cursor="hand2"
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
    
    def on_button_click(self, char):
        current = self.display.get()
        if char == '=':
            try:
                result = eval(current)
                self.display.set(str(result))
                self.preview.set("")
            except:
                self.display.set("Error")
                self.preview.set("")
        else:
            # Masukkan karakter baru ke display
            if current == "0" or current == "Error":
                new = char
            else:
                new = current + char
            self.display.set(new)
            self.update_preview()
    
    def on_key_backspace(self):
        """Handle backspace key dan tombol CE"""
        current = self.display.get()
        if len(current) > 1:
            new = current[:-1]
            self.display.set(new)
            self.update_preview()
        else:
            self.display.set("0")
            self.preview.set("")
    
    def update_preview(self):
        """Update preview dengan hasil evaluasi"""
        current = self.display.get()
        try:
            # Jangan evaluasi ketika terakhir adalah operator atau titik
            if current and current[-1] in '+-*/.(':
                self.preview.set("")
            else:
                result = eval(current)
                self.preview.set(f"= {result}")
        except:
            self.preview.set("")
    
    def clear(self):
        """Clear semua input"""
        self.display.set("0")
        self.preview.set("")
    
    def sqrt_calc(self):
        """Hitung square root"""
        current = self.display.get()
        try:
            result = float(current) ** 0.5
            self.display.set(str(result))
            self.preview.set("")
        except:
            self.display.set("Error")
            self.preview.set("")

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    Kalkulator(root)
    root.mainloop()
