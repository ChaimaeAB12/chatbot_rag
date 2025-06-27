import csv
import io

def extract_text_from_csv(file_bytes: bytes) -> str:
    # Essayer de décoder avec utf-8, fallback latin-1
    try:
        decoded = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        decoded = file_bytes.decode("latin-1", errors="ignore")

    stream = io.StringIO(decoded)
    try:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("No header found, fallback to raw reader")

        descriptions = []
        for i, row in enumerate(reader):
            sentence = ", ".join(
                [f"{key.strip()}: {value.strip()}" for key, value in row.items()]
            )
            descriptions.append(f"Ligne {i+1} → {sentence}.")
        return "\n".join(descriptions)

    except Exception:
        # fallback brut si échec DictReader
        stream.seek(0)
        reader = csv.reader(stream)
        lines = ["\t".join(row) for row in reader]
        return "\n".join(lines)
