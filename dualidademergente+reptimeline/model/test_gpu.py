"""Quick GPU test for GPT-2 + Triadic Head."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch
from gpt2_triadic import GPT2Triadic

print('Loading GPT-2 MEDIUM + triadic head (65 bits)...')
model = GPT2Triadic('gpt2-medium', n_triadic_bits=65, freeze_base=False).to('cuda')

total = model.num_params_total()
trainable = model.num_params()
print(f'Total: {total:,}  Trainable: {trainable:,}')

x = torch.randint(0, 50257, (8, 256), device='cuda')
outputs, triadic = model(x, labels=x)
print(f'Lang loss: {outputs.loss.item():.4f}  Triadic: {triadic.shape}')

tri_loss = model.triadic_loss(triadic, entropy_weight=1.0, input_ids=x, align_weight=5.0)
print(f'Triadic loss: {tri_loss.item():.4f}')

alloc = torch.cuda.memory_allocated() / 1e9
reserved = torch.cuda.memory_reserved() / 1e9
print(f'VRAM: {alloc:.2f} GB allocated, {reserved:.2f} GB reserved')
print('OK - GPT-2 MEDIUM FITS')
