import os
import customtkinter as ctk
from tkinter import Canvas, messagebox, simpledialog
from PIL import Image, ImageTk
import pygame

# --- Init ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1000x600")
app.title("Fotorobot")

# --- Muusika ---
pygame.mixer.init()
pygame.mixer.music.load("dwarf.mp3")

def mängi_muusika():
    pygame.mixer.music.play(-1)

def peata_muusika():
    pygame.mixer.music.stop()

# --- Näo osad ja indeksid ---
kaustad = {
    "Frame": "FaceFrame",
    "Podb": "FacePodb",
    "Eye": "FaceEye",
    "Nose": "FaceNose",
    "Lips": "FaceLips"
}

indeksid = {osa: 0 for osa in kaustad}
maxid = {}

for osa, kaust in kaustad.items():
    failid = sorted([f for f in os.listdir(os.path.join("assets", kaust)) if f.endswith(".png")])
    maxid[osa] = len(failid)

pildid = {}
objektid = {}

# --- Canvas ---
canvas = Canvas(app, width=400, height=400, bg="white")
canvas.pack(side="right", padx=10, pady=10)

# --- Näita ---
def uuenda_osa(osa):
    if osa in objektid:
        canvas.delete(objektid[osa])
    kaust = kaustad[osa]
    indeks = indeksid[osa]
    failitee = os.path.join("assets", kaust, f"{indeks+1}.png")
    if os.path.exists(failitee):
        img = Image.open(failitee).convert("RGBA").resize((400, 400))
        tk_img = ImageTk.PhotoImage(img)
        pildid[osa] = tk_img
        objektid[osa] = canvas.create_image(200, 200, image=tk_img)

def uuenda_koik():
    for osa in kaustad:
        uuenda_osa(osa)

# --- Liigu edasi/tagasi ---
def muuda_osa(osa, suund):
    indeksid[osa] += suund
    if indeksid[osa] >= maxid[osa]:
        indeksid[osa] = 0
    elif indeksid[osa] < 0:
        indeksid[osa] = maxid[osa] - 1
    uuenda_osa(osa)

# --- Salvesta ---
def salvesta():
    failinimi = simpledialog.askstring("Salvesta", "Sisesta faili nimi:")
    if not failinimi:
        return
    lõpp = Image.new("RGBA", (400, 400), (255, 255, 255, 0))
    for osa in kaustad:
        kaust = kaustad[osa]
        indeks = indeksid[osa]
        failitee = os.path.join("assets", kaust, f"{indeks+1}.png")
        if os.path.exists(failitee):
            kiht = Image.open(failitee).convert("RGBA").resize((400, 400))
            lõpp = Image.alpha_composite(lõpp, kiht)
    lõpp.save(f"{failinimi}.png")
    messagebox.showinfo("Valmis", f"Salvestatud: {failinimi}.png")

# --- Vasak menüü ---
frame = ctk.CTkFrame(app)
frame.pack(side="left", padx=20, pady=20)

ctk.CTkLabel(frame, text="Fotorobot", font=("Segoe UI", 28)).pack(pady=10)

# --- Nupud iga osa jaoks ---
for osa in kaustad:
    osa_nimi = {
        "Frame": "Näo kuju",
        "Podb": "Lõug",
        "Eye": "Silmad",
        "Nose": "Nina",
        "Lips": "Suu"
    }[osa]
    
    rida = ctk.CTkFrame(frame, fg_color="transparent")
    rida.pack(pady=5)

    ctk.CTkLabel(rida, text=osa_nimi, width=80).pack(side="left")
    ctk.CTkButton(rida, text="<<", width=40, command=lambda o=osa: muuda_osa(o, -1)).pack(side="left", padx=2)
    ctk.CTkButton(rida, text=">>", width=40, command=lambda o=osa: muuda_osa(o, 1)).pack(side="left", padx=2)

# --- Muusika ja salvesta ---
muusika_frame = ctk.CTkFrame(frame, fg_color="transparent")
muusika_frame.pack(pady=15)

ctk.CTkButton(muusika_frame, text="▶ Mängi muusikat", command=mängi_muusika).pack(side="left", padx=5)
ctk.CTkButton(muusika_frame, text="⏹ Peata", command=peata_muusika).pack(side="left", padx=5)

ctk.CTkButton(frame, text="💾 Salvesta pilt", command=salvesta, fg_color="#1e88e5").pack(pady=10)

# --- Start ---
uuenda_koik()
app.mainloop()
