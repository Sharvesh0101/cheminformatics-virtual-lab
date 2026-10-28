import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Cheminformatics Virtual Laboratory", page_icon="🧪", layout="wide", initial_sidebar_state="expanded")

# Theme and styling inspired by the supplied reference screenshots
st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp { background: #0e1117; color: #f5f6fa; }
section[data-testid="stSidebar"] { background: #262730; border-right: 1px solid #343640; }
section[data-testid="stSidebar"] .block-container { padding-top: 1.4rem; }
.hero { text-align:center; padding: 2rem 0 1.4rem; }
.hero .flask { font-size: 4rem; line-height: 1.4; }
.hero h1 { font-size: clamp(2rem, 5vw, 3.7rem); font-weight: 800; line-height: 1.22; margin: .25rem 0 1rem; color: #f7f7fb; }
.hero h3 { color: #315b83; font-size: clamp(1.1rem, 2.5vw, 1.8rem); margin: .3rem 0; }
.hero p { font-size: 1.15rem; line-height: 1.7; }
.section-rule { border:0; border-top:1px solid #3a3d46; margin:2.2rem 0; }
.info-card { background:#182f46; border-radius:12px; padding:1rem 1.2rem; color:#7bb7f4; }
.small-muted { color:#a4a7b0; }
div[data-testid="stMetric"] { background:#171a22; border:1px solid #30333d; border-radius:12px; padding: .9rem; }
.stButton > button, .stDownloadButton > button { border-radius: 9px; font-weight:600; }
h1, h2, h3 { letter-spacing: -.02em; }
</style>
""", unsafe_allow_html=True)

if "student_name" not in st.session_state: st.session_state.student_name = ""
if "reg_no" not in st.session_state: st.session_state.reg_no = ""
if "smiles" not in st.session_state: st.session_state.smiles = "CCO"

PAGES = {
    "🏠 Home": "home",
    "📖 Theory": "theory",
    "🧬 Molecular Visualization": "visual",
    "📊 Molecular Properties Report": "properties",
    "📈 Structure–Property Analysis": "analysis",
    "📝 Assessment": "assessment",
    "📄 Final Project Report": "report",
}
with st.sidebar:
    st.markdown("## 🧪 Virtual Lab")
    st.caption("Navigation")
    page_label = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    page = PAGES[page_label]
    st.markdown("---")
    st.markdown("### 🧑‍🎓 Student Information")
    st.session_state.student_name = st.text_input("Student Name", value=st.session_state.student_name, placeholder="Enter your name")
    st.session_state.reg_no = st.text_input("Registration Number", value=st.session_state.reg_no, placeholder="Enter registration number")
    st.markdown("---")
    st.markdown("### 🎓 Learning Objectives")
    st.write("Students can learn:")
    for objective in ["SMILES notation", "Molecular representation", "2D visualization", "3D visualization", "Molecular descriptors", "Structure-property relationships"]:
        st.markdown(f"• {objective}")

def rdkit_available():
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors, rdMolDescriptors
        return Chem, Descriptors, rdMolDescriptors
    except Exception:
        return None, None, None

def molecule_from_smiles(smiles):
    Chem, Descriptors, rdMolDescriptors = rdkit_available()
    if Chem is None:
        return None, "RDKit is not installed. Install the packages in requirements.txt to enable molecular chemistry features."
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "This SMILES string could not be parsed. Check the notation and try again."
    return mol, None

def property_table(smiles):
    Chem, Descriptors, rdMolDescriptors = rdkit_available()
    mol, error = molecule_from_smiles(smiles)
    if error: return None, error
    data = [
        ("Canonical SMILES", Chem.MolToSmiles(mol)),
        ("Molecular formula", rdMolDescriptors.CalcMolFormula(mol)),
        ("Molecular weight (g/mol)", round(Descriptors.MolWt(mol), 3)),
        ("Exact molecular weight", round(Descriptors.ExactMolWt(mol), 4)),
        ("LogP (estimated)", round(Descriptors.MolLogP(mol), 3)),
        ("TPSA (Å²)", round(Descriptors.TPSA(mol), 3)),
        ("Hydrogen-bond donors", rdMolDescriptors.CalcNumHBD(mol)),
        ("Hydrogen-bond acceptors", rdMolDescriptors.CalcNumHBA(mol)),
        ("Rotatable bonds", rdMolDescriptors.CalcNumRotatableBonds(mol)),
        ("Heavy atoms", mol.GetNumHeavyAtoms()),
        ("Ring count", rdMolDescriptors.CalcNumRings(mol)),
    ]
    return pd.DataFrame(data, columns=["Property", "Value"]), None

def report_csv(df):
    return df.to_csv(index=False).encode("utf-8")

if page == "home":
    st.markdown("""
    <div class="hero">
      <div class="flask">🧪</div>
      <h1>Cheminformatics<br>Virtual Laboratory</h1>
      <h3>SRM Institute of Science and Technology, Tiruchirappalli</h3>
      <p>Faculty of Engineering and Technology |<br>School of Sciences | Division of Chemistry</p>
    </div>
    <hr class="section-rule">
    """, unsafe_allow_html=True)
    st.title("Welcome to the Virtual Laboratory 🔗")
    st.write("This interactive virtual laboratory helps students understand important concepts in cheminformatics and computational chemistry.")
    st.markdown("## 🧪 What can students do?")
    tasks = [
        "Enter any SMILES notation", "Validate molecular structures", "Generate 2D structures",
        "Generate interactive 3D structures", "Select different molecular visualization styles",
        "Calculate complete molecular properties", "Download molecular reports",
        "Compare multiple molecules", "Complete an assessment"
    ]
    for task in tasks: st.markdown(f"✅ {task}")
    st.markdown("## Example Molecules")
    st.dataframe(pd.DataFrame([
        ["Ethanol", "CCO"], ["Benzene", "c1ccccc1"], ["Phenol", "Oc1ccccc1"],
        ["Acetic Acid", "CC(=O)O"], ["Aspirin", "CC(=O)Oc1ccccc1C(=O)O"]
    ], columns=["Molecule", "SMILES"]), hide_index=True, use_container_width=True)
    st.markdown("<hr class='section-rule'>", unsafe_allow_html=True)
    st.markdown("## 👨‍🏫 Developed by")
    st.markdown("**Dr. C. Manivannan**")
    st.write("Assistant Professor")
    st.write("Division of Chemistry, School of Sciences")
    st.write("Faculty of Engineering and Technology")
    st.write("SRM Institute of Science and Technology, Tiruchirappalli")
    st.markdown("<div class='info-card'>📧 <b>For queries, contact:</b><br><a href='mailto:cmanivannan89@gmail.com'>cmanivannan89@gmail.com</a></div>", unsafe_allow_html=True)
    st.markdown("<hr class='section-rule'>", unsafe_allow_html=True)
    st.caption("🧪 Cheminformatics Virtual Laboratory | Developed using Python, Streamlit and RDKit")

elif page == "theory":
    st.title("📖 Cheminformatics Theory")
    st.write("Review the concepts behind molecular representations and computational chemistry.")
    with st.expander("1. What is cheminformatics?", expanded=True):
        st.write("Cheminformatics combines chemistry, computer science and information science to store, search, analyze and visualize chemical structures and their properties.")
    with st.expander("2. SMILES notation"):
        st.write("SMILES (Simplified Molecular Input Line Entry System) represents a molecular structure as a text string. Atoms are written as symbols, branches use parentheses, bonds can be shown with symbols, and ring closures use matching digits.")
        st.code("CCO  # ethanol\nc1ccccc1  # benzene\nCC(=O)O  # acetic acid")
    with st.expander("3. Molecular descriptors"):
        st.write("Descriptors are numerical or categorical features calculated from a molecular structure, such as molecular weight, LogP, topological polar surface area (TPSA), hydrogen-bond donors and acceptors.")
    with st.expander("4. Structure–property relationships"):
        st.write("A molecule's structure influences its physical, chemical and biological properties. Comparing descriptors across molecules can help identify patterns, while remembering that descriptors alone do not prove causation.")
    with st.expander("5. 2D and 3D visualization"):
        st.write("2D depictions show atoms and bonds in a plane. 3D conformers estimate spatial arrangements; they are models, not direct experimental measurements.")

elif page == "visual":
    st.title("🧬 Molecular Visualization")
    st.write("Enter a SMILES string to validate and visualize its molecular structure.")
    examples = {"Ethanol — CCO":"CCO", "Benzene — c1ccccc1":"c1ccccc1", "Phenol — Oc1ccccc1":"Oc1ccccc1", "Acetic acid — CC(=O)O":"CC(=O)O", "Aspirin":"CC(=O)Oc1ccccc1C(=O)O"}
    choice = st.selectbox("Quick examples", ["Custom"] + list(examples.keys()))
    if choice != "Custom": st.session_state.smiles = examples[choice]
    smiles = st.text_input("SMILES notation", key="smiles")
    mode = st.radio("Visualization style", ["2D structure", "3D conformer"], horizontal=True)
    if st.button("Validate and generate", type="primary"):
        mol, error = molecule_from_smiles(smiles)
        if error: st.error(error)
        else:
            st.success("Valid molecular structure!")
            Chem, _, _ = rdkit_available()
            try:
                from rdkit.Chem import Draw, AllChem
                if mode == "2D structure":
                    img = Draw.MolToImage(mol, size=(650, 420))
                    st.image(img, caption="2D molecular structure")
                else:
                    m3 = Chem.AddHs(mol)
                    status = AllChem.EmbedMolecule(m3, randomSeed=42)
                    if status == 0:
                        AllChem.MMFFOptimizeMolecule(m3)
                        st.info("A 3D conformer was generated. For an interactive 3D viewer, install py3Dmol and enable the optional viewer integration.")
                        try:
                            import py3Dmol
                            block = Chem.MolToMolBlock(m3)
                            view = py3Dmol.view(width=650, height=450)
                            view.addModel(block, "mol")
                            view.setStyle({"stick": {}})
                            view.zoomTo()
                            st.components.v1.html(view._make_html(), height=470, scrolling=False)
                        except Exception:
                            st.code(Chem.MolToMolBlock(m3), language="text")
                    else: st.warning("Could not generate a 3D conformer for this structure.")
            except Exception as e:
                st.error(f"Visualization error: {e}")
            st.code(Chem.MolToSmiles(mol), language="text")
    st.caption("Chemistry calculations require RDKit. Some advanced 3D rendering depends on optional py3Dmol.")

elif page == "properties":
    st.title("📊 Molecular Properties Report")
    st.write("Calculate common molecular descriptors from a valid SMILES notation.")
    smiles = st.text_input("SMILES notation", value=st.session_state.smiles, key="prop_smiles")
    if st.button("Calculate properties", type="primary"):
        df, error = property_table(smiles)
        if error: st.error(error)
        else:
            st.session_state["last_props"] = df
            st.session_state["last_smiles"] = smiles
    if "last_props" in st.session_state:
        st.subheader("Calculated properties")
        st.dataframe(st.session_state["last_props"], hide_index=True, use_container_width=True)
        st.download_button("⬇️ Download properties as CSV", report_csv(st.session_state["last_props"]), "molecular_properties.csv", "text/csv")
        st.download_button("⬇️ Download report as TXT", "\n".join(f"{r.Property}: {r.Value}" for r in st.session_state["last_props"].itertuples()).encode(), "molecular_report.txt", "text/plain")

elif page == "analysis":
    st.title("📈 Structure–Property Analysis")
    st.write("Compare descriptor patterns for two or more molecules.")
    raw = st.text_area("Enter one molecule per line as Name,SMILES", value="Ethanol,CCO\nBenzene,c1ccccc1\nPhenol,Oc1ccccc1\nAcetic acid,CC(=O)O", height=140)
    if st.button("Analyze molecules", type="primary"):
        rows, errors = [], []
        for line in raw.splitlines():
            if not line.strip(): continue
            parts = line.split(",", 1)
            if len(parts) != 2:
                errors.append(f"Could not read: {line}"); continue
            name, smiles = parts[0].strip(), parts[1].strip()
            df, error = property_table(smiles)
            if error: errors.append(f"{name}: {error}"); continue
            values = dict(zip(df["Property"], df["Value"]))
            rows.append({"Molecule": name, "SMILES": smiles, "Formula": values["Molecular formula"], "MW (g/mol)": values["Molecular weight (g/mol)"], "LogP": values["LogP (estimated)"], "TPSA (Å²)": values["TPSA (Å²)"], "H-bond donors": values["Hydrogen-bond donors"], "H-bond acceptors": values["Hydrogen-bond acceptors"]})
        for err in errors: st.warning(err)
        if rows:
            result = pd.DataFrame(rows)
            st.dataframe(result, hide_index=True, use_container_width=True)
            numeric = ["MW (g/mol)", "LogP", "TPSA (Å²)"]
            metric = st.selectbox("Plot descriptor", numeric)
            st.bar_chart(result.set_index("Molecule")[[metric]])
            st.download_button("⬇️ Download comparison CSV", report_csv(result), "molecule_comparison.csv", "text/csv")
        elif not errors: st.info("Add at least one molecule to analyze.")

elif page == "assessment":
    st.title("📝 Assessment")
    st.write("Check your understanding. Select one answer for each question, then submit.")
    questions = [
        ("What does SMILES stand for?", ["Simple Molecular Input Line Entry System", "Standard Molecule Index List", "Systematic Model of Isomers"], 0),
        ("Which SMILES represents ethanol?", ["c1ccccc1", "CCO", "CC(=O)O"], 1),
        ("Which descriptor is commonly used as an estimate of lipophilicity?", ["TPSA", "LogP", "Ring count"], 1),
        ("What do matching ring digits indicate in SMILES?", ["A ring closure", "An isotope", "A charge"], 0),
        ("What does molecular weight describe?", ["Number of rings only", "Mass of a molecule based on its atoms", "Its colour"], 1),
    ]
    with st.form("assessment_form"):
        answers = []
        for i, (q, opts, correct) in enumerate(questions):
            answers.append(st.radio(f"{i+1}. {q}", opts, key=f"q{i}"))
        submitted = st.form_submit_button("Submit assessment", type="primary")
    if submitted:
        score = sum(answer == questions[i][1][questions[i][2]] for i, answer in enumerate(answers))
        st.metric("Your score", f"{score} / {len(questions)}", f"{score/len(questions)*100:.0f}%")
        if score == len(questions): st.success("Excellent — all answers are correct!")
        elif score >= 3: st.info("Good work! Review the theory section for the questions you missed.")
        else: st.warning("Keep practising. Revisit the theory section and try again.")

elif page == "report":
    st.title("📄 Final Project Report")
    st.write("Create a simple downloadable project report for your lab work.")
    name = st.text_input("Project title", value="Cheminformatics Virtual Laboratory")
    objective = st.text_area("Aim / objective", value="To represent molecular structures using SMILES and calculate basic molecular descriptors.")
    method = st.text_area("Methodology", value="A SMILES string was entered, validated using RDKit, and used to generate molecular visualizations and descriptors.")
    observations = st.text_area("Observations / results", value="Record the molecular formula, molecular weight, LogP, TPSA and other descriptors calculated during the experiment.")
    conclusion = st.text_area("Conclusion", value="Cheminformatics tools can support molecular representation, visualization and descriptor-based comparisons.")
    if st.button("Generate project report", type="primary"):
        student = st.session_state.student_name or "Not provided"
        reg = st.session_state.reg_no or "Not provided"
        report = f"""CHEMINFORMATICS VIRTUAL LABORATORY — PROJECT REPORT
Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}
Student: {student}
Registration number: {reg}

PROJECT TITLE
{name}

AIM / OBJECTIVE
{objective}

METHODOLOGY
{method}

OBSERVATIONS / RESULTS
{observations}

CONCLUSION
{conclusion}
"""
        st.success("Your report is ready.")
        st.download_button("⬇️ Download project report (.txt)", report.encode("utf-8"), "cheminformatics_project_report.txt", "text/plain")
        st.text_area("Report preview", report, height=320)

st.markdown("---")
st.caption("🧪 Cheminformatics Virtual Laboratory · Python + Streamlit + RDKit")
