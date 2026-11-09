
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import platform

from PIL import Image, ImageTk
from gtts import gTTS

from classification import predict_animal


APP_TITLE = "Animal Classification App"
UPLOAD_BUTTON_TEXT = "Choose Animal Image"
EMPTY_IMAGE_TEXT = "Upload an animal image"
RESULT_EMPTY_TEXT = "Animal result will appear here"

PREVIEW_SIZE = (320, 240)

# COLORS

BG_COLOR = "#101827"
CARD_COLOR = "#1E293B"
PRIMARY_COLOR = "#7C3AED"
HOVER_COLOR = "#6D28D9"
CYAN_COLOR = "#22D3EE"
WHITE_COLOR = "#FFFFFF"
GRAY_COLOR = "#94A3B8"
GREEN_COLOR = "#34D399"


class AnimalApp:

    def __init__(self, root):

        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("520x680")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.preview_image = None

        # TITLE

        self.title_label = tk.Label(
            root,
            text="🐾 ANIMAL CLASSIFICATION",
            font=("Segoe UI", 19, "bold"),
            bg=BG_COLOR,
            fg=CYAN_COLOR
        )
        self.title_label.pack(pady=(22, 5))

        self.subtitle_label = tk.Label(
            root,
            text="AI Powered Animal Recognition System",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=GRAY_COLOR
        )
        self.subtitle_label.pack(pady=(0, 15))

        # IMAGE CARD

        self.image_frame = tk.Frame(
            root,
            bg=CARD_COLOR,
            padx=12,
            pady=12
        )
        self.image_frame.pack(pady=10)

        self.image_label = tk.Label(
            self.image_frame,
            text=EMPTY_IMAGE_TEXT,
            width=42,
            height=12,
            bg="#263449",
            fg=GRAY_COLOR,
            font=("Segoe UI", 12),
            relief="flat",
            borderwidth=0
        )
        self.image_label.pack()

        # UPLOAD BUTTON

        self.choose_button = tk.Button(
            root,
            text="📁  Choose Animal Image",
            command=self.choose_image,
            font=("Segoe UI", 11, "bold"),
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=WHITE_COLOR,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            bd=0
        )
        self.choose_button.pack(pady=12)

        # RESULT CARD

        self.result_frame = tk.Frame(
            root,
            bg=CARD_COLOR,
            padx=25,
            pady=15
        )
        self.result_frame.pack(pady=10, padx=30, fill="x")

        self.result_title = tk.Label(
            self.result_frame,
            text="PREDICTION RESULT",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_COLOR,
            fg=CYAN_COLOR
        )
        self.result_title.pack(pady=(0, 8))

        self.result_label = tk.Label(
            self.result_frame,
            text=RESULT_EMPTY_TEXT,
            font=("Segoe UI", 15, "bold"),
            bg=CARD_COLOR,
            fg=WHITE_COLOR
        )
        self.result_label.pack(pady=5)

        self.confidence_label = tk.Label(
            self.result_frame,
            text="Confidence: -",
            font=("Segoe UI", 12),
            bg=CARD_COLOR,
            fg=GREEN_COLOR
        )
        self.confidence_label.pack(pady=5)

        # LANGUAGE SELECTION

        self.language_label = tk.Label(
            root,
            text="Speech Language",
            font=("Segoe UI", 10, "bold"),
            bg=BG_COLOR,
            fg=WHITE_COLOR
        )
        self.language_label.pack(pady=(10, 4))

        self.language_entry = tk.Entry(
            root,
            font=("Segoe UI", 11),
            justify="center",
            bg=CARD_COLOR,
            fg=WHITE_COLOR,
            insertbackground=WHITE_COLOR,
            relief="flat",
            width=15
        )
        self.language_entry.insert(0, "en")
        self.language_entry.pack(ipady=7)

        # TEXT TO SPEECH BUTTON

        self.speech_button = tk.Button(
            root,
            text="🔊  Listen to Result",
            command=self.speak_result,
            font=("Segoe UI", 11, "bold"),
            bg=CYAN_COLOR,
            fg="#101827",
            activebackground="#06B6D4",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            state="disabled",
            bd=0
        )
        self.speech_button.pack(pady=15)

        # IMAGE PATH

        self.path_label = tk.Label(
            root,
            text="",
            font=("Segoe UI", 8),
            wraplength=460,
            bg=BG_COLOR,
            fg=GRAY_COLOR
        )
        self.path_label.pack(pady=5)

        # FOOTER

        self.footer_label = tk.Label(
            root,
            text="Powered by TensorFlow  |  Python  |  gTTS",
            font=("Segoe UI", 9),
            bg=BG_COLOR,
            fg=GRAY_COLOR
        )
        self.footer_label.pack(side="bottom", pady=12)

        self.current_result = None

    def choose_image(self):

        image_path = filedialog.askopenfilename(
            title="Choose Animal Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("All files", "*.*"),
            ],
        )

        if not image_path:
            return

        self.current_result = None
        self.speech_button.configure(state="disabled")

        self.show_preview(image_path)
        self.predict(image_path)

    def show_preview(self, image_path):

        try:
            image = Image.open(image_path).convert("RGB")
            image.thumbnail(PREVIEW_SIZE)

            self.preview_image = ImageTk.PhotoImage(image)

            self.image_label.configure(
                image=self.preview_image,
                text=""
            )

            self.path_label.configure(
                text=str(Path(image_path))
            )

        except Exception as error:

            messagebox.showerror(
                "Image Error",
                str(error)
            )

    def predict(self, image_path):

        try:
            result = predict_animal(image_path)

        except Exception as error:
            messagebox.showerror(
                "Prediction Error",
                str(error)
            )
            return

        self.current_result = result

        self.result_label.configure(
            text=f"Animal: {result['animal_class']}"
        )

        self.confidence_label.configure(
            text=f"Confidence: {result['confidence']:.2%}"
        )

        self.speech_button.configure(
            state="normal"
        )

    # TEXT TO SPEECH

    def speak_result(self):

        if not self.current_result:
            messagebox.showwarning(
                "Warning",
                "Please classify an animal first!"
            )
            return

        animal = self.current_result["animal_class"]

        confidence = self.current_result["confidence"] * 100

        language = self.language_entry.get().strip() or "en"

        speech_text = (
            f"The detected animal is {animal}. "
            f"The confidence is {confidence:.2f} percent."
        )

        try:

            tts = gTTS(
                text=speech_text,
                lang=language
            )

            audio_path = Path(__file__).resolve().parent / "animal_voice.mp3"

            tts.save(str(audio_path))

            if platform.system() == "Windows":
                os.startfile(str(audio_path))

            elif platform.system() == "Darwin":
                os.system(f'open "{audio_path}"')

            else:
                os.system(f'xdg-open "{audio_path}"')

        except Exception as error:

            messagebox.showerror(
                "Text-to-Speech Error",
                str(error)
            )


def main():

    root = tk.Tk()

    app = AnimalApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
