import secrets
import math


def uniform(a: float = 0.0, b: float = 1.0) -> float:
    """Cryptographically secure uniform sample in [a, b)."""
    # 53 random bits gives 53-bit precision double
    u = secrets.randbits(53) / (1 << 53)   # in [0, 1)
    return a + (b - a) * u

def exponentialdist(lam: float) -> float:
    """Cryptographically secure exponentially-distributed sample.
    Uses inverse transform sampling: x = -(1/lam) * ln(U), U ~ Uniform(0,1).
    """
    u = uniform()                      # reuse our secure uniform in [0,1)
    return -(1.0 / lam) * math.log(u)  # inverse CDF of exponential

if __name__ == "__main__":
    print("5 uniform samples:", [uniform() for _ in range(5)])
    print("5 exponential samples (lam=1.0):", [exponentialdist(1.0) for _ in range(5)])



