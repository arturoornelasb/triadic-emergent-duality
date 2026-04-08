"""
LM + Triadic Projection Head.

Wraps a pre-trained causal LM from HuggingFace (GPT-2, GPT-Neo, etc.)
and adds a triadic projection head that maps hidden states to
n_bits-dimensional semantic space.

Architecture:
    Input tokens -> [Pre-trained LM] -> hidden states (hidden_size D)
                                               |
                                               +-> LM Head (next-token prediction)
                                               +-> Triadic Head (n_bits)

Supported backbones: any AutoModelForCausalLM (GPT-2, GPT-Neo, Llama, etc.)

Head modes:
    simple: Linear(hidden_size, n_bits) — blueprint default (1 layer)
    deep:   Linear→GELU→Dropout→Linear  — 2-layer MLP

Activation modes:
    tanh:  torch.tanh(x) — standard, but concentrates near 0
    ifsq:  2*sigmoid(1.6*x)-1 — distributes activations more uniformly

Usage:
    model = GPT2Triadic('gpt2-medium', n_bits=72, head_mode='deep', activation='ifsq')
    model = GPT2Triadic('EleutherAI/gpt-neo-125m', n_bits=72, head_mode='deep')
    outputs, triadic_proj = model(input_ids, attention_mask=mask, labels=labels)
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoConfig


# ######################################################################
#  MODEL
# ######################################################################

class GPT2Triadic(nn.Module):
    """Pre-trained LM with Triadic Projection Head."""

    def __init__(self, model_name='gpt2-medium', n_triadic_bits=65,
                 freeze_base=False, dropout=0.1,
                 head_mode='simple', activation='ifsq'):
        super().__init__()
        self.model_name = model_name
        self.n_triadic_bits = n_triadic_bits
        self.freeze_base = freeze_base
        self.head_mode = head_mode
        self.activation = activation

        # Load pre-trained LM (any AutoModelForCausalLM)
        self.gpt2 = AutoModelForCausalLM.from_pretrained(model_name)
        config = self.gpt2.config
        # hidden_size: GPT-2 uses n_embd, others use hidden_size
        hidden_size = getattr(config, 'n_embd', None) or config.hidden_size

        if freeze_base:
            for param in self.gpt2.parameters():
                param.requires_grad = False

        # Triadic Projection Head
        if head_mode == 'simple':
            # Blueprint: single linear layer (like triadic-microgpt)
            self.triadic_head = nn.Linear(hidden_size, n_triadic_bits, bias=False)
            nn.init.normal_(self.triadic_head.weight, mean=0.0, std=0.02)
        elif head_mode == 'deep':
            # 2-layer MLP with GELU
            self.triadic_head = nn.Sequential(
                nn.Linear(hidden_size, hidden_size // 2, bias=False),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_size // 2, n_triadic_bits, bias=False),
            )
            for m in self.triadic_head.modules():
                if isinstance(m, nn.Linear):
                    nn.init.normal_(m.weight, mean=0.0, std=0.02)
        else:
            raise ValueError(f"head_mode must be 'simple' or 'deep', got '{head_mode}'")

    def _activate(self, x):
        """Apply triadic activation function."""
        if self.activation == 'tanh':
            return torch.tanh(x)
        elif self.activation == 'ifsq':
            # iFSQ (Tencent, 2025): distributes activations more uniformly
            # than tanh, which concentrates near 0 causing dead bits
            return 2 * torch.sigmoid(1.6 * x) - 1
        else:
            raise ValueError(f"activation must be 'tanh' or 'ifsq', got '{self.activation}'")

    def forward(self, input_ids, attention_mask=None, labels=None):
        """
        Forward pass.

        Returns:
            outputs: GPT-2 outputs (with loss if labels provided)
            triadic: (B, T, n_bits) projections in [-1, 1]
        """
        outputs = self.gpt2(
            input_ids,
            attention_mask=attention_mask,
            labels=labels,
            output_hidden_states=True,
        )

        # Last hidden state
        hidden = outputs.hidden_states[-1]  # (B, T, hidden_size)

        # Triadic projection
        triadic = self._activate(self.triadic_head(hidden))  # (B, T, n_bits)

        return outputs, triadic

    def triadic_loss(self, triadic_proj, entropy_weight=1.0, input_ids=None,
                     align_weight=5.0, align_mode='infonce'):
        """
        Multi-objective triadic loss (from triadic-microgpt).

        1. Diversity: each bit fires ~50% of the time
        2. Contrastive: different sequences produce different projections
        3. Entropy: prevent dead bits
        4. Embedding alignment: triadic similarity matches embedding similarity
        """
        if triadic_proj.size(1) < 2:
            return torch.tensor(0.0, device=triadic_proj.device)

        B, T, n_bits = triadic_proj.shape

        # 1. Diversity
        bit_means = triadic_proj.mean(dim=(0, 1))
        diversity_loss = (bit_means ** 2).mean()

        # 2. Contrastive
        seq_proj = triadic_proj.mean(dim=1)
        if B > 1:
            seq_norm = F.normalize(seq_proj, dim=-1)
            sim_matrix = seq_norm @ seq_norm.T
            mask = ~torch.eye(B, device=sim_matrix.device, dtype=torch.bool)
            contrastive_loss = sim_matrix[mask].pow(2).mean()
        else:
            contrastive_loss = torch.tensor(0.0, device=triadic_proj.device)

        # 3. Entropy regularization
        entropy_loss = torch.tensor(0.0, device=triadic_proj.device)
        if entropy_weight > 0:
            probs = (bit_means + 1.0) / 2.0
            eps = 1e-7
            probs = probs.clamp(eps, 1.0 - eps)
            bit_ent = -(probs * torch.log2(probs) + (1 - probs) * torch.log2(1 - probs))
            entropy_loss = (1.0 - bit_ent).mean()

        # 4. Embedding alignment
        alignment_loss = torch.tensor(0.0, device=triadic_proj.device)
        if align_weight > 0 and input_ids is not None:
            with torch.no_grad():
                embeds = self._get_embeddings(input_ids).detach()

            if align_mode == 'mse':
                alignment_loss = self._align_mse(triadic_proj, embeds, B, T, n_bits)
            elif align_mode == 'infonce':
                alignment_loss = self._align_infonce(triadic_proj, embeds, B, T, n_bits)

        loss = diversity_loss + contrastive_loss
        if entropy_weight > 0:
            loss = loss + entropy_weight * entropy_loss
        if align_weight > 0:
            loss = loss + align_weight * alignment_loss
        return loss

    def _get_embeddings(self, input_ids):
        """Get token embeddings from the backbone (architecture-agnostic)."""
        # GPT-2: transformer.wte, GPT-Neo: transformer.wte, Llama: model.embed_tokens
        if hasattr(self.gpt2, 'transformer') and hasattr(self.gpt2.transformer, 'wte'):
            return self.gpt2.transformer.wte(input_ids)
        elif hasattr(self.gpt2, 'model') and hasattr(self.gpt2.model, 'embed_tokens'):
            return self.gpt2.model.embed_tokens(input_ids)
        else:
            # Fallback: run a forward pass and grab hidden states
            with torch.no_grad():
                out = self.gpt2(input_ids, output_hidden_states=True)
                return out.hidden_states[0]

    def _align_mse(self, triadic_proj, embeds, B, T, n_bits):
        """MSE alignment: match absolute similarity values."""
        n_pairs = 64
        idx = torch.randint(0, T, (B, n_pairs, 2), device=triadic_proj.device)
        idx_i, idx_j = idx[:, :, 0], idx[:, :, 1]

        idx_i_e = idx_i.unsqueeze(-1).expand(-1, -1, embeds.size(-1))
        idx_j_e = idx_j.unsqueeze(-1).expand(-1, -1, embeds.size(-1))
        e_i = torch.gather(embeds, 1, idx_i_e)
        e_j = torch.gather(embeds, 1, idx_j_e)
        embed_sim = F.cosine_similarity(e_i, e_j, dim=-1)

        idx_i_p = idx_i.unsqueeze(-1).expand(-1, -1, n_bits)
        idx_j_p = idx_j.unsqueeze(-1).expand(-1, -1, n_bits)
        p_i = torch.gather(triadic_proj, 1, idx_i_p)
        p_j = torch.gather(triadic_proj, 1, idx_j_p)
        triadic_sim = F.cosine_similarity(p_i, p_j, dim=-1)

        return F.mse_loss(triadic_sim, embed_sim)

    def _align_infonce(self, triadic_proj, embeds, B, T, n_bits, temperature=0.1):
        """InfoNCE contrastive alignment with embedding-mined positives."""
        n_anchors = 32

        anchor_idx = torch.randint(0, T, (B, n_anchors), device=triadic_proj.device)
        pool_idx = torch.randint(0, T, (B, n_anchors), device=triadic_proj.device)
        collisions = anchor_idx == pool_idx
        if collisions.any():
            pool_idx = pool_idx.clone()
            pool_idx[collisions] = (pool_idx[collisions] + 1) % T

        anchor_e = torch.gather(embeds, 1,
                                anchor_idx.unsqueeze(-1).expand(-1, -1, embeds.size(-1)))
        pool_e = torch.gather(embeds, 1,
                              pool_idx.unsqueeze(-1).expand(-1, -1, embeds.size(-1)))
        anchor_e_norm = F.normalize(anchor_e, dim=-1)
        pool_e_norm = F.normalize(pool_e, dim=-1)
        embed_sim_matrix = torch.bmm(anchor_e_norm, pool_e_norm.transpose(1, 2))
        pos_labels = embed_sim_matrix.argmax(dim=-1)

        anchor_p = torch.gather(triadic_proj, 1,
                                anchor_idx.unsqueeze(-1).expand(-1, -1, n_bits))
        pool_p = torch.gather(triadic_proj, 1,
                              pool_idx.unsqueeze(-1).expand(-1, -1, n_bits))
        anchor_p_norm = F.normalize(anchor_p.float(), dim=-1)
        pool_p_norm = F.normalize(pool_p.float(), dim=-1)
        triadic_sim_matrix = torch.bmm(anchor_p_norm, pool_p_norm.transpose(1, 2))

        logits = (triadic_sim_matrix / temperature).clamp(-50, 50)
        return F.cross_entropy(logits.reshape(-1, n_anchors), pos_labels.reshape(-1))

    @torch.no_grad()
    def generate(self, input_ids, attention_mask=None, max_new_tokens=100,
                 temperature=0.7, top_k=50):
        """Autoregressive text generation."""
        for _ in range(max_new_tokens):
            outputs = self.gpt2(input_ids, attention_mask=attention_mask)
            logits = outputs.logits[:, -1, :] / temperature
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = float('-inf')
            probs = F.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            input_ids = torch.cat([input_ids, next_id], dim=1)
            if attention_mask is not None:
                attention_mask = torch.cat([
                    attention_mask,
                    torch.ones((attention_mask.size(0), 1), device=attention_mask.device, dtype=attention_mask.dtype)
                ], dim=1)
        return input_ids

    def num_params(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def num_params_total(self):
        return sum(p.numel() for p in self.parameters())
