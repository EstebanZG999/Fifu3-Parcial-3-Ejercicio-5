import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os   

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
            ttk.Label(self.root, text="Número inválido. Por favor ingrese un número entre 1 y 10.").grid(row=2, column=0, columnspan=6, padx=10, pady=10)
            return
        
        # Lista de electrodomésticos
        electrodomesticos = ["Refrigerador", "Televisor", "Lavadora", "Aire acondicionado", "Horno de microondas", "Computadora", "Licuadora", "Plancha", "Secadora de ropa", "Cafetera", "Lámpara", "Ventilador", "Cargador de teléfono", "Horno eléctrico", "Aspiradora", "Tostadora", "Batidora", "Calentador de agua", "Estufa eléctrica", "Impresora"]

        # Etiquetas para las columnas
        ttk.Label(self.root, text="Dispositivo").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(self.root, text="Potencia (W)").grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Corriente (A)").grid(row=2, column=2, padx=5, pady=5)
        ttk.Label(self.root, text="Voltaje (V)").grid(row=2, column=3, padx=5, pady=5)
        ttk.Label(self.root, text="Horas de uso al dia por mes").grid(row=2, column=4, padx=5, pady=5)

        self.dispositivos = []
        for i in range(num_dispositivos):
            dispositivo_var = tk.StringVar()
            dispositivo_combobox = ttk.Combobox(self.root, textvariable=dispositivo_var, values=electrodomesticos)
            dispositivo_combobox.grid(row=i+3, column=0, padx=10, pady=10)

            potencia_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=potencia_var, width=7).grid(row=i+3, column=1, padx=10, pady=10)

            corriente_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=corriente_var, width=7).grid(row=i+3, column=2, padx=10, pady=10)

            voltaje_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=voltaje_var, width=7).grid(row=i+3, column=3, padx=10, pady=10)

            horas_var = tk.DoubleVar()
            ttk.Entry(self.root, textvariable=horas_var, width=7).grid(row=i+3, column=4, padx=10, pady=10)

            self.dispositivos.append({
                "dispositivo_var": dispositivo_var,
                "potencia_var": potencia_var,
                "corriente_var": corriente_var,
                "voltaje_var": voltaje_var,
                "horas_var": horas_var
            })

        # Ingresar el largo del cable
        ttk.Label(self.root, text="Largo del cable (m)").grid(row=num_dispositivos+3, column=0, padx=10, pady=10)
        self.largo_cable_var = tk.DoubleVar()
        ttk.Entry(self.root, textvariable=self.largo_cable_var, width=7).grid(row=num_dispositivos+3, column=1, padx=10, pady=10)

        # Botón para calcular
        ttk.Button(self.root, text="Calcular", command=self.calcular).grid(row=num_dispositivos+4, column=0, columnspan=6, pady=20)

        # Etiquetas para mostrar los resultados
        self.resultado_tipo_tarifa_label = ttk.Label(self.root, text="")
        self.resultado_tipo_tarifa_label.grid(row=num_dispositivos+5, column=0, columnspan=6, padx=10, pady=10)

        self.resultado_corriente_label = ttk.Label(self.root, text="")
        self.resultado_corriente_label.grid(row=num_dispositivos+6, column=0, columnspan=6, pady=10)

        self.resultado_energia_label = ttk.Label(self.root, text="")
        self.resultado_energia_label.grid(row=num_dispositivos+7, column=0, columnspan=6, pady=10)

        self.resultado_diametro_label = ttk.Label(self.root, text="")
        self.resultado_diametro_label.grid(row=num_dispositivos+8, column=0, columnspan=6, pady=10)

    def calcular_calibre_cable(self, diametro_minimo):
        tabla = [
            {"calibre": 14, "diametro": 0.163, "imax": 18},
            {"calibre": 12, "diametro": 0.205, "imax": 25},
            {"calibre": 10, "diametro": 0.259, "imax": 30},
            {"calibre": 8,  "diametro": 0.326, "imax": 40},
            {"calibre": 6,  "diametro": 0.412, "imax": 60},
            {"calibre": 5,  "diametro": 0.462, "imax": 65},
            {"calibre": 4,  "diametro": 0.519, "imax": 85}
        ]

        for fila in tabla:
            if diametro_minimo <= fila["diametro"]:
                return fila["calibre"]
        
        return "Se necesita un calibre de cable más grande"

    def graficar(self):
        fig, ax = plt.subplots()

        # Dibujar la línea del cable
        largo_cable = self.largo_cable_var.get()
        ax.plot([0, largo_cable], [0, 0], 'k-', lw=2)

        # Dibujar los dispositivos
        y_offset = 0.5  # Ajusta este valor para cambiar la separación vertical de las imágenes
        line_length = 0.2  # Ajusta este valor para cambiar la longitud de las líneas que señalan las imágenes
        image_size = 0.5  # Ajusta este valor para cambiar el tamaño de las imágenes
        for i, dispositivo in enumerate(self.dispositivos, start=1):
            dispositivo_seleccionado = dispositivo["dispositivo_var"].get()
            if dispositivo_seleccionado:
                x = largo_cable * (i / (len(self.dispositivos) + 1))
                y_direction = (i % 2 * 2 - 1)  # Será 1 para dispositivos arriba, -1 para abajo
                y = y_offset * y_direction
                ax.plot([x, x], [0, y - line_length * y_direction], 'k-', lw=2)
                
                # Ruta a la imagen
                img_path = os.path.join('imagenes', f'{dispositivo_seleccionado}.png')
                
                # Verificar si la imagen existe
                if os.path.exists(img_path):
                    # Cargar y mostrar la imagen
                    img = mpimg.imread(img_path)
                    if y_direction == 1:
                        ax.imshow(img, extent=[x - image_size / 2, x + image_size / 2, y, y + image_size])
                    else:
                        ax.imshow(img, extent=[x - image_size / 2, x + image_size / 2, y - image_size, y])
                else:
                    print(f"Advertencia: No se encontró la imagen para el dispositivo {dispositivo_seleccionado}")

        ax.set_xlim(0, largo_cable)
        ax.set_ylim(-1, 1)
        ax.axis('off')
        plt.show()

    def calcular(self):
        corriente_total = 0 
        energia_total = 0
        potencia_total = 0
        largo_cable = self.largo_cable_var.get()
        
        dispositivo_max_potencia = None
        dispositivo_max_corriente = None
        max_potencia = 0
        max_corriente = 0

        for dispositivo in self.dispositivos:
            dispositivo_seleccionado = dispositivo["dispositivo_var"].get()
            if dispositivo_seleccionado:
                potencia = dispositivo["potencia_var"].get()
                corriente = dispositivo["corriente_var"].get()
                voltaje = dispositivo["voltaje_var"].get()
                horas = dispositivo["horas_var"].get()

                potencia_total += potencia

                if potencia > max_potencia:
                    max_potencia = potencia
                    dispositivo_max_potencia = dispositivo

                if corriente > max_corriente:
                    max_corriente = corriente
                    dispositivo_max_corriente = dispositivo


        if max_potencia > 0:
            dispositivo_max_corriente = max(self.dispositivos, key=lambda d: d["corriente_var"].get())
            if dispositivo_max_potencia != dispositivo_max_corriente:
                self.resultado_tipo_tarifa_label.config(text="Error: La potencia y corriente máximas deben pertenecer al mismo dispositivo.")
                return


        # Calcular diámetro mínimo del cable (usando la fórmula de la caída de voltaje)
        resistividad_cobre = 1.72e-8  # ohm*m
        diametro_minimo = (((max_corriente**2)*(resistividad_cobre)*(largo_cable))/(math.pi/4))**0.5

        energia = 565 * horas * 30
        energiaKw = energia/1000
        cobroEnergia = energiaKw * 1.386

        # Calcular el calibre del cable necesario
        calibre_cable = self.calcular_calibre_cable(diametro_minimo)

        # Mostrar resultados
        self.resultado_energia_label.config(text=f"Costo de Energía: Q{cobroEnergia:.2f}")
        self.resultado_diametro_label.config(text=f"Diámetro Mínimo del Cable: {diametro_minimo:.2f} m \nCalibre de Cable Necesario: {calibre_cable}")
        self.resultado_tipo_tarifa_label.config(text="Tipo de Tarifa: Baja Tension Simple Social - BTSS")


        # Mostrar la gráfica
        self.graficar()



if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraElectrica(root)
    root.mainloop()
