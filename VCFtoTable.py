#!/usr/bin/env python3


## =========================================
## USAGE:
# python VCFtoTable.py input.vcf output.tsv
## =========================================
# NOTES:
# outputs readable dataframe from whole VCF
# designed to be step 2 after 'regionsVCF.sh'
# requires VCF annotated for functional effect & variant type (SnpEff)
# begin with a uncompressed VCF file (small region)
# convert genotypes to 0 or 1 instead of 0/0:.....
# extract variant TYPE & gene_id from INFO column and put in new columns
# comments descibe what fields are being removed from VCF
# ----------------------------------------------------------------------


import sys
import csv


def process_vcf(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.reader(infile, delimiter="\t")
        writer = csv.writer(outfile, delimiter="\t")

        header_written = False
        for row in reader:
            # remove metadata/header lines
            if row[0].startswith("##"):
                continue
            if row[0].startswith("#CHROM"):
                row[0] = "CHROM"
                # remove QUAL (5), FILTER (6), INFO (7), FORMAT (8)
                header = row[:5] + row[9:]
                # add TYPE and gene_id columns
                header.append("TYPE")
                header.append("gene_id")
                writer.writerow(header)
                header_written = True
                continue

            if not header_written:
                continue

            # extract TYPE (4th–5th |) and gene_id (1st–2nd |) from INFO col
            info_field = row[7] if len(row) > 7 else ""
            parts = info_field.split("|")
            type_val = parts[4] if len(parts) > 5 else ""
            gene_id_val = parts[1] if len(parts) > 2 else ""

            # clean up sample columns (replace 0/0:* → 0, 1/1:* → 1)
            cleaned_row = []
            for i, val in enumerate(row):
                if i >= 9:  # sample columns only
                    if val.startswith("0/0"):
                        cleaned_row.append("0")
                    elif val.startswith("1/1"):
                        cleaned_row.append("1")
                    else:
                        cleaned_row.append(val)
                else:
                    cleaned_row.append(val)

            # remove QUAL (5), FILTER (6), INFO (7), FORMAT (8)
            filtered_row = cleaned_row[:5] + cleaned_row[9:]

            # Add TYPE and gene_id
            filtered_row.append(type_val)
            filtered_row.append(gene_id_val)

            writer.writerow(filtered_row)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.vcf output.tsv")
        sys.exit(1)

    process_vcf(sys.argv[1], sys.argv[2])
