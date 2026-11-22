from pathlib import Path

import tensorflow as tf

BACKEND_DIR = Path(__file__).resolve().parents[1]
SOURCE_MODEL = BACKEND_DIR / "trained_models" / "disease" / "plant_disease_model.keras"
OUTPUT_MODEL = BACKEND_DIR / "trained_models" / "disease" / "plant_disease_model.tflite"


def main():
    if not SOURCE_MODEL.is_file():
        raise FileNotFoundError(f"Keras model not found: {SOURCE_MODEL}")

    model = tf.keras.models.load_model(SOURCE_MODEL, compile=False)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    OUTPUT_MODEL.write_bytes(converter.convert())
    print(f"Saved TFLite model to {OUTPUT_MODEL}")


if __name__ == "__main__":
    main()
