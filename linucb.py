"""LinUCB contextual-bandit algorithm for adaptive UI selection."""

import json
import math

VARIANTS = ("hint", "example", "concise", "challenge")


def learner_features(context):
    """Convert learner context into a numerical feature vector."""
    experience = {
        "beginner": 0.0,
        "intermediate": 0.5,
        "advanced": 1.0,
    }

    preference = {
        "hint": 0,
        "example": 1,
        "concise": 2,
        "challenge": 3,
    }

    device = {
        "desktop": 0,
        "mobile": 1,
        "tablet": 2,
    }

    return [
        1.0,
        experience[context["experience_level"]],
        preference[context["learning_preference"]] / 3.0,
        device[context["device_type"]] / 2.0,
        context["diagnostic_score"] / 100.0,
    ]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mat_vec(matrix, vector):
    return [
        sum(matrix[i][j] * vector[j] for j in range(len(vector)))
        for i in range(len(vector))
    ]


def solve(matrix, vector):
    """Solve matrix * x = vector using Gaussian elimination."""
    n = len(vector)
    augmented = [
        list(map(float, matrix[i])) + [float(vector[i])]
        for i in range(n)
    ]

    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(augmented[r][col]))

        if abs(augmented[pivot][col]) < 1e-12:
            raise ValueError("LinUCB matrix is singular.")

        augmented[col], augmented[pivot] = (
            augmented[pivot],
            augmented[col],
        )

        divisor = augmented[col][col]
        augmented[col] = [v / divisor for v in augmented[col]]

        for row in range(n):
            if row == col:
                continue

            factor = augmented[row][col]
            augmented[row] = [
                augmented[row][j] - factor * augmented[col][j]
                for j in range(n + 1)
            ]

    return [augmented[i][-1] for i in range(n)]


def quadratic_form(matrix, vector):
    """Calculate vector.T * matrix * vector."""
    return dot(vector, mat_vec(matrix, vector))


class LinUCB:
    """Disjoint LinUCB with a separate linear model for each UI variant."""

    def __init__(self, alpha=0.8, state=None):
        if alpha < 0:
            raise ValueError("alpha must be non-negative.")

        self.alpha = float(alpha)
        self.dimension = 5

        self.A = {}
        self.b = {}
        self.counts = {}

        for variant in VARIANTS:
            self.A[variant] = [
                [
                    1.0 if i == j else 0.0
                    for j in range(self.dimension)
                ]
                for i in range(self.dimension)
            ]
            self.b[variant] = [0.0] * self.dimension
            self.counts[variant] = 0

        if state is not None:
            self.load_state(state)

    def select(self, context):
        x = learner_features(context)
        candidates = []

        for variant in VARIANTS:
            theta = solve(self.A[variant], self.b[variant])
            predicted = dot(theta, x)

            # Solve A * z = x to calculate the uncertainty.
            z = solve(self.A[variant], x)
            uncertainty = math.sqrt(
                max(0.0, dot(x, z))
            )

            exploration = self.alpha * uncertainty
            total = predicted + exploration

            candidates.append({
                "variant": variant,
                "predicted_reward": predicted,
                "exploration_bonus": exploration,
                "score": total,
                "observations": self.counts[variant]
            })

        selected = max(
            candidates,
            key=lambda item: item["score"]
        )

        return {
            **selected,
            "method": "linucb",
            "reason": (
                f"LinUCB selected {selected['variant']}: "
                f"predicted reward "
                f"{selected['predicted_reward']:.3f}, "
                f"exploration bonus "
                f"{selected['exploration_bonus']:.3f}."
            ),
            "scores": candidates
        }

    def update(self, variant, context, observed_reward):
        """Update the selected variant after observing its reward."""
        if variant not in VARIANTS:
            raise ValueError("Unknown UI variant.")

        if not isinstance(observed_reward, (int, float)):
            raise ValueError("Reward must be numeric.")

        if not math.isfinite(observed_reward) or not 0 <= observed_reward <= 1:
            raise ValueError("Reward must be between 0 and 1.")

        x = learner_features(context)
        matrix = self.A[variant]

        for i in range(self.dimension):
            for j in range(self.dimension):
                matrix[i][j] += x[i] * x[j]

            self.b[variant][i] += observed_reward * x[i]

        self.counts[variant] += 1

    def state(self):
        """Return JSON-serialisable model state for persistence."""
        return {
            "alpha": self.alpha,
            "dimension": self.dimension,
            "A": self.A,
            "b": self.b,
            "counts": self.counts,
        }

    def load_state(self, state):
        """Restore a previously saved model state."""
        if state.get("dimension") != self.dimension:
            raise ValueError("Incompatible LinUCB state.")

        if set(state.get("A", {})) != set(VARIANTS):
            raise ValueError("Invalid LinUCB matrix state.")

        if set(state.get("b", {})) != set(VARIANTS):
            raise ValueError("Invalid LinUCB reward state.")

        for variant in VARIANTS:
            matrix = state["A"][variant]
            vector = state["b"][variant]
            count = state["counts"][variant]

            if (
                len(matrix) != self.dimension
                or any(len(row) != self.dimension for row in matrix)
                or len(vector) != self.dimension
                or type(count) is not int
                or count < 0
            ):
                raise ValueError("Invalid LinUCB state dimensions.")

        self.alpha = float(state["alpha"])
        self.A = {
            variant: [
                [float(value) for value in row]
                for row in state["A"][variant]
            ]
            for variant in VARIANTS
        }
        self.b = {
            variant: [float(value) for value in state["b"][variant]]
            for variant in VARIANTS
        }
        self.counts = dict(state["counts"])

    def to_json(self):
        return json.dumps(self.state())