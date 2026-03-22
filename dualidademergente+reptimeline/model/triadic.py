"""
Triadic Algebra — Pure-Python neurosymbolic bridge.

Maps continuous hidden states from the transformer into discrete
prime-factor integers. Provides algebraic operations (subsumption,
composition, gap analysis) for transparent semantic verification.

Copied from triadic-microgpt/src/triadic.py, adapted for 65 bits.
Zero external dependencies — primes are computed via a simple sieve.
"""

import math


# ============================================================
# Prime Number Utilities
# ============================================================

def sieve_primes(limit):
    """Return all primes up to `limit` using the Sieve of Eratosthenes."""
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]


# Pre-compute first 100 primes (more than enough for n_bits <= 65)
_PRIMES_CACHE = sieve_primes(600)


def nth_prime(n):
    """Return the nth prime (1-indexed: nth_prime(1) = 2, nth_prime(2) = 3, ...)."""
    if n <= 0:
        raise ValueError("n must be >= 1")
    if n <= len(_PRIMES_CACHE):
        return _PRIMES_CACHE[n - 1]
    while len(_PRIMES_CACHE) < n:
        candidate = _PRIMES_CACHE[-1] + 2
        while True:
            if all(candidate % p != 0 for p in _PRIMES_CACHE if p * p <= candidate):
                _PRIMES_CACHE.append(candidate)
                break
            candidate += 2
    return _PRIMES_CACHE[n - 1]


def prime_factors(n):
    """Return the sorted list of unique prime factors of n."""
    if n <= 1:
        return []
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors


# ============================================================
# Prime Mapper — Maps projections to composite primes
# ============================================================

class PrimeMapper:
    """
    Maps continuous projections (from tanh, in [-1, 1]) to composite prime integers.

    Each bit position is assigned a unique prime. If projection[i] > 0,
    then prime[i] is included in the composite product.
    """

    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.primes = [nth_prime(i + 1) for i in range(n_bits)]

    def map(self, projections):
        composite = 1
        for proj, prime in zip(projections, self.primes):
            val = proj.data if hasattr(proj, 'grad') else proj
            if val > 0:
                composite *= prime
        return composite

    encode = map

    def get_bits(self, projections):
        return [1 if (p.data if hasattr(p, 'grad') else p) > 0 else 0
                for p in projections]

    def explain(self, composite):
        factors = []
        bit_indices = []
        for i, prime in enumerate(self.primes):
            if composite % prime == 0:
                factors.append(prime)
                bit_indices.append(i)
        return {
            'composite': composite,
            'factors': factors,
            'active_bits': bit_indices,
            'n_active': len(factors),
            'n_total': self.n_bits,
        }


# ============================================================
# Triadic Validator — Algebraic semantic operations
# ============================================================

class TriadicValidator:
    """
    Verifies semantic relationships using prime-factor algebra.

    Three operations IMPOSSIBLE with cosine similarity:
      1. Subsumption — Does concept A contain all features of B?
      2. Composition — Create a concept with all features of A and B
      3. Gap Analysis — Exactly WHICH features differ between A and B?
    """

    @staticmethod
    def subsumes(a, b):
        if b == 0:
            return False
        return a % b == 0

    @staticmethod
    def compose(*concepts):
        result = concepts[0]
        for c in concepts[1:]:
            result = (result * c) // math.gcd(result, c)
        return result

    @staticmethod
    def explain_gap(a, b):
        shared = math.gcd(a, b)
        only_in_a = a // shared
        only_in_b = b // shared
        return {
            'shared': shared,
            'shared_factors': prime_factors(shared),
            'only_in_a': only_in_a,
            'only_in_a_factors': prime_factors(only_in_a),
            'only_in_b': only_in_b,
            'only_in_b_factors': prime_factors(only_in_b),
            'a_contains_b': (a % b == 0),
            'b_contains_a': (b % a == 0),
        }

    @staticmethod
    def analogy(a, b, c):
        shared_ab = math.gcd(a, b)
        only_in_a = a // shared_ab
        only_in_b = b // shared_ab
        c_reduced = c // math.gcd(c, only_in_a)
        target = (c_reduced * only_in_b) // math.gcd(c_reduced, only_in_b)
        return target

    @staticmethod
    def similarity(a, b):
        factors_a = set(prime_factors(a))
        factors_b = set(prime_factors(b))
        if not factors_a and not factors_b:
            return 1.0
        shared = factors_a & factors_b
        total = factors_a | factors_b
        return len(shared) / len(total) if total else 0.0

    @staticmethod
    def intersect(a, b):
        return math.gcd(a, b)

    @staticmethod
    def difference(a, b):
        return a // math.gcd(a, b)

    @staticmethod
    def symmetric_difference(a, b):
        g = math.gcd(a, b)
        return (a // g) * (b // g)

    @staticmethod
    def negate(a, n_bits=65):
        omega = 1
        for i in range(n_bits):
            omega *= nth_prime(i + 1)
        return omega // a

    @staticmethod
    def project(a, category_primes):
        result = 1
        for p in category_primes:
            if a % p == 0:
                result *= p
        return result


# ============================================================
# Bitwise Mapper — O(1) alternative to PrimeMapper
# ============================================================

class BitwiseMapper:
    """Maps projections to bitmask integers instead of prime composites.
    Isomorphic to PrimeMapper but uses O(1) bitwise operations."""

    def __init__(self, n_bits):
        self.n_bits = n_bits

    def map(self, projections):
        bitmask = 0
        for i, proj in enumerate(projections[:self.n_bits]):
            val = proj.data if hasattr(proj, 'grad') else proj
            if val > 0:
                bitmask |= (1 << i)
        return bitmask

    encode = map

    def get_bits(self, projections):
        return [1 if (p.data if hasattr(p, 'grad') else p) > 0 else 0
                for p in projections[:self.n_bits]]

    def to_prime(self, bitmask, prime_mapper):
        composite = 1
        for i in range(self.n_bits):
            if bitmask & (1 << i):
                composite *= prime_mapper.primes[i]
        return composite

    def from_prime(self, composite, prime_mapper):
        bitmask = 0
        for i, p in enumerate(prime_mapper.primes):
            if composite % p == 0:
                bitmask |= (1 << i)
        return bitmask

    def explain(self, bitmask):
        active = []
        for i in range(self.n_bits):
            if bitmask & (1 << i):
                active.append(i)
        return {
            'bitmask': bitmask,
            'active_bits': active,
            'n_active': len(active),
            'n_total': self.n_bits,
        }


class BitwiseValidator:
    """Algebraic semantic operations using O(1) bitwise ops."""

    @staticmethod
    def subsumes(a, b):
        return (a & b) == b

    @staticmethod
    def compose(*concepts):
        result = 0
        for c in concepts:
            result |= c
        return result

    @staticmethod
    def explain_gap(a, b):
        return {
            'shared': a & b,
            'only_in_a': a & ~b,
            'only_in_b': b & ~a,
            'a_contains_b': (a & b) == b,
            'b_contains_a': (a & b) == a,
        }

    @staticmethod
    def analogy(a, b, c):
        only_a = a & ~b
        only_b = b & ~a
        return (c & ~only_a) | only_b

    @staticmethod
    def similarity(a, b):
        shared = bin(a & b).count('1')
        total = bin(a | b).count('1')
        if total == 0:
            return 1.0
        return shared / total

    @staticmethod
    def intersect(a, b):
        return a & b

    @staticmethod
    def difference(a, b):
        return a & ~b

    @staticmethod
    def symmetric_difference(a, b):
        return a ^ b

    @staticmethod
    def negate(a, n_bits=65):
        mask = (1 << n_bits) - 1
        return a ^ mask

    @staticmethod
    def project(a, category_bits):
        mask = 0
        for b in category_bits:
            mask |= (1 << b)
        return a & mask


DefaultMapper = BitwiseMapper
DefaultValidator = BitwiseValidator
