# RDF Computation from VASP XDATCAR

This Python script computes the **Radial Distribution Function (RDF)** from VASP's `XDATCAR` file. It allows you to exclude initial dynamics (e.g., equilibration), specify time ranges, atom pairs, smearing width, and more.

## 🔧 Requirements

Make sure you have the following Python packages installed:

- `pymatgen`
- `vasppy`
- `matplotlib`

You can install them via pip (note: `vasppy` may require manual installation or cloning from GitHub):

```bash
pip install pymatgen matplotlib
pip install git+https://github.com/JamesAlexanderHill/vasppy.git
```

## 🚀 Usage

```bash
python compute_rdf.py --dt 2 \
                      --file XDATCAR \
                      --exclude 3 \
                      --total 10 \
                      --pairs Si-O,O-O,Si-Si \
                      --smearing 0.05 \
                      --maxpeaks 3
```

### Parameters

| Argument       | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| `--dt`         | float   | Time step in femtoseconds (required)                                        |
| `--file`       | string  | Path to `XDATCAR` file (default: `XDATCAR`)                                 |
| `--exclude`    | float   | Time to exclude from the beginning of the trajectory (in picoseconds)       |
| `--total`      | float   | Total time range to consider (in picoseconds)                               |
| `--pairs`      | string  | Comma-separated list of atomic pairs to compute RDFs (e.g. `Si-O,O-O`)       |
| `--smearing`   | float   | Gaussian smearing width (default: `0.05`)                                   |
| `--maxpeaks`   | int     | Number of RDF maxima to print for each pair                                 |

## 📊 Output

- Saves the RDF plot as: `rdf_aimd_filtered.png`
- Prints the top local maxima of `g(r)` for each atomic pair in the terminal (e.g., position of peaks)

## 📎 Example

```bash
python compute_rdf.py --dt 2 --pairs "Si-O,O-O" --exclude 3 --total 10
```

This computes the RDFs for Si–O and O–O between 3 ps and 10 ps, assuming a 2 fs timestep.

## 🧪 Notes

- Atom types are case-sensitive and should be valid chemical symbols (e.g. `Si`, `O`, `Na`, not `si` or `oxygen`).
- The script automatically filters structures to only include those that contain both atoms of each specified pair.
- Local maxima are detected from unsmeared RDF data, and the smeared RDF is plotted.

## 📬 Contact

For improvements or bug reports, feel free to open an issue or submit a pull request.
