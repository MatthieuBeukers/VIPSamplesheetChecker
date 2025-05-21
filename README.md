# VIPSamplesheetChecker
Small set of Python scripts to check your VIP Samplesheets with

## About
The VIP Samplesheet Checker is a set of Python scripts that can be used to check one or more samplesheets before you start running VIP. This makes it easier to check what might be a problem with the samplesheet.

*Requirements:*
- Python >= 3.10
- PrettyTable


## Running the vip_samplesheet_checker
The VIP Samplesheet Checker can be run in two different ways as described below.

### Running with `-r` and `-s`
The program can be run via: `python vip_samplesheet_checker.py -r vcf -s trio1.tsv trio2.tsv`. The `-r` parameter specifies the runmode you want to use the samplesheets for and valid values for this parameter are: “fastq”, “cram”, “gvcf” and “vcf”. One or more paths (separated by a space) to the samplesheets to check can be supplied with `-s`. Note that this mode is limited to one runmode.

### Running with `-i`
The program can also be run via: `python vip_samplesheet_checker.py -I infile.tsv`. The input file must be a tab separated file with two columns. The first column in this file should be a runmode, the second the path or paths to samplesheets. Paths to multiple samplesheets must be separated by a ‘,’.

_Note that running the program with `-i` takes precedent and any set `-r` and `-s` and will therefore be ignored._


## Output
Output from runs with the program are by default written to the console. The output consists of a table like the provided samplesheet being checked. The fields of this table are filled with either a checkmark if there is no problem with the field, or error mark if there is a problem with the field. All encounted problems will be noted beneath the table. Output for multiple samplesheets is separated by a line of ‘*’.

### Display table values (-p/--printvalues)
It is possible to not only print the checkmarks and error marks but also the value of each samplesheet field. This can be done by adding the -p or --printvalues parameter.

### Display info messages (-n/--show-info)
While checking the samplesheet, the program can also saves info message but does not show them by default. Use the -n or --show-info parameter to also display these infomessages.

### Write output files (-o/--outdir)
The program can also write the table and error and info messages to an output file if wanted. This can be done by indicating an output directory via the -o or --outdir parameter. The program will then write a file for each checked samplesheet, with the name ‘checked_’ followed by the samplesheet name.

### Divide samplesheet (-d/--divide-samplesheet)
It is also possible to divide the samplesheet by either family_id or project_id via the -d or --divide-samplesheet parameter. For each family_id or project_id a new samplesheet file will be written with the family_id or project_id as prefix.

### Correct samplesheet for non printable characters (-cn/--correct-nonprintable)
It is possible for a samplesheet to contain non printable characters. The program can remove these and write out a new samplesheet via the -cn or --correct-nonprintable parameter. The new output file will be prefixed with ‘corrected’ followed by the samplesheet name.
