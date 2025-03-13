import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk

def generate_qr():
    text = entry_text.get()
    if not text:
        messagebox.showerror("Error", "Ingrese un texto o enlace para generar el QR")
        return
    
    qr = qrcode.make(text)
    qr.save("generated_qr.png")
    
    img = Image.open("generated_qr.png")
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)
    qr_label.config(image=img)
    qr_label.image = img

def clear_qr():
    qr_label.config(image='')
    qr_label.image = None

def scan_qr():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    
    image = cv2.imread(file_path)
    qr_codes = decode(image)
    
    if qr_codes:
        decoded_text = qr_codes[0].data.decode("utf-8")
        messagebox.showinfo("QR Detectado", f"Contenido: {decoded_text}")
    else:
        messagebox.showerror("Error", "No se detectó un código QR en la imagen seleccionada.")

def scan_qr_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        qr_codes = decode(frame)
        for qr in qr_codes:
            text = qr.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("QR Detectado", f"Contenido: {text}")
            return
        
        cv2.imshow("Escanear QR", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty("Escanear QR", cv2.WND_PROP_VISIBLE) < 1:
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Configuración de la ventana
root = tk.Tk()
root.title("QR Scanner & Generator")
root.geometry("400x500")
root.configure(bg="#1E1E2E")

frame = tk.Frame(root, bg="#282A36", padx=20, pady=20)
frame.pack(pady=20)

tk.Label(frame, text="Ingrese texto o enlace:", bg="#282A36", fg="white").pack()
entry_text = tk.Entry(frame, width=30)
entry_text.pack(pady=5)

tk.Button(frame, text="Generar QR", command=generate_qr, bg="#FF5555", fg="white").pack(pady=5)
tk.Button(frame, text="Eliminar QR", command=clear_qr, bg="#6272A4", fg="white").pack(pady=5)
qr_label = tk.Label(frame, bg="#282A36")
qr_label.pack(pady=10)

tk.Button(frame, text="Escanear desde imagen", command=scan_qr, bg="#50FA7B", fg="black").pack(pady=5)
tk.Button(frame, text="Escanear desde cámara", command=scan_qr_camera, bg="#BD93F9", fg="black").pack(pady=5)

root.mainloop()
