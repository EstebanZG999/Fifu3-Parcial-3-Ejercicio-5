import tkinter as tk
from tkinter import ttk
import math

class CalculadoraElectrica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Eléctrica")

        # Configurar estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))

        # Crear y configurar widgets
        self.crear_widgets()

    def crear_widgets(self):
        # Preguntar cuántos dispositivos desea ingresar
        ttk.Label(self.root, text="¿Cuántos dispositivos desea ingresar?").grid(row=0, column=0, padx=10, pady=10)
        self.num_dispositivos_var = tk.IntVar()
        self.num_dispositivos_entry = ttk.Entry(self.root, textvariable=self.num_dispositivos_var)
        self.num_dispositivos_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Aceptar", command=self.crear_campos_dispositivos).grid(row=0, column=2, padx=10, pady=10)

    def crear_campos_dispositivos(self):
        num_dispositivos = self.num_dispositivos_var.get()
        if num_dispositivos < 1 or num_dispositivos > 10:
            ttk.Label(self.root, text="Número inválido. Por favor ingrese un número entre 1 y 10.").grid(row=1, column=0, columnspan=6, padx=10, pady=10)
            return
        
        # Lista de electrodomésticos
        electrodomesticos = ["Refrigerador", "Televisor", "Lavadora", "Aire acondicionado", "Horno de microondas", "Computadora", "Licuadora", "Plancha", "Secadora de ropa", "Cafetera", "Lámpara", "Ventilador", "Cargador de teléfono", "Horno eléctrico", "Aspiradora", "Tostadora", "Batidora", "Calentador de agua", "Estufa eléctrica", "Impresora"]

        # Etiquetas para las columnas
        ttk.Label(self.root, text="Dispositivo").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.root, text="Potencia (W)").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Corriente (A)").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(self.root, text="Voltaje (V)").grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(self.root, text="Horas de uso").grid(row=1, column=4, padx=5, pady=5)
        ttk.Label(self.root, text="Largo del cable (m)").grid(row=1, column=5, padx=5, pady=5)

        self.dispositivos = []
        for i in range(num_dispositivos):
            dispositivo_var = tk.StringVar()
            dispositivo_combobox = ttk.Combobox(self.root, textvariable=dispositivo_var, values=electrodomesticos)
            dispositivo_combobox.grid(row=i+2, column=0, padx=10, pady=10)

            potencia_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=potencia_var, width=7).grid(row=i+2, column=1, padx=10, pady=10)

            corriente_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=corriente_var, width=7).grid(row=i+2, column=2, padx=10, pady=10)

            voltaje_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=voltaje_var, width=7).grid(row=i+2, column=3, padx=10, pady=10)

            horas_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=horas_var, width=7).grid(row=i+2, column=4, padx=10, pady=10)

            largo_cable_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=largo_cable_var, width=7).grid(row=i+2, column=5, padx=10, pady=10)

            self.dispositivos.append({
                "dispositivo_var": dispositivo_var,
                "potencia_var": potencia_var,
                "corriente_var": corriente_var,
                "voltaje_var": voltaje_var,
                "horas_var": horas_var,
                "largo_cable_var": largo_cable_var
            })

        # Botón para calcular
        ttk.Button(self.root, text="Calcular", command=self.calcular).grid(row=num_dispositivos+2, column=0, columnspan=6, pady=20)

        # Etiquetas para mostrar los resultados
        self.resultado_tipo_tarifa_label = ttk.Label(self.root, text="")
        self.resultado_tipo_tarifa_label.grid(row=num_dispositivos+3, column=0, columnspan=6, padx=10, pady=10)

        self.resultado_corriente_label = ttk.Label(self.root, text="")
        self.resultado_corriente_label.grid(row=num_dispositivos+4, column=0, columnspan=6, pady=10)

        self.resultado_energia_label = ttk.Label(self.root, text="")
        self.resultado_energia_label.grid(row=num_dispositivos+5, column=0, columnspan=6, pady=10)

        self.resultado_diametro_label = ttk.Label(self.root, text="")
        self.resultado_diametro_label.grid(row=num_dispositivos+6, column=0, columnspan=6, pady=10)

    def calcular(self):
        corriente_total = 0
        energia_total = 0
        largo_cable_total = 0

        for dispositivo in self.dispositivos:
            dispositivo_seleccionado = dispositivo["dispositivo_var"].get()
            if dispositivo_seleccionado:
                potencia = dispositivo["potencia_var"].get()
                corriente = dispositivo["corriente_var"].get()
                voltaje = dispositivo["voltaje_var"].get()
                horas = dispositivo["horas_var"].get()
                largo_cable = dispositivo["largo_cable_var"].get()

                corriente_calculada = potencia / voltaje
                energia = potencia * horas  # kWh

                corriente_total += corriente_calculada
                energia_total += energia
                largo_cable_total += largo_cable

        costo_energia = energia_total * 1.386  # Costo de 1.386 Q por kWh

        # Calcular diámetro mínimo del cable (usando la fórmula de la caída de voltaje)
        resistividad_cobre = 1.68e-8  # ohm*m
        caida_voltaje_max = 0.05 * voltaje  # 5% de caída de voltaje máximo
        area_minima = (2 * resistividad_cobre * largo_cable_total * corriente_total) / caida_voltaje_max
        diametro_minimo = 2 * (area_minima / math.pi)**0.5

        # Mostrar resultados
        self.resultado_corriente_label.config(text=f"Corriente Total: {corriente_total:.2f} A")
        self.resultado_energia_label.config(text=f"Costo de Energía: Q{costo_energia:.2f}")
        self.resultado_diametro_label.config(text=f"Diámetro Mínimo del Cable: {diametro_minimo:.2f} m")
        self.resultado_tipo_tarifa_label.config(text="Tipo de Tarifa: Baja Tension Simple Social - BTSS")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraElectrica(root)
    root.mainloop()