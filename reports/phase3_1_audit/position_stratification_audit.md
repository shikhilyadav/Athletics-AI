# ATHLETIX AI — Phase 3.1 Position Stratification Audit

**Auditor:** Statistical Quality Assurance  
**Status:** **PASS WITH LIMITATIONS**  
**Audit Target:** Position distribution across CV folds, rare positions, macro-group categorization

---

## 1. Audit Problem Statement: Granular Position Sparsity

In the NFL Big Data Bowl cohort ($N = 149$ verified players), prospects belong to 12 distinct roster positions. However, position frequencies are highly unbalanced:

```
NFL Position Frequencies (N = 149):
  WR:  34 prospects (22.8%)
  G:   16 prospects (10.7%)
  DE:  14 prospects (9.4%)
  CB:  14 prospects (9.4%)
  T:   13 prospects (8.7%)
  TE:  12 prospects (8.1%)
  SS:  12 prospects (8.1%)
  OLB: 10 prospects (6.7%)
  DT:   7 prospects (4.7%)
  FS:   7 prospects (4.7%)
  C:    7 prospects (4.7%)
  NT:   3 prospects (2.0%)  <-- RARE POSITION (N < 5)
```

**The Mathematical Impossibility of Granular Stratification:**
In a 5-fold cross-validation scheme, each fold requires at least 1 holdout instance of a class for that class to appear in all 5 validation splits ($N \ge K$). Because Nose Tackles (`NT`) comprise only $N = 3$ prospects, **it is mathematically impossible to stratify directly across the 12 granular NFL positions in 5 folds**. Any strict stratified splitter on `nfl_position` throws a runtime error or produces empty test folds for rare classes.

---

## 2. Implemented Architecture: Macro-Position Stratification

To maintain rigorous stratification without dropping rare positions, `src/models/model_comparison.py` implemented a **macro-position classification hierarchy** reflecting positional biomechanics and line-of-scrimmage role:

```python
# Code Reference: src/models/model_comparison.py lines 42-59
macro_position_map = {
    # Skill Offense (high speed, perimeter, open field)
    "WR": "SKILL_OFFENSE", "TE": "SKILL_OFFENSE",
    
    # Offensive Line (trench blocking, high mass, short-area power)
    "T": "LINE_OFFENSE", "G": "LINE_OFFENSE", "C": "LINE_OFFENSE",
    
    # Defensive Front (rush, run stop, high collision)
    "DE": "DEFENSIVE_FRONT", "DT": "DEFENSIVE_FRONT",
    "NT": "DEFENSIVE_FRONT", "OLB": "DEFENSIVE_FRONT",
    
    # Defensive Backs (coverage, open-field tracking, high backpedal)
    "CB": "DEFENSIVE_BACKS", "SS": "DEFENSIVE_BACKS", "FS": "DEFENSIVE_BACKS",
}
```

This yields 4 balanced macro-groups:
- `SKILL_OFFENSE`: 46 prospects (30.9%)
- `LINE_OFFENSE`: 36 prospects (24.2%)
- `DEFENSIVE_FRONT`: 34 prospects (22.8%)
- `DEFENSIVE_BACKS`: 33 prospects (22.1%)

---

## 3. Empirical Verification of Fold Allocations

The audit inspected all 50 fold partitions across the 10 repeats. Table 3.1 details the exact distribution of prospects across macro-groups for Repeat 1:

### Table 3.1: Actual Macro-Position Allocation Across Folds (Repeat 1)

| Fold Number | Total Players | SKILL_OFFENSE | LINE_OFFENSE | DEFENSIVE_FRONT | DEFENSIVE_BACKS |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Fold 1** | 30 | 9 | 7 | 7 | 7 |
| **Fold 2** | 30 | 9 | 7 | 7 | 7 |
| **Fold 3** | 30 | 9 | 7 | 7 | 7 |
| **Fold 4** | 30 | 9 | 8 | 6 | 7 |
| **Fold 5** | 29 | 10 | 7 | 7 | 5 |
| **Total** | **149** | **46** | **36** | **34** | **33** |

Across all 10 repeats, every validation fold contained:
- 9 to 10 Skill Offense players.
- 7 to 8 Offensive Linemen.
- 6 to 7 Defensive Front players.
- 5 to 7 Defensive Backs.

No fold experienced positional starvation.

---

## 4. Limitation: Within-Macro Granular Drift

While macro-level balance is maintained, granular position allocations within each macro-group vary randomly across folds:
- Nose Tackles (`NT`, $N=3$) appear in exactly 3 out of 5 folds per repeat, with 2 folds having zero `NT` test instances.
- Centers (`C`, $N=7$) have 1 or 2 instances per fold.

Because Ridge regression utilizes position dummy variables as linear additive offsets, folds missing an `NT` prospect evaluate the trench intercept using the broader defensive front coefficient.

---

## 5. Audit Verdict & Recommendation

**Verdict: PASS WITH LIMITATIONS**  
Macro-position stratification is an acceptable engineering solution that guarantees balance across trench, skill, and secondary players. However, researchers must document that rare granular positions ($N < 5$) cannot be guaranteed uniform representation across folds.
