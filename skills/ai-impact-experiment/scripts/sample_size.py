#!/usr/bin/env python3
"""A/B 테스트 그룹당 표본 크기 (양측 alpha=0.05, power=0.8).
평균 지표: --baseline 평균 --sd 표준편차 --lift 0.05
비율 지표: --rate 0.12 --lift 0.10   (lift = 상대 개선율)"""
import argparse, math
Z_A, Z_B = 1.96, 0.8416
ap = argparse.ArgumentParser()
ap.add_argument("--baseline", type=float); ap.add_argument("--sd", type=float)
ap.add_argument("--rate", type=float); ap.add_argument("--lift", type=float, required=True)
ap.add_argument("--daily", type=float, help="하루 실험 대상 수(선택)")
a = ap.parse_args()
if a.rate is not None:
    p1, p2 = a.rate, a.rate * (1 + a.lift)
    n = (Z_A + Z_B) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2
else:
    if a.baseline is None or a.sd is None: ap.error("--baseline 과 --sd 가 필요해요")
    d = a.baseline * a.lift
    n = 2 * (Z_A + Z_B) ** 2 * a.sd ** 2 / d ** 2
n = math.ceil(n)
print(f"그룹당 {n:,}명 · 총 {2*n:,}명")
if a.daily: print(f"필요 기간 약 {max(14, math.ceil(2*n/a.daily))}일 (최소 14일)")
