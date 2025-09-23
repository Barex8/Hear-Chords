import random
import tkinter
import tkinter.messagebox
from tkinter import ttk

import numpy as np
import sounddevice as sd

from note import Note


class RetentiveNotesTab(ttk.Frame):


    form = {
        "num_notes_min":1,
        "num_notes_max":1,
        "notes_played":[],
        "note_to_guess" : []

    }

    def __init__(self,master):
        super().__init__(master)

        ttk.Label(self,text="Número de notas:").grid(column=0,row=0)

        ttk.Label(self,text="mín:",width=10).grid(column=0,row=1)
        self.num_notes_min_input = ttk.Entry(self, width=3)
        self.num_notes_min_input.grid(column=1,row=1)
        self.num_notes_min_input.insert(0,"2")

        ttk.Label(self,text="máx:",width=10).grid(column=2,row=1)
        self.num_notes_max_input = ttk.Entry(self,width=3)
        self.num_notes_max_input.grid(column=3,row=1)
        self.num_notes_max_input.insert(0, "2")


        ttk.Label(self, text="Duración de cada nota:").grid(column=0, row=2)

        ttk.Label(self, text="mín:", width=10).grid(column=0, row=3)
        self.dur_notes_min_input = ttk.Entry(self, width=3)
        self.dur_notes_min_input.grid(column=1, row=3)
        self.dur_notes_min_input.insert(0, "1")

        ttk.Label(self, text="máx:", width=10).grid(column=2, row=3)
        self.dur_notes_max_input = ttk.Entry(self, width=3)
        self.dur_notes_max_input.grid(column=3, row=3)
        self.dur_notes_max_input.insert(0, "1")


        ttk.Label(self, text="Duración entre notas:").grid(column=0, row=4)

        ttk.Label(self, text="mín:", width=10).grid(column=0, row=5)
        self.dur_between_notes_min_input = ttk.Entry(self, width=3)
        self.dur_between_notes_min_input.grid(column=1, row=5)
        self.dur_between_notes_min_input.insert(0, "1")

        ttk.Label(self, text="máx:", width=10).grid(column=2, row=5)
        self.dur_between_notes_max_input = ttk.Entry(self, width=3)
        self.dur_between_notes_max_input.grid(column=3, row=5)
        self.dur_between_notes_max_input.insert(0, "1")


        ttk.Label(self, text="Octavas de las notas:").grid(column=0, row=6)

        ttk.Label(self, text="mín:", width=10).grid(column=0, row=7)
        self.octave_min_input = ttk.Entry(self, width=3)
        self.octave_min_input.grid(column=1, row=7)
        self.octave_min_input.insert(0, "2")

        ttk.Label(self, text="máx:", width=10).grid(column=2, row=7)
        self.octave_max_input = ttk.Entry(self, width=3)
        self.octave_max_input.grid(column=3, row=7)
        self.octave_max_input.insert(0, "4")

        checkboxes_frame = ttk.LabelFrame(self, text="Otros")
        checkboxes_frame.grid(column=0, row=8, columnspan=4, pady=10, sticky="ew")

        self.sharp_notes = tkinter.BooleanVar(value=True)
        self.check_sharp = tkinter.Checkbutton(checkboxes_frame,text="¿Sostenidos?",variable= self.sharp_notes)
        self.check_sharp.grid(column=0,row=0,pady=5,padx=5,sticky="ew")
        self.check_sharp.select()


        self.mind_octaves = tkinter.BooleanVar(value=True)
        self.check_mind_octaves= tkinter.Checkbutton(checkboxes_frame, text="¿Tener en cuenta octavas en la solución?", variable=self.mind_octaves)
        self.check_mind_octaves.grid(column=0, row=1, pady=5, padx=5)
        self.check_mind_octaves.select()

        ttk.Label(checkboxes_frame, text="¿Que nota quieres adivinar?").grid(column=0, row=2)
        self.note_to_guess_entry = ttk.Entry(checkboxes_frame,width=3)
        self.note_to_guess_entry.grid(column=1, row=2)
        self.note_to_guess_entry.insert(0, "1")


        ttk.Label(self, text="Solución:").grid(column=0, row=9)
        self.solution_entry = ttk.Entry(self, width=40)
        self.solution_entry.grid(column=0,row=10,columnspan=3)

        replay_bt = ttk.Button(self, text="REPLAY", command= lambda: self.play_sound(self.form))
        replay_bt.grid(column=1, row=12)

        play_bt = ttk.Button(self,text="PLAY",command=self.play_sound)
        play_bt.grid(column=2,row=12)

        check_bt = ttk.Button(self, text="CHECK", command= lambda: self.check_solution(self.form))
        check_bt.grid(column=3, row=10)

        check_bt = ttk.Button(self, text="SOLUCION", command=lambda: self.show_solution(self.form))
        check_bt.grid(column=0, row=12)


    def new_form(self):
        self.form["num_notes_min"] = int( self.num_notes_min_input.get())
        self.form["num_notes_max"] = int( self.num_notes_max_input.get())
        self.form["dur_notes_min"] = float( self.dur_notes_min_input.get())
        self.form["dur_notes_max"] = float( self.dur_notes_max_input.get())
        self.form["dur_between_notes_min"] = float (self.dur_between_notes_min_input.get())
        self.form["dur_between_notes_max"] = float (self.dur_between_notes_max_input.get())
        self.form["octave_min"] = int(self.octave_min_input.get())
        self.form["octave_max"] = int(self.octave_max_input.get())
        self.form["notes_played"] = []
        self.form["pos_note_to_guess"] = int(self.note_to_guess_entry.get())

        return self.form


    # === Funciones útiles ===
    notes = {
        "DO": 261.63,
        "DO#": 277.18,
        "RE": 293.66,
        "RE#": 311.13,
        "MI": 329.63,
        "FA": 349.23,
        "FA#": 369.99,
        "SOL": 392.00,
        "SOL#": 415.30,
        "LA": 440.00,
        "LA#": 466.16,
        "SI": 493.88
    }

#------ TEMA ACORDES ----------
    intervals = {
        "major": [0],
        "minor": [0, 3, 7],
        "7": [0, 4, 7, 10],
        "maj7": [0, 4, 7, 11],
        "m7": [0, 3, 7, 10],
        }


    def generate_wave(self,frequency, duration=2.0, fs=44100, volume=0.3):
        """Genera una onda sinusoidal de una frecuencia dada"""
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        return volume * np.sin(2 * np.pi * frequency * t)

    def chord(self,root_freq, type="major", duration=2.0):
        """Genera un acorde a partir de la frecuencia raíz"""
        waves = []
        for interval in self.intervals[type]:
            f = root_freq * (2 ** (interval / 12))  # sube interval semitonos
            waves.append(self.generate_wave(f, duration))
        return sum(waves)  # mezcla las notas del acorde

    def change_octave(self, note: str, octave: int) -> float:
        """
        Devuelve la frecuencia de una nota en una octava dada.
        La referencia es la octava 4 (las que definiste en 'notes').
        """
        base_freq = self.notes[note]
        shift = octave - 4  # diferencia de octavas
        return base_freq * (2 ** shift)

    def play_sound(self,form = None):

        if form is None:
            form = self.new_form()
            form["notes_played"] = []
            self.form["note_to_guess"] = []

        if not form["notes_played"]:
            for i in range(random.randint(form["num_notes_min"],form["num_notes_max"])):
                #Guardar cada nota en una lista para poder hacer replay
                random_note_duration = random.uniform(form["dur_notes_min"],form["dur_notes_max"])
                notes = {}
                if self.sharp_notes.get():
                    notes = self.notes
                else:
                    for n in self.notes:
                        if not "#" in n:
                            notes[n] = self.notes[n]



                random_note_name = random.choice(list(notes.keys()))
                random_octave = random.randint(form["octave_min"],form["octave_max"])
                print(f"Note: {random_note_name}{random_octave}")
                note_name = f"{random_note_name}{random_octave}"

                random_note_freq = self.change_octave(random_note_name,random_octave)
                wave = self.chord(random_note_freq, "major", duration=random_note_duration)
                sd.play(wave, 44100)
                if i == self.form["pos_note_to_guess"]-1:
                    self.form["note_to_guess"].append(Note(int(random_note_duration*1000),wave,random_octave,note_name))

                form["notes_played"].append(Note(int(random_note_duration*1000),wave,random_octave,note_name))
                sd.sleep(int(random_note_duration*1000))
                sd.sleep(int(random.uniform(form["dur_between_notes_min"],form["dur_between_notes_max"])*1000))
            print("-------------------------")
        else:
            for note in form["notes_played"]:
                sd.play(note.wave, 44100)
                sd.sleep(note.duration)
                sd.sleep(int(random.uniform(form["dur_between_notes_min"],form["dur_between_notes_max"])*1000))

        sd.wait()

    def check_solution(self,form):
        solution = ""
        for note in form["note_to_guess"]:
            if self.mind_octaves.get():
                solution += f"{str(note.name)},"
            else:

                solution += f"{str(note.name[:-1])},"
        solution = solution[:-1].upper() #Delete final , y all mayúsculas
        print(solution)
        print(self.solution_entry.get().upper())

        if solution == self.solution_entry.get().upper():
            print("Has acertado!!!")
            tkinter.messagebox.showinfo("Check", "Has acertado!! ✔")
        else:
            tkinter.messagebox.showinfo("Check", "No es correcto ❌")
            print("Vuelve a intentarlo")

    def show_solution(self,form):
        solution = ""
        for note in form["note_to_guess"]:
            solution += f"{str(note.name)},"
        solution = solution[:-1]
        tkinter.messagebox.showinfo("Solución", solution)
