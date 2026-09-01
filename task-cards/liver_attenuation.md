# Liver Attenuation Task Card

Status: draft

Task id: `liver_attenuation`

Evidence status: grounded

Evidence reviewed: 2026-07-28

Benchmark status: complete

## Target

Hologic/SuperSonic MACH 30 Att.PLUS attenuation coefficient. It quantifies
frequency-normalized ultrasound energy loss and generally rises with hepatic
fat.

Implementation facts:

- target field: `c__attenuation`
- target dataset: `liver_ultrasound`
- target source: None (loaded through HPP `hpp_data_loader`)
- default research stage: `00_00_visit`
- valid range: 0.10-1.50 dB/cm/MHz; a PhenoBench plausibility filter,
  not a device or diagnostic interval
- primary metric: R2

## Why This Matters

Liver attenuation adds a hepatic-fat imaging marker distinct from blood scores.
Forecasting it does not establish MASLD, histologic grade, causality, or
intervention response.

## Related HPP Measurements

HPP work jointly analyzed gut-microbiome pathways with liver attenuation, CGM,
and DXA. Same-visit comparators include sound speed, viscosity, elasticity,
FLI, and liver blood tests; this Task does not establish their relationships.

## Benchmark-Track Evidence

OpenEvidence review prioritized a fixed Nightingale metabolic panel, then DXA
regional body composition, for hepatic-fat prediction beyond age/sex/BMI.
Metabolomic profiles show associations with liver fat distinct from visceral
fat, while DXA android/gynoid and visceral fat capture adiposity not represented
by BMI alone. HPP microbiome work linked many microbial features with liver
attenuation, but that evidence was cross-sectional and did not justify
prioritizing a microbiome track over Nightingale or DXA.

## V0 Benchmark Execution

The frozen same-visit V1→V1 matrix completed on 2026-07-29. All six rows are
locally successful, remotely `FINISHED` in operational source, and share the exact
cohort within each track.

- Nightingale: n=7,065; test=1,066; best R2=0.131 (Ridge), with paired
  delta R2 +0.047 [0.022, 0.071] over age/sex/BMI.
- DXA: n=8,594; test=1,284; best R2=0.130 (Ridge), with paired delta R2
  +0.053 [0.032, 0.072].
- Full rows and provenance:
  deep dive and
  aggregate review.

## Clinically Meaningful Variants

Continuous attenuation remains primary. A same-platform, single-center NAFLD
study reported Att.PLUS thresholds of 0.46/0.50/0.52 dB/cm/MHz for at least
S1/S2/S3 (AUROC 0.82/0.70/0.73). These are hypothesis-only leads: even a binary
at-least-S1 Task requires HPP acquisition/software, population, balance, and
repeatability validation. Canon ATI and CAP thresholds are not interchangeable.

**These numbers are under reconciliation and must not be acted on yet -
[research-harness#2](https://github.com/PhenoAI/research-harness/issues/2).**
Pheno's HPP dataset documentation carries a **different** same-device Att.PLUS
grade set: `S0 < 0.63 / S1 0.63-0.74 / S2 0.74-0.83 / S3 > 0.83`, cited to Popa
et al. 2021, which measured Att.PLUS on the same Aixplorer MACH 30. So our own
documentation puts the S1 boundary at **0.63** where this card puts it at
**0.46**, and the harness figure is the one wired into runnable binning code
(`knowledge_base/datasets/liver_ultrasound/loader.md`). HPP's median attenuation
is 0.39, so the choice materially changes the cohort's steatosis character.

Neither number is endorsed here pending that reconciliation. Note also that
Tanpowpong 2024 is **not retrievable in the paperclip corpus**, so this card's
own claim that it is same-platform is uncorroborated on our side.

## Baselines And Ceilings

`NoFeaturesPredictor` contributes no modality features; `DemographicFloorStrategy`
fits age, sex, and BMI. Last observation carried forward (LOCF) copies prior Y.
Ordinary least squares (OLS) and gradient-boosted trees (GBDT) fit prior Y plus
demographics. HealthFormer reported
LOCF and per-modality linear baselines, not trees or the demographic floor.
Compare representations on one cohort.

## Caveats

- The dataset has no formal global quality flag; acquisition failures are
  filtered upstream.
- Operator, protocol, body depth/BMI, and device algorithm affect values.
- Strong autocorrelation can make LOCF difficult to beat.

## Metrics

R2 is primary. Also report RMSE, MAE, Pearson r, Spearman rho, and same-cohort
deltas against LOCF. Review age/BMI residuals and target-range coverage.

## References

- Lutsker et al. (2026), HealthFormer, <https://arxiv.org/abs/2604.27899>.
- HPP `liver_ultrasound` dataset documentation for `c__attenuation`.
- Tanpowpong et al. (2024), Att.PLUS versus MRI-PDFF,
  <https://doi.org/10.1016/j.wfumbo.2024.100043>.
- Keshet and Segal (2024), HPP microbiome and metabolic-health map,
  <https://doi.org/10.1038/s41467-024-53832-y>.
- Pang et al. (2022), adiposity, metabolomics, and NAFLD risk,
  <https://doi.org/10.1093/ajcn/nqab392>.
- Lind et al. (2021), metabolomic profiles of liver and visceral fat,
  <https://doi.org/10.1210/clinem/dgaa693>.

## Open Questions

- Does HPP repeatability support a device-matched binary threshold?
- **Which Att.PLUS grade boundaries are operative for HPP - 0.46 (Tanpowpong
  2024, this card) or 0.63 (Popa 2021, the HPP dataset docs)?** Open at
  [research-harness#2](https://github.com/PhenoAI/research-harness/issues/2).
  Whichever wins, both repositories should name the same study, and this card
  needs the corresponding edit. Blocked on that reconciliation, deliberately not
  guessed here.
- Where does the `0.31 dB/cm/MHz` "steatosis suspected" cutoff come from? It is
  unsourced in the HPP dataset docs yet drives their headline prevalence figure
  and ships as binning code. Same issue.
