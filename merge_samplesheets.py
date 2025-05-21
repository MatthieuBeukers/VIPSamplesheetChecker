import os
import re
import argparse
from pathlib import Path
from VIPSamplesheet import VIPSamplesheet
from VIPSamplesheetChecker import VIPSamplesheetChecker
from VIPSamplesheetSample2 import VIPSamplesheetSample2

GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS = ["individual_id"]
REQUIRED_SAMPLESHEET_COLUMNS = {
    "fastq": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["fastq", "fastq_r1", "fastq_r2"],
    "cram": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["cram"],
    "gvcf": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["gvcf"],
    "vcf": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["vcf"]
}


def get_parameters():
    """Returns the set command line parameters.
    
    Returns
    -------
    dict of str
        CLI parameter values
    """
    vipcss_args = argparse.ArgumentParser()
    vipcss_args.add_argument("-i", "--infiles", dest="infiles", nargs="+", help="Path to samplesheet to use as main sheet for merging", required=True)
    vipcss_args.add_argument("-o", "--outfile", dest="outfile", help="Path to write combined samplesheet to", required=True)
    vipcss_args.add_argument("-r", "--runmode", dest="runmode", choices=["fastq", "cram", "gvcf", "vcf"], help="Runmode the samplesheets will be used for", required=True)
    return vars(vipcss_args.parse_args())


def check_parameters(cliargs):
    """Checks that the parameters are ok.
    
    Parameters
    ----------
    cliargs : dict of str
        Set command line parameters
    
    Returns
    -------
    parameters_good : bool
        Indicates whether the set parameters are ok
    """
    parameters_good = True

    # Check infile parameter
    if len(cliargs["infiles"]) < 2:
        parameters_good = False
        print("Please provide at least two input files to combine")
    
    # Check the outfile parameter
    if not Path().is_dir():
        parameters_good = False
        print("Directory to write the output file to does not exist.")


def get_correct_infiles(infileslist):
    """Returns a list of correct input file to merge
    
    Parameters
    ----------
    infilelist : str
        List of paths to input files
    
    Returns
    -------
    correct_infiles : list of str
        List of paths to correct input files
    """
    correct_infiles = []
    for infile in infileslist:
        if Path(infile).is_file():
            if os.stat(infile).st_size == 0:
                print(f"Input file {infile} seems to be empty, therefore skipping this file")
            else:
                correct_infiles.append(infile)
        else:
            print(f"Could not find {infile}, therefore skipping this file")
    return correct_infiles


def header_cols_ok(vipchecker, runmode, vipsamplesheet):
    """Checks that the header columns in the samplesheet are ok.
    
    Returns
    -------
    boolean
        True if header columns are ok, False if not
    """
    missing_columns = vipchecker.check_header_fields(runmode, vipsamplesheet.get_header_fields())
    if len(missing_columns) > 0:
        print("[ERROR]: Missing required columns: ", end="")
        x = 0
        for mc in missing_columns:
            if x == len(missing_columns) - 1:
                print(f"{mc}")
            else:
                print(f"{mc}, ", end="")
            x += 1
        return False
    return True


def get_combined_header(samplesheets):
    """Creates and returns the header for the combined samplesheet.
    
    This header will contain the fields of all individual samplesheets.
    
    Parameters
    ----------
    samplesheets : dict
        Samplesheets to use to create the new header
    
    Returns
    -------
    combined_header : set of str
        New header line for the combined samplesheet
    """
    combined_header = set()
    for vipssheet in samplesheets:
        combined_header.update(vipssheet.get_header_fields())
    return list(combined_header)


def get_combined_header_v2(runmode, samplesheets):
    """Creates and returns the header for the combined samplesheet
    
    Parameters
    ----------
    runmode : str
        Specific runmode selected
    samplesheets : dict
        Samplesheets to use to create a combined header
    
    Returns
    -------
    combined_header : list of str
    """
    if runmode == "fastq":
        return get_combined_fastq_header(samplesheets)
    else:
        combined_header = set()
        for x in range(0, samplesheets):
            combined_header.update(samplesheets[x].get_header_fields())
        return list(combined_header)


def get_combined_fastq_header(samplesheets):
    """Creates a combined header for fastq runmode
    
    Parameters
    ----------
    samplesheets : dict
    
    Returns
    -------
    combined_header : list of str
        Combined fastq samplesheet header fields
    """
    single_fastq = False
    combined_header = set()
    
    # Check the first sheet
    combined_header.update(samplesheets[0].get_header_fields())
    if "fastq" in combined_header and "fastq_r1" not in combined_header:
        single_fastq = True
    
    # Create the combined header by merging the rest (checking for fastq fields)
    for x in range (1, len(samplesheets)):
        if single_fastq:
            if "fastq_r1" not in samplesheets[x].get_header_fields():
                combined_header.update(samplesheets[x].get_header_fields())
        else:
            if "fastq" not in samplesheets[x].get_header_fields():
                combined_header.update(samplesheets[x].get_header_fields())
    return list(combined_header)


def write_merged_samplesheet(vipsamplesheets, sheetheader, outfilepath):
    """Merges the supplied samplesheets and outputs a new samplesheet file.
    
    Parameters
    ----------
    vipsamplesheets : dict
        VIP samplesheets to combine
    sheetheader : list of str
        Header to use for the combined file
    outfilepath : str
        Path to write new combined samplesheet to
    """
    try:
        with open(outfilepath, "w") as outfile:
            outfile.write("\t".join(sheetheader) + "\n")
            for x in range (0, len(vipsamplesheets)):
                sheetsamples = vipsamplesheets[x].get_samplesheet_samples()
                for samplenum in sheetsamples:
                    outfile.write(f"{sheetsamples[samplenum].get_sampledata_as_filelinestr()}\n")
        return True
    except IOError:
        print("Could not write combined samplesheet.")
        return False


def merge_samplesheets(runmode, samplesheets, outfilepath):
    """Writes the merged samplesheet.
    
    Parameters
    ----------
    runmode : str
        Specific runmode to merge samplesheets for
    samplesheets : dict
        Dictionary with samplesheets to combine into one
    outfilepath : str
        Path to write combined samplesheet file to
    """
    headerline = get_combined_header_v2(runmode, samplesheets)
    wrote_mergedsheet = False
    
    if runmode == "fastq":
        wrote_mergedsheet = write_merged_fastq_samplesheet(samplesheets, headerline, outfilepath)
    else:
        wrote_mergedsheet = write_merged_samplesheet(samplesheets, headerline, outfilepath)
    return wrote_mergedsheet


def write_merged_fastq_samplesheet(vipsamplesheets, sheetheader, outfilepath):
    """Merges fastq runmode samplesheets.
    
    Parameters
    ----------
    vipsamplesheets : dict
        Dict of samplesheets to combine
    sheetheader : list of str
        New header to use for the combined samplesheet
    outfilepath : str
        Path to write output file to
    """
    single_fastq = False
    if "fastq" in sheetheader and "fastq_r1" not in sheetheader:
        single_fastq = True
    
    try:
        with open(outfilepath, "w") as outfile:
            outfile.write("\t".join(sheetheader))
            for x in range(0, len(vipsamplesheets)):
                if single_fastq:
                    if "fastq_r1" not in vipsamplesheets[x].get_header_fields():
                        sheetsamples = vipsamplesheets[x].get_samplesheet_samples()
                        for samplenum in sheetsamples:
                            outfile.write(f"{sheetsamples[samplenum].get_sampledata_as_filelinestr()}\n")
                        outfile.write()
                    else:
                        print(f"Could not combine samplesheet {vipsamplesheets[x].get_file_path()} due to differing fastq header fields.")
                else:
                    if "fastq" not in vipsamplesheet[x].get_header_fields():
                        sheetsamples = vipsamplesheets[x].get_samplesheet_samples()
                        for samplenum in sheetsamples:
                            outfile.write(f"{sheetsamples[samplenum].get_sampledata_as_filelinestr()}\n")
                        outfile.write()
                    else:
                        print(f"Could not combine samplesheet {vipsamplesheets[x].get_file_path()} due to differing fastq header fields.")
        return True
    except IOError:
        print("Could not write combined samplesheet")
        return False


def main():
    """Does the main work for merging the samplesheets."""
    # TODOs prior
    # 1. Get and check args
    cli_args = get_parameters()
    params_good = check_parameters(cli_args)
    
    if params_good:
        # 2. Get the valid input files
        usable_infiles = get_correct_infiles(cli_args["infiles"])
        
        if len(usable_infiles) > 1:
            # TODOs for the process
            # 1. Read the two or more samplesheets
            samplesheets = {}
            for x in range(0, len(usable_infiles)):
                samplesheet = VIPSamplesheet(usable_infiles[x])
                if samplesheet.file_was_read_succesfully():
                    if header_cols_ok(vip_checker, cli_args["runmode"], vip_samplesheet):
                        samplesheets[x] = VIPSamplesheet(usable_infiles[x])
            
            # Check that the number of successfully read and header correct files is stil two or more
            if len(samplesheets) > 1:
                # combined_header = get_combined_header()
                # combined_header = get_combined_header_v2(cli_args["runmode"], samplesheets)
                merge_successfull = merge_samplesheets(cli_args["runmode"], samplesheets, cli_args["outfile"])
                
                if merge_successfull:
                    print("Succesfully wrote combined samplesheet")
                else:
                    print("Writing combined samplesheet was not successful")
                
                # 2. Check that the header fields are compatible
                # 3. Create the new combined header based on the individual headers
                # 4. Merge the two or more samplesheets together
            else:
                print("Less than two valid input files were left so there is nothing to combine")
        else:
            print("Less than two valid input files were left so there is nothing to combine")


main()
