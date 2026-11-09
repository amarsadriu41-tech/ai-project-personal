

from pathlib import Path
import os
import platform

import numpy as np
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model
from gtts import gTTS


# SETTINGS

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "model"

MODEL_PATH = MODEL_DIR / "keras_model.h5"
LABELS_PATH = MODEL_DIR / "labels.txt"

IMAGE_SIZE = (224, 224)


# LOAD LABELS

def load_labels():
    labels = []

    with open(LABELS_PATH, "r", encoding="utf-8") as file:
        for line in file:
            label = line.strip()

            if not label:
                continue

            parts = label.split(" ", 1)

            if len(parts) == 2 and parts[0].isdigit():
                labels.append(parts[1])
            else:
                labels.append(label)

    return labels


# LOAD MODEL

model = load_model(
    MODEL_PATH,
    compile=False
)

class_names = load_labels()


# PREPARE IMAGE

def prepare_image(image_path):

    data = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    image = Image.open(image_path).convert("RGB")

    image = ImageOps.fit(
        image,
        IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )

    image_array = np.asarray(image)

    normalized_image_array = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    data[0] = normalized_image_array

    return data


# ANIMAL PREDICTION

def predict_animal(image_path):

    data = prepare_image(image_path)

    prediction = model.predict(
        data,
        verbose=0
    )

    index = int(np.argmax(prediction[0]))

    animal_class = class_names[index]

    confidence = float(prediction[0][index])

    return {
        "animal_class": animal_class,
        "confidence": confidence
    }


# TEXT TO SPEECH

def text_to_speech(text, language="en"):

    try:
        tts = gTTS(
            text=text,
            lang=language
        )

        filename = BASE_DIR / "animal_voice.mp3"

        tts.save(str(filename))

        print("\nAudio created successfully!")

        # PLAY AUDIO

        if platform.system() == "Windows":
            os.startfile(filename)

        elif platform.system() == "Darwin":
            os.system(f'open "{filename}"')

        else:
            os.system(f'xdg-open "{filename}"')

    except Exception as e:
        print("Text-to-Speech Error:", e)


# MAIN PROGRAM

def main():

    print("================================")
    print("   ANIMAL DETECTION SYSTEM")
    print("================================")

    image_path = input(
        "\nEnter image path: "
    ).strip().strip('"')

    if not os.path.isfile(image_path):
        print("Image file not found!")
        return

    # PREDICTION

    result = predict_animal(image_path)

    animal = result["animal_class"]

    confidence = result["confidence"] * 100

    print("\n================================")
    print("        PREDICTION RESULT")
    print("================================")

    print("Animal:", animal)

    print(f"Confidence: {confidence:.2f}%")

    # TEXT TO SPEECH

    print("\nConverting prediction to speech...")

    language = input(
        "Enter speech language (default en): "
    ).strip() or "en"

    speech_text = (
        f"The detected animal is {animal}. "
        f"The confidence is {confidence:.2f} percent."
    )

    text_to_speech(
        speech_text,
        language
    )


if __name__ == "__main__":
    main()
