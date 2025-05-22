import os
import customtkinter as ctk
from tkinter import Canvas, messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import pygame

# --- Init ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1000x600")
app.title("Fotorobot")

# --- Muusika ---
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("dwarf1.mp3")

def mängi_muusika():
    pygame.mixer.music.play(-1)

def peata_muusika():
    pygame.mixer.music.stop()

# --- Näo osad ---
kaustad = {
    "Frame": "FaceFrame",
    "Eye": "FaceEye",
    "Nose": "FaceNose",
    "Lips": "FaceLips"
}

valikud = {}
valitud = {}
optionmenus = {}

for osa, kaust in kaustad.items():
    failid = sorted([f for f in os.listdir(os.path.join("assets", kaust)) if f.endswith(".png")])
    valikud[osa] = failid
    valitud[osa] = failid[0] if failid else None

pildid = {}
objektid = {}

# --- Canvas ---
canvas = Canvas(app, width=400, height=400, bg="white")
canvas.pack(side="right", padx=10, pady=10)

# --- Näita ---
def uuenda_osa(osa):
    if osa in objektid:
        canvas.delete(objektid[osa])
    failinimi = valitud[osa]
    if not failinimi:
        return
    failitee = os.path.join("assets", kaustad[osa], failinimi)
    if os.path.exists(failitee):
        img = Image.open(failitee).convert("RGBA").resize((400, 400))
        tk_img = ImageTk.PhotoImage(img)
        pildid[osa] = tk_img
        objektid[osa] = canvas.create_image(200, 200, image=tk_img)

def uuenda_koik():
    for osa in kaustad:
        uuenda_osa(osa)

# --- Salvesta ---
def salvesta():
    failinimi = simpledialog.askstring("Salvesta", "Sisesta faili nimi:")
    if not failinimi:
        return
    lõpp = Image.new("RGBA", (400, 400), (255, 255, 255, 0))
    for osa in kaustad:
        failinimi_osa = valitud[osa]
        if not failinimi_osa:
            continue
        failitee = os.path.join("assets", kaustad[osa], failinimi_osa)
        if os.path.exists(failitee):
            kiht = Image.open(failitee).convert("RGBA").resize((400, 400))
            lõpp = Image.alpha_composite(lõpp, kiht)
    lõpp.save(f"{failinimi}.png")
    messagebox.showinfo("Valmis", f"Salvestatud: {failinimi}.png")

# --- Lisa pilt ---
def lisa_pilt(osa):
    filepath = filedialog.askopenfilename(filetypes=[("PNG failid", "*.png")])
    if not filepath:
        return
    kaust = os.path.join("assets", kaustad[osa])
    failinimi = os.path.basename(filepath)
    uus_tee = os.path.join(kaust, failinimi)

    try:
        img = Image.open(filepath).convert("RGBA").resize((400, 400))
        img.save(uus_tee)
        valikud[osa].append(failinimi)
        valitud[osa] = failinimi
        uuenda_osa(osa)
        uuenda_valikud(osa, optionmenus[osa])
        messagebox.showinfo("Lisatud", f"Pilt lisatud: {failinimi}")
    except Exception as e:
        messagebox.showerror("Viga", str(e))

# --- Valikud menüü ---
def uuenda_valikud(osa, menu):
    failid = valikud[osa]
    menu.configure(values=failid)
    menu.set(valitud[osa])

def vali_osa(osa, nimi):
    if nimi in valikud[osa]:
        valitud[osa] = nimi
        uuenda_osa(osa)

# --- Vasak menüü ---
frame = ctk.CTkFrame(app)
frame.pack(side="left", padx=20, pady=20)

ctk.CTkLabel(frame, text="Fotorobot", font=("Segoe UI", 28)).pack(pady=10)

# --- Nupud iga osa jaoks ---
for osa in kaustad:
    osa_nimi = {
        "Frame": "Näo kuju",
        "Eye": "Silmad",
        "Nose": "Nina",
        "Lips": "Suu"
    }[osa]

    rida = ctk.CTkFrame(frame, fg_color="transparent")
    rida.pack(pady=5)

    ctk.CTkLabel(rida, text=osa_nimi, width=80).pack(side="left")
    menu = ctk.CTkOptionMenu(rida, width=150, command=lambda valik, o=osa: vali_osa(o, valik))
    menu.pack(side="left", padx=5)
    ctk.CTkButton(rida, text="Lisa", width=60, command=lambda o=osa: lisa_pilt(o)).pack(side="left", padx=5)

    optionmenus[osa] = menu
    uuenda_valikud(osa, menu)

# --- Muusika ja salvesta ---
muusika_frame = ctk.CTkFrame(frame, fg_color="transparent")
muusika_frame.pack(pady=15)

ctk.CTkButton(muusika_frame, text="▶ Mängi muusikat", command=mängi_muusika).pack(side="left", padx=5)
ctk.CTkButton(muusika_frame, text="⏹ Peata", command=peata_muusika).pack(side="left", padx=5)

ctk.CTkButton(frame, text="💾 Salvesta pilt", command=salvesta, fg_color="#1e88e5").pack(pady=10)

# --- Start ---
uuenda_koik()
app.mainloop()
