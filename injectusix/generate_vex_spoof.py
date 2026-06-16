# script by ChatGPT
# script for TryHackMe room Injectus IX Task 3 https://tryhackme.com/room/injectusix 
# YouTube video full walk through: https://youtu.be/NjyseAGg4fA
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
# pip install safetensors pillow
# pip install facenet-pytorch --no-deps

# generate_vex_spoof.py
import os

os.environ["ATEN_CPU_CAPABILITY"] = "default"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import torch
torch.backends.nnpack.enabled = False
torch.backends.mkldnn.enabled = False
torch.set_num_threads(1)

import torch.nn.functional as F
from PIL import Image
from safetensors.torch import load_file
from facenet_pytorch import InceptionResnetV1

device = "cuda" if torch.cuda.is_available() else "cpu"

TARGET_INDEX = 8   # change this after mapping templates

templates = load_file("face_recognition_v3.safetensors")["templates"].to(device)
templates = F.normalize(templates, dim=1)
target = templates[TARGET_INDEX:TARGET_INDEX+1]

model = InceptionResnetV1(pretrained="vggface2").eval().to(device)

# Start from random pixels in FaceNet input size: 160x160
x = torch.randn(1, 3, 160, 160, device=device, requires_grad=True)

optimizer = torch.optim.Adam([x], lr=0.03)

best_sim = -1
best_img = None

for step in range(3000):
    img = torch.tanh(x)

    emb = model(img)
    emb = F.normalize(emb, dim=1)

    sim = (emb @ target.T).squeeze()

    tv_h = (img[:, :, 1:, :] - img[:, :, :-1, :]).abs().mean()
    tv_w = (img[:, :, :, 1:] - img[:, :, :, :-1]).abs().mean()
    tv = tv_h + tv_w

    loss = -sim + 0.03 * tv

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if float(sim) > best_sim:
        best_sim = float(sim)
        best_img = img.detach().clone()

    if step % 100 == 0:
        print(step, "similarity:", float(sim), "loss:", float(loss))

    # Early stop once similarity is safely above threshold
    if float(sim) > 0.995:
        print("Early stop at step", step, "similarity:", float(sim))
        break
with torch.no_grad():
    final = best_img[0]
    final = (final + 1) / 2
    final = final.clamp(0, 1)
    final = (final.permute(1, 2, 0).cpu().numpy() * 255).astype("uint8")

Image.fromarray(final).save("vex_generated.png")
print("Saved vex_generated.png with best similarity:", best_sim)
