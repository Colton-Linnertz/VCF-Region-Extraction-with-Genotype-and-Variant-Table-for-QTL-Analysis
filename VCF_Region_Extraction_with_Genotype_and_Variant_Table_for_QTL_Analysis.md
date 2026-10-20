# VCF Region Extraction with Genotype and Variant Table for QTL Analysis

![Status](https://img.shields.io/badge/status-usable-blue)
![Shell](https://img.shields.io/badge/shell-Bash-4EAA25?logo=gnubash&logoColor=white)
![Python](https://img.shields.io/badge/python-3.x-3776AB?logo=python&logoColor=white)
![Data](https://img.shields.io/badge/input-VCF%2FVCF.gz-lightgrey)

A lightweight bioinformatics workflow for extracting genomic regions from VCF files, filtering variants for selected samples, and converting annotated VCF records into a simplified tab-separated table for downstream analysis.

---

## Overview

Working with VCF files can involve navigating large genomic datasets and interpreting complex variant annotations. This repository provides two scripts to simplify that process:

- **Region extraction:** Extract genomic intervals, select samples, and filter variants using `bcftools` and GATK.
- **Table conversion:** Transform VCF records into a more readable tabular format for inspection and downstream analysis in Python, R, or other tools.

## Workflow

```text
Input VCF
    │
    ▼
regionsVCF.sh
    │
    ├── Extract genomic regions
    ├── Select specified samples
    ├── Filter variant records
    └── Compress and index regional VCFs
    │
    ▼
Regional VCF (.vcf.gz)
    │
    ▼
Decompress VCF
    │
    ▼
VCFtoTable.py
    │
    ├── Remove selected VCF metadata columns
    ├── Simplify selected homozygous genotypes
    └── Extract TYPE and gene_id annotations
    │
    ▼
Tab-separated variant table (.tsv)
```

## Scripts

### 1. `regionsVCF.sh` — Genomic Region Extraction

A Bash script for extracting specified genomic intervals and filtering variant records for two selected samples.

Applies an allele-count selection expression to identify genomic positions where the selected samples have discordant genotypes, enabling direct comparison of genetic differences between samples.

The allele-count expression can be modified to accommodate a different number of samples by adjusting the expected alternate allele count (AC) and total allele count (AN) to match the desired sample configuration.

**Key features**
- Extracts chromosome coordinates defined in a region list.
- Selects two specified samples from the input VCF.
- Restricts variants to biallelic SNPs and indels.
- Excludes heterozygous genotypes using a `bcftools` filter.
- Compresses and indexes output VCF files.

**Input format**

The region list is a whitespace- or tab-delimited file containing four fields per line:

| CHR | CORDS | sample1 | sample2 |
|---|---|---|---|
| chr1 | 183910165-193910165 | sample_A | sample_B |
| chr9 | 111996255-121996255 | sample_C | sample_D |

Chromosome names, coordinates, and sample IDs must match the input data and the script's expected format.

### 2. `VCFtoTable.py` — VCF-to-Table Conversion

A Python script that converts a VCF file into a tab-separated table designed for easier inspection and downstream analysis.

**Key features**
- Removes VCF metadata lines and the `QUAL`, `FILTER`, `INFO`, and `FORMAT` columns.
- Retains chromosome, position, reference allele, alternate allele, and sample columns.
- Simplifies genotype strings beginning with `0/0` to `0` and `1/1` to `1`.
- Extracts `TYPE` and `gene_id` values from pipe-delimited INFO annotations.
- Writes the resulting table as a TSV file.

**Input requirements**

The input should be an uncompressed VCF containing sample genotype columns and functional annotations, specifically, variant `TYPE`, in the expected pipe-delimited INFO format. VCF should be annotated with `SnpEff` to matche the positions used by the script.

## Requirements

| Tool | Purpose |
|---|---|
| `bcftools` | VCF region extraction, filtering, and compression |
| `tabix` | Indexing compressed VCF files |
| Java | Running the GATK JAR |
| GATK 3.7 | Variant selection in `regionsVCF.sh` |
| Python 3 | VCF-to-table conversion |

## Usage

### Step 1 — Configure and run region extraction

Update the paths and variables in `regionsVCF.sh` to match your environment, including the reference genome, input VCF, GATK JAR, region list, and output directories.

Run:

```bash
bash regionsVCF.sh
```

The script reads the region list specified by `SAMPLES` and generates compressed, indexed VCF files for the requested regions and sample pairs.

### Step 2 — Convert the extracted VCF to a table

The Python script expects an uncompressed VCF. Convert a generated regional VCF before running it:

```bash
bcftools view -Ov \
  -o region.vcf \
  region.vcf.gz
```

Then run:

```bash
python VCFtoTable.py region.vcf variants.tsv
```

The resulting `variants.tsv` file can be opened in a text editor or imported into Python, R, or spreadsheet software.

## Output

The final TSV contains a simplified representation of each variant, including:

- Chromosome and genomic position
- Reference and alternate alleles
- Selected sample genotype columns
- Variant type (`TYPE`)
- Gene identifier (`gene_id`)

The exact output depends on the input VCF, sample selection, filters, and annotation format.

## Notes and Limitations

- The region extraction script currently expects two sample IDs per region-list row.
- The allele-count expression `AC == 2 && AN == 4` assumes a particular allele-count configuration; adjust it for your sample set and filtering objective.
- The Python script simplifies only genotype strings beginning with `0/0` or `1/1`. Other genotype representations are retained as written. Does not account for a positions with a different alternative allele count, as `0/2`, `0/3`, etc.
- The `TYPE` and `gene_id` fields are extracted by position from a pipe-delimited INFO field, so the input annotation format must be compatible. Use `SnpEff` to add functional annotations for compatibility. 
- File paths and software versions are configured in the scripts and may need to be adapted to your environment.

## Potential Extensions

- [ ] Add command-line options for input paths, sample IDs, and genomic intervals.
- [ ] Support a variable number of samples.
- [ ] Add input validation and clearer error messages.
- [ ] Support additional genotype representations, including phased and missing genotypes.
- [ ] Add configurable annotation-field parsing.
- [ ] Include a small test dataset and example output.

---

*An example bioinformatics utility workflow for regional variant extraction, sample-level filtering, and simplified VCF data representation.*