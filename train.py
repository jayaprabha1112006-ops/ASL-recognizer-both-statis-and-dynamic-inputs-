# === train.py: Pretrained CNN (MobileNetV2) to create sign_model.h5 ===

import os

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam


# Parameters
image_size = (224, 224)
batch_size = 32
epochs = 5

# Load and preprocess data
print("\n📁 Checking folders inside 'asl_dataset':")
print("✅ Folders found in asl_dataset:", os.listdir("asl_dataset"))

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    'asl_dataset/asl_dataset',  # FIXED: now points to actual A-Z folders
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    'asl_dataset/asl_dataset',
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# DEBUG: Check if data is loading
print("\n Checking training data:")
print("Number of classes:", train_generator.num_classes)
print("Training samples:", train_generator.samples)
print("Validation samples:", val_generator.samples)

# Load MobileNetV2 model (pretrained)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_tensor=Input(shape=(224, 224, 3)))

# Freeze base model layers
for layer in base_model.layers:
    layer.trainable = False

# Custom head for ASL classification
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
output = Dense(train_generator.num_classes, activation='softmax')(x)  # AUTO-ADJUST TO 29 CLASSES

model = Model(inputs=base_model.input, outputs=output)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
print("\n⏳ Training started...")
history = model.fit(train_generator, validation_data=val_generator, epochs=epochs)
print("✅ Training complete.")

# Save the model
try:
    model.save('sign_model.h5')
    print("✅ Model saved as 'sign_model.h5'")
except Exception as e:
    print("❌ Error saving model:", e)

# Final check: confirm model file exists
print("\n📂 Checking file existence:")
print("sign_model.h5 exists?", os.path.exists("sign_model.h5"))
