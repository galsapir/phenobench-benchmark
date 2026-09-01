# ABOUTME: Reference submission image for the PhenoBench container contract.
# ABOUTME: Pinned base by digest; default entrypoint runs predict.py over /input and writes /output/predictions.csv.
FROM python@sha256:7a8b475003c4fe15a2cd4e55e5cfc2f3560bdc9333d624f24cdd6d4340fd7a17
# python:3.12-slim at the time of pinning
WORKDIR /app
COPY predict.py /app/predict.py
RUN useradd --uid 1000 --no-create-home runner
USER runner
ENTRYPOINT ["python3", "/app/predict.py"]
