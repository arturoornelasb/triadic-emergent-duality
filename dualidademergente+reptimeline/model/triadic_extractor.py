"""
TriadicExtractor for GPT-2 + Triadic Head checkpoints.

Implements reptimeline.RepresentationExtractor for our 65-bit model.
Loads step_*.pt checkpoints, runs forward pass on concepts, extracts
binary codes from the triadic projection head.

Usage:
    from triadic_extractor import TriadicExtractor
    from reptimeline import TimelineTracker

    extractor = TriadicExtractor()
    snapshots = extractor.extract_sequence('checkpoints/gpt2_triadic_65/', concepts)
    tracker = TimelineTracker(extractor)
    timeline = tracker.analyze(snapshots)
    timeline.print_summary()
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import re
import math

import numpy as np
import torch

from reptimeline.core import ConceptSnapshot
from reptimeline.extractors.base import RepresentationExtractor

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from gpt2_triadic import GPT2Triadic
from triadic import PrimeMapper


class TriadicExtractor(RepresentationExtractor):
    """Extracts 65-bit triadic codes from GPT-2 + Triadic Head checkpoints.

    Uses GPT2Tokenizer from transformers. Caches the model across
    extract() calls when the model_name hasn't changed.
    """

    def __init__(self, checkpoints_dir=None, n_bits=65, max_tokens=8):
        # checkpoints_dir accepted for API compat with probes (stored but
        # not required — extract_sequence discovers checkpoints itself)
        self.checkpoints_dir = checkpoints_dir
        self.n_bits = n_bits
        self.max_tokens = max_tokens
        self._model = None
        self._tokenizer = None
        self._device = None
        self._mapper = PrimeMapper(n_bits)

    def _load_model(self, checkpoint_path, device='cpu'):
        """Load model from checkpoint, caching across calls."""
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
        cfg = ckpt['config']

        if (self._model is not None
                and self._device == device
                and self._model.model_name == cfg['model_name']):
            # Same architecture, just load new weights
            self._model.load_state_dict(ckpt['model_state_dict'])
            self._model.eval()
            return

        # Build fresh model
        model = GPT2Triadic(
            model_name=cfg['model_name'],
            n_triadic_bits=cfg['n_triadic_bits'],
            freeze_base=cfg.get('freeze_base', False),
            head_mode=cfg.get('head_mode', 'simple'),
            activation=cfg.get('activation', 'ifsq'),
        )
        model.load_state_dict(ckpt['model_state_dict'])
        model.to(device)
        model.eval()

        self._model = model
        self._device = device

        # Tokenizer (cached)
        if self._tokenizer is None:
            from transformers import GPT2Tokenizer
            self._tokenizer = GPT2Tokenizer.from_pretrained(cfg['model_name'])
            self._tokenizer.pad_token = self._tokenizer.eos_token

    def extract(self, checkpoint_path, concepts, device='cpu'):
        """Extract triadic snapshot from a GPT-2 + Triadic checkpoint."""
        self._load_model(checkpoint_path, device)

        codes = {}
        continuous = {}
        composites = {}

        for concept in concepts:
            try:
                ids = self._tokenizer.encode(' ' + concept.replace('_', ' '))
                ids = ids[:self.max_tokens]
            except Exception:
                continue
            if not ids:
                continue

            x = torch.tensor([ids], dtype=torch.long, device=device)
            with torch.no_grad():
                _, triadic_proj = self._model(x)

            # Mean over sequence positions -> (n_bits,)
            proj = triadic_proj[0].mean(dim=0).cpu().numpy()

            # Binarize: active if > 0 (tanh output)
            bits = [1 if v > 0 else 0 for v in proj]
            composite = int(self._mapper.map(proj.tolist()))

            codes[concept] = bits
            continuous[concept] = proj.tolist()
            composites[concept] = composite

        # Parse step from filename
        basename = os.path.basename(checkpoint_path)
        step = 0
        m = re.search(r'step[-_](\d+)', basename)
        if m:
            step = int(m.group(1))

        return ConceptSnapshot(
            step=step,
            codes=codes,
            continuous=continuous,
            metadata={'composites': composites, 'n_bits': self.n_bits},
        )

    def similarity(self, code_a, code_b):
        """Jaccard similarity on active bits."""
        active_a = set(i for i, v in enumerate(code_a) if v == 1)
        active_b = set(i for i, v in enumerate(code_b) if v == 1)
        if not active_a and not active_b:
            return 1.0
        union = active_a | active_b
        if not union:
            return 0.0
        return len(active_a & active_b) / len(union)

    def shared_features(self, code_a, code_b):
        """Indices where both codes are active."""
        return [i for i in range(min(len(code_a), len(code_b)))
                if code_a[i] == 1 and code_b[i] == 1]

    def algebraic_similarity(self, composite_a, composite_b):
        """GCD-based Jaccard on prime factors."""
        from triadic import prime_factors
        factors_a = set(prime_factors(composite_a))
        factors_b = set(prime_factors(composite_b))
        union = factors_a | factors_b
        if not union:
            return 0.0
        return len(factors_a & factors_b) / len(union)


# ######################################################################
#  STANDALONE TEST
# ######################################################################

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Test TriadicExtractor')
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--device', default='cuda')
    args = parser.parse_args()

    concepts = [
        'entropy', 'gravity', 'molecule', 'DNA', 'algebra',
        'consciousness', 'syntax', 'harmony', 'temperature', 'evolution',
    ]

    ext = TriadicExtractor(n_bits=65)
    snap = ext.extract(args.checkpoint, concepts, device=args.device)

    print(f'Step: {snap.step}')
    print(f'Concepts extracted: {len(snap.codes)}')
    print(f'Code dim: {snap.code_dim}')
    print()
    for c in concepts:
        if c in snap.codes:
            active = snap.active_indices(c)
            print(f'  {c:<20} {len(active)} active bits: {active[:10]}...')
