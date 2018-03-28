import numpy as np


class Scaler:
    def __init__(self, A=None):
        self.A = A

    def scale(self, ts):
        for t in ts:
            yield self.scale_one(t)

    def scale_one(self, t):
        return t


class Linear(Scaler):  # SP-CT
    pass


class AlphaToT(Scaler):  # α > 0 -> 0 < t < α^{-1}
    def __init__(self, A=None):
        super().__init__(A)
        cfm = np.linalg.eigvals(self.A)
        self.rho = np.max(np.abs(cfm))

    def scale_one(self, alpha):
        return 1 / (1 / alpha + self.rho)


class Rho(Scaler):  # pWalk, Walk
    def __init__(self, A=None):
        super().__init__(A)
        cfm = np.linalg.eigvals(self.A)
        self.rho = np.max(cfm)

    def scale_one(self, t):
        return t / self.rho


class Fraction(Scaler):  # Forest, logForest, Comm, logComm, Heat, logHeat, SCT, SCCT, ...
    def scale_one(self, t):
        return 0.5 * t / (1.0 - t)


class FractionReversed(Scaler):  # RSP, FE
    def scale_one(self, beta):
        return (1.0 - beta) / beta
