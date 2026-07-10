import streamlit as st
import torch
import timm
import torch.nn as nn

from torchvision import transforms
from PIL import Image

# =========================
# Device
# =========================
device = torch.device("cpu")

# =========================
# Classes
# =========================
classes = ['Fire', 'Non_Fire']

# =========================
# Load Model
# =========================
model = timm.create_model(
    'vit_tiny_patch16_224',
    pretrained=False
)

model.head = nn.Linear(
    model.head.in_features,
    len(classes)
)

model.load_state_dict(
    torch.load(
        "vit_forest_fire.pth",
        map_location=device
    )
)

model = model.to(device)

model.eval()

# =========================
# Transform
# =========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# =========================
# Streamlit UI
# =========================
st.title("🔥 Forest Fire Detection")

st.write("Upload an image to detect fire.")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

# =========================
# Prediction
# =========================
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    # Transform
    input_tensor = transform(image)

    input_tensor = input_tensor.unsqueeze(0)

    input_tensor = input_tensor.to(device)

    # Predict
    with torch.no_grad():

        outputs = model(input_tensor)

        probabilities = torch.softmax(outputs, dim=1)

        confidence, predicted = torch.max(probabilities, 1)

    predicted_class = classes[predicted.item()]

    confidence_score = confidence.item() * 100

    # =========================
    # Output
    # =========================
    st.subheader("Prediction")

    if predicted_class == "Fire":

        st.error(
            f"🔥 Fire Detected ({confidence_score:.2f}% confidence)"
        )

    else:

        st.success(
            f"✅ No Fire Detected ({confidence_score:.2f}% confidence)"
        )