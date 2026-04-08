class AdaptiveAgent:
    def __init__(self):
        # initial weights aligned with detector categories
        self.weights = {
            "override": 0.4,
            "data_exfiltration": 0.35,
            "role_manipulation": 0.25
        }

    def update(self, categories, reward):
        # simple policy update
        for cat in categories:
            if cat not in self.weights:
                continue

            if reward < 0:
                self.weights[cat] -= 0.05
            else:
                self.weights[cat] += 0.05

        # clamp values between 0 and 1
        for k in self.weights:
            self.weights[k] = max(0, min(1, self.weights[k]))