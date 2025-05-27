#!/usr/bin/env python3
import argparse
from pymatgen.io.vasp import Xdatcar
from pymatgen.core.periodic_table import Element
from vasppy.rdf import RadialDistributionFunction
from matplotlib import pyplot as plt

def filter_structures_by_species(structures, species_i, species_j):
    filtered = []
    for s in structures:
        species_in_structure = {str(site.specie) for site in s.sites}
        if species_i in species_in_structure and species_j in species_in_structure:
            filtered.append(s)
    return filtered


def main():
    parser = argparse.ArgumentParser(description="Compute RDF from XDATCAR between given time windows.")
    parser.add_argument("--dt", type=float, required=True, help="Time step in femtoseconds (e.g. 2)")
    parser.add_argument("--file", type=str, default="XDATCAR", help="Path to XDATCAR file")
    parser.add_argument("--exclude", type=float, default=3.0, help="Time in ps to exclude at start")
    parser.add_argument("--total", type=float, default=10.0, help="Total time in ps to analyze")
    parser.add_argument("--pairs", type=str, required=True,
                        help="Comma-separated atom pairs for RDF (e.g. N-N,Pb-N,Pb-Pb)")
    parser.add_argument("--maxpeaks", type=int, default=3, help="Number of RDF maxima to print per pair")
    parser.add_argument("--smearing", type=float, default=0.05, help="Gaussian smearing width")
    parser.add_argument("--out", type=str, default="rdf_aimd.png", help="Output file name")


    args = parser.parse_args()

    # Load XDATCAR
    xd = Xdatcar(args.file)

    exclude_steps = int(args.exclude * 1000 / args.dt)
    total_steps = int(args.total * 1000 / args.dt)

    structures = xd.structures[exclude_steps:total_steps]

    pairs = [p.strip().split('-') for p in args.pairs.split(',')]

    plt.figure(figsize=(8, 6))
    plt.subplots_adjust(top=0.93, bottom=0.11, left=0.10, right=0.99)
    #plt.text(0.02, 0.92, '(a)', fontsize=12)

    for pair in pairs:
        species_i, species_j = pair

        filtered_structures = filter_structures_by_species(structures, species_i, species_j)
        if len(filtered_structures) == 0:
            print(f"No structures contain both {species_i} and {species_j}. Skipping this pair.")
            continue
        species_i = str(Element(species_i).symbol)
        species_j = str(Element(species_j).symbol)
        iat = species_i
        jat = species_j
        rdf = RadialDistributionFunction.from_species_strings(structures=filtered_structures, species_i=iat, species_j=jat)

        plt.plot(rdf.r, rdf.smeared_rdf(args.smearing), label=f"{species_i}-{species_j}")

        # Peak detection (local maxima)
        rdf_values = rdf.rdf
        r_values = rdf.r

        maxima = []
        for i in range(1, len(rdf_values) - 1):
            if rdf_values[i] > rdf_values[i - 1] and rdf_values[i] > rdf_values[i + 1]:
                maxima.append((rdf_values[i], r_values[i]))
        maxima.sort(reverse=True, key=lambda x: x[0])

        print(f"Top {args.maxpeaks} maxima for {species_i}-{species_j}:")
        for v, rpos in maxima[:args.maxpeaks]:
            print(f"  g(r) = {v:.3f} at r = {rpos:.3f} Å")
        print()

    plt.xlabel(r'$r$ / Å', fontsize=16)
    plt.ylabel(r'$g(r)$', fontsize=16)
    plt.xlim([0, 4])
    plt.legend(frameon=False, fontsize=16, loc="upper right")

    plt.savefig(args.out, format="png", dpi=400)
    #plt.show()

if __name__ == "__main__":
    main()

