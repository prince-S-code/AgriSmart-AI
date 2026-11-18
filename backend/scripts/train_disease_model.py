import json
import random
from pathlib import Path

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

SEED = 42
IMAGE_SIZE = 224
BATCH_SIZE = 32
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "trained_models" / "disease"

random.seed(SEED)
np.random.seed(SEED)
tf.keras.utils.set_random_seed(SEED)


def preprocess(image, label):
    image = tf.image.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
    image = tf.keras.applications.mobilenet_v2.preprocess_input(tf.cast(image, tf.float32))
    return image, label


def augment(image, label):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, 0.12)
    image = tf.image.random_contrast(image, 0.88, 1.12)
    return image, label


def main():
    dataset, info = tfds.load("plant_village", split="train", as_supervised=True, with_info=True, shuffle_files=True)
    class_names = info.features["label"].names

    total = info.splits["train"].num_examples
    train_count = int(total * 0.70)
    val_count = int(total * 0.15)

    dataset = dataset.shuffle(total, seed=SEED, reshuffle_each_iteration=False)
    train_ds = dataset.take(train_count)
    val_ds = dataset.skip(train_count).take(val_count)
    test_ds = dataset.skip(train_count + val_count)

    train_ds = train_ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).map(augment, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    test_ds = test_ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), include_top=False, weights="imagenet"
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.30)(x)
    outputs = tf.keras.layers.Dense(len(class_names), activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    checkpoint = OUTPUT_DIR / "checkpoint.keras"
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(checkpoint, monitor="val_accuracy", save_best_only=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-7),
    ]

    history = model.fit(train_ds, validation_data=val_ds, epochs=12, callbacks=callbacks)

    fine_tune_at = max(len(base_model.layers) - 40, 0)
    base_model.trainable = True
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    history_fine = model.fit(train_ds, validation_data=val_ds, epochs=5, callbacks=callbacks)

    test_loss, test_accuracy = model.evaluate(test_ds, verbose=1)
    model.save(OUTPUT_DIR / "plant_disease_model.keras")

    metadata = {
        "model_name": "MobileNetV2 transfer learning",
        "dataset": "PlantVillage 1.0.2 via TensorFlow Datasets",
        "dataset_examples": total,
        "train_examples": train_count,
        "validation_examples": val_count,
        "test_examples": total - train_count - val_count,
        "image_size": [IMAGE_SIZE, IMAGE_SIZE],
        "class_count": len(class_names),
        "class_names": class_names,
        "test_accuracy": float(test_accuracy),
        "test_loss": float(test_loss),
        "head_epochs": len(history.history["accuracy"]),
        "fine_tune_epochs": len(history_fine.history["accuracy"]),
        "random_seed": SEED,
    }
    (OUTPUT_DIR / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
