#! /bin/bash


## extract a list of regions from VCF
# =================================== 
# name the project which is a directory for the output
# contig format: "chr14:13000000-17121752"
# extract specific samples from VCF: -sn sampleName (omit -sn to get all samples in vcf)
# -select "AC == 2 && AN == 4" gives position where 2 samples differ (adjust for more samples)
# AC = ALT allele count
# AN = Number of alleles = REF + ALT count 

## EXPECTED SAMPLES INPUT:
# ========================
# CHR CORDS sample1 sample2
# chr1	183910165-193910165	sample1name	sample2name
# chr9	111996255-121996255	sample1name	sample2name
# chr15	80761514-90761514	sample1name	sample2name

# requires GATK v3.7
GATK="/path/to/GenomeAnalysisTK.jar"
TOOL="SelectVariants"
REF="/path/to/reference.fa"
VCF="/path/to/vcf.gz"
VCFlabel="/label/output/vcfs/with/source/vcf"
SELECT="/path/to/select/directory/with/projects"
PROJECT="/name/project"
SAMPLES="list.regions.txt"


while read CHR CORDS sample1 sample2;
do

	bcftools view -Oz -r "${CHR}:${CORDS}" -o "${SELECT}/${PROJECT}/${VCFlabel}.${CHR}.${CORDS}.vcf.gz" "${VCF}" \
	&& tabix "${SELECT}/${PROJECT}/${VCFlabel}.${CHR}.${CORDS}.vcf.gz" \
	&& java -jar ${GATK} -T ${TOOL} -nt 12 -R ${REF} -V "${SELECT}/${PROJECT}/${VCFlabel}.${CHR}.${CORDS}.vcf.gz" \
	--restrictAllelesTo BIALLELIC \
	-selectType SNP \
	-selectType INDEL \
	-sn ${sample1} \
	-sn ${sample2} \
	-select "AC == 2 && AN == 4"| bcftools view -Oz --threads 12 -g ^het - -o "${SELECT}/${PROJECT}/${VCFlabel}.${sample1}.${sample2}.${CHR}.${CORDS}.vcf.gz" \
	&& tabix "${SELECT}/${PROJECT}/${VCFlabel}.${sample1}.${sample2}.${CHR}.${CORDS}.vcf.gz"

done < $SAMPLES
