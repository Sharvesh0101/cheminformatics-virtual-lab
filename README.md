# Cheminformatics Virtual Laboratory

A Streamlit recreation inspired by the supplied screenshots of the Cheminformatics Virtual Laboratory.

## Run locally
1. Install Python 3.10 or newer.
2. In a terminal, run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Open the local URL shown by Streamlit.

## Deploy on Streamlit Community Cloud
1. Upload `app.py` and `requirements.txt` to a GitHub repository.
2. In Streamlit Community Cloud, choose the repository and `app.py` as the main file.
3. Deploy.

## Included pages
- Home / introduction
- Theory notes
- SMILES validation and 2D/optional 3D visualization
- Molecular property calculator and CSV/TXT downloads
- Multi-molecule structure–property comparison
- Multiple-choice assessment
- Downloadable final project report

Chemistry functionality depends on RDKit being installed successfully. This is a recreation based on screenshots, not the original source code, so details may differ from the original application.
