import sys
from pathlib import Path
import argparse
from prettytable import PrettyTable

from VIPSamplesheet import VIPSamplesheet
from VIPSamplesheetSample2 import VIPSamplesheetSample2
from VIPSamplesheetChecker import VIPSamplesheetChecker

def get_parameters():
    """Creates command line arguments for this script to make usage easier.
    
    It creates the following parameters:
    -r/--runmode: Used to specify the runmode the samplesheet(s) will be used for
    -s/--samplesheets: Path(s) to the samplesheet(s) to check
    -i/--infile: Path to a tab separated input file containing runmodes and samplesheets to check
    -o/--outdir: Path to a directory to write output files to
    -p/--printvalues: Flag to display the samplesheet values in the output table
    -n/--show-info: Flag to also display info messages found during check of the samplesheet(s)
    -cn/--correct-nonprintable: Flag to write new output samplesheet(s) stripped of non printable characters
    -d/--divide-samplesheet: Indicator to split samplesheet(s) on project_id or family_id
    
    Returns
    -------
    dict
        Argument parser values
    """
    vipssc = argparse.ArgumentParser()
    vipssc.add_argument("-r", "--runmode", dest="runmode", choices=["fastq", "cram", "gvcf", "vcf"], help="VIP runmode to check samplesheets for")
    vipssc.add_argument("-s", "--samplesheets", dest="samplesheets", nargs="+", help="Paths to one or more samplesheets to check")
    vipssc.add_argument("-i", "--infile", dest="infile", help="Path to tab separated file containing runmodes and paths to samplesheets")
    vipssc.add_argument("-o", "--outdir", dest="outdir", help="Path to output directory to write output files to")
    vipssc.add_argument("-p", "--printvalues", dest="printvalues", action="store_true", help="Also print values in the samplesheet")
    vipssc.add_argument("-n", "--show-info", dest="showinfo", action="store_true", help="Also print sample info messages")
    vipssc.add_argument("-cn", "--correct-nonprintable", dest="correctnonprintable", action="store_true", help="Correct samplesheet for non printable characters")
    vipssc.add_argument("-d", "--divide-samplesheet", dest="dividesamplesheet", choices=["family_id", "project_id"], help="Divide the samplesheet into multiple individual output samplesheet files")
    return vars(vipssc.parse_args())


def check_parameters(cliparameters):
    """Checks that the supplied CLI parameters are correct.
    
    Parameters
    ----------
    cliparameters : dict of str
        Set command line parameters
    """
    if cliparameters["infile"] is not None:
        if not Path(cliparameters["infile"]).is_file():
            print("Supplied input file is not a file.\n")
            usage()
            return False
        return True
    else:
        if cliparameters["runmode"] is None or cliparameters["samplesheets"] is None:
            usage()
            return False
        elif cliparameters["runmode"] not in ["fastq", "cram", "gvcf", "vcf"]:
            usage()
            return False
        return True


def check_parameters_v2(cliparameters):
    """Checks that the supplied CLI parameters are correct.
    
    Parameters
    ----------
    cliparameters : list of str
        Set command line parameters
    """
    if cliparameters["infile"] is not None:
        if not Path(cliparameters["infile"]).is_file():
            print("Supplied input file is not a file \n")
            usage()
            return False
        if cliparameters["outdir"] is not None:
            if not Path(cliparameters["outdir"]).is_dir():
                print("Supplied path to output directory is not a directory\n")
            usage()
            return False
        return True
    else:
        if cliparameters["runmode"] is None or cliparameters["samplesheets"] is None:
            usage()
            return False
        elif cliparameters["runmode"] not in ["fastq", "cram", "gvcf", "vcf"]:
            usage()
            return False
        
        if cliparameters["outdir"] is not None:
            if not Path(cliparameters["outdir"]).is_dir():
                print("Supplied path to output directory is not a directory\n")
                usage()
                return False
        return True


def read_infile(infilepath):
    """Reads the supplied infile with runmodes and paths to samplesheet files.
    
    Parameters
    ----------
    infilepath : str
        Path to the input file
    """
    runmodes_and_samplesheets = {}
    if Path(infilepath).is_file():
        try:
            with open(infilepath, "r") as infile:
                for fileline in infile:
                    filelinedata = fileline.strip().split("\t")
                    if filelinedata[0] not in runmodes_and_samplesheets:
                        runmodes_and_samplesheets[filelinedata[0]] = []
                    runmodes_and_samplesheets[filelinedata[0]].extend(filelinedata[1].split(","))
        except IOError:
            print(f"Could not read file {infilepath}")
    return runmodes_and_samplesheets


def usage():
    """Prints how to use the program.
    
    """
    # print("usage: python test.py fastq|cram|gvcf|vcf <samplesheets>")
    print("Usage: ")
    print("python test.py -r |fastq|cram|gvcf|vcf -s <samplesheets>")
    print("or")
    print("python test.py -i <infile.tsv>")


def header_cols_ok(vipchecker, runmode, vipsamplesheet):
    """Checks that the header columns in the samplesheet are ok.
    
    Returns
    -------
    boolean
        True if header columns are ok, False if not
    """
    missing_columns = vipchecker.check_header_fields(runmode, vipsamplesheet.get_header_fields())
    if len(missing_columns) > 0:
        print("\t[ERROR]: Missing required columns: ", end="")
        x = 0
        for mc in missing_columns:
            if x == len(missing_columns) - 1:
                print(f"{mc}")
            else:
                print(f"{mc}, ", end="")
            x += 1
        return False
    return True


def make_report_table(samplesheet):
    """
    """
    headerfields = samplesheet.get_header_fields()
    sheetsamples = samplesheet.get_samplesheet_samples()
    reporttable = PrettyTable(headerfields)
    
    for samplenum in range(1, len(sheetsamples)+1):
        tablerow = []
        for hf in headerfields:
            if sheetsamples[samplenum].field_has_errors(hf):
                tablerow.append("\u2718")
            else:
                tablerow.append("\u2714")
        reporttable.add_row(tablerow)
    return reporttable


def make_report_table_v2(samplesheet, printvalues):
    """Creates the report table indicating which columns are correct and which are not
    
    The report table has the same columns and rows as the input samplesheet.
    It also has rownumbers to make it easier to identify the fields in the actual samplesheet.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
        Samplesheet containing the samples
    """
    headerfields = samplesheet.get_header_fields()
    tableheaders = [""]
    tableheaders.extend(headerfields)
    sheetsamples = samplesheet.get_samplesheet_samples()
    reporttable = PrettyTable(tableheaders)
    
    # Loop over the samples (it uses range to ensure that sample are added in the correct linenumber order)
    for samplenum in range(1, len(sheetsamples)+1):
        tablerow = [samplenum]
        for hf in headerfields:
            if sheetsamples[samplenum].field_has_errors(hf):
                if printvalues:
                    tablerow.append("\u2718" + " " + sheetsamples[samplenum].get_datafield(hf))
                else:
                    tablerow.append("\u2718")
            else:
                if printvalues:
                    tablerow.append("\u2714" + " " + sheetsamples[samplenum].get_datafield(hf))
                else:
                    tablerow.append("\u2714")
        reporttable.add_row(tablerow)
    return reporttable


def print_samples_error_messsages(samplesheet):
    """Prints the error messages found in all samplesheet samples.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
        Samplesheet containing samples
    """
    sheetsamples = samplesheet.get_samplesheet_samples()
    for samplenum in sheetsamples:
        errormessages = sheetsamples[samplenum].get_sample_errors()
        if len(errormessages) > 0:
            print(f"Found problems for sample \"{sheetsamples[samplenum].get_individual_id()}\" on line {samplenum}:")
            for columnname in errormessages:
                for cermessage in errormessages[columnname]:
                    print(f"\t[{columnname}]: {cermessage}")
            print("")


def print_samplesheet_error_messages(samplesheet):
    """Prints the overall error messages found in the samplesheet.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
        Samplesheet containing the potential error messages to print
    """
    sheet_errors = samplesheet.get_samplesheet_errors()
    if len(sheet_errors) > 0:
        print("General errors found in the samplesheet:")
        for errortype in sheet_errors:
            for errormessage in sheet_errors[errortype]:
                print(f"\t[{errortype}]: {errormessage}")


def print_samples_info_messages(samplesheet):
    """Prints the info messages found in all samplesheet samples.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
        Samplesheet with info messages to print
    """
    sheetsamples = samplesheet.get_samplesheet_samples()
    for samplenum in sheetsamples:
        infomessages = sheetsamples[samplenum].get_sample_infos()
        if len(infomessages) > 0:
            print(f"Found the following notifications for sample {sheetsamples[samplenum].get_individual_id()} on line {samplenum}:")
            for columnname in infomessages:
                for infmessage in infomessages[columnname]:
                    print(f"\t[{columnname}]: {infmessage}")
            print("")


def print_samples_error_info_messages(samplesheet, displayinfo):
    """Prints the error and info messages found in all samplesheet samples.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
        Samplesheet with samples containing error and info messages to print
    displayinfo : bool
        Boolean indicating whether the samples info messages should be printed
    """
    sheetsamples = samplesheet.get_samplesheet_samples()
    for samplenum in sheetsamples:
        errormessages = sheetsamples[samplenum].get_sample_errors()
        infomessages = sheetsamples[samplenum].get_sample_infos()
        
        # Print the sample error messages
        if len(errormessages) > 0:
            print(f"Found problems for sample \"{sheetsamples[samplenum].get_individual_id()}\" on line {samplenum}:")
            for columnname in errormessages:
                for cermessage in errormessages[columnname]:
                    print(f"\t[{columnname}]: {cermessage}")
            print("")
        
        # Print the sample info messages
        if displayinfo and len(infomessages) > 0:
            print(f"Found the following notifications for sample {sheetsamples[samplenum].get_individual_id()} on line {samplenum}:")
            for columnname in infomessages:
                for infmessage in infomessages[columnname]:
                    print(f"\t[{columnname}]: {infmessage}")
            print("")


def write_output_file(pathtofile, samplesheet, reporttable, displayinfo):
    """Writes the output of a samplesheet check to an output file.
    
    Parameters
    ----------
    pathtofile : str
        Path to write output file to
    samplesheet : VIPSamplesheet
        Samplesheet to write report of
    reporttable : PrettyTable
        The report table to write to file
    """
    try:
        with open(pathtofile, "w") as outfile:
            outfile.write(str(reporttable))
            outfile.write("\n")
            
            # Write the sample error messages
            sheetsamples = samplesheet.get_samplesheet_samples()
            for samplenum in sheetsamples:
                errormessages = sheetsamples[samplenum].get_sample_errors()
                infomessages = sheetsamples[samplenum].get_sample_infos()
                
                # Write the error messages of the current sample
                if len(errormessages) > 0:
                    outfile.write(f"Found problems for sample \"{sheetsamples[samplenum].get_individual_id()}\" on line {samplenum}:\n")
                    for columnname in errormessages:
                        for cermessage in errormessages[columnname]:
                            outfile.write(f"\t[{columnname}]: {cermessage}\n")
                    outfile.write("\n")
                
                # Write the info messages of the current sample
                if displayinfo and len(infomessages) > 0:
                    outfile.write(f"Found the following notifications for sample {sheetsamples[samplenum].get_individual_id()} on line {samplenum}:\n")
                    for columnname in infomessages:
                        for infmessage in infomessages[columnname]:
                            outfile.write(f"\t[{columnname}]: {infmessage}\n")
                    outfile.write("\n")
            
            # Write the samplesheet error messages
            sheet_errors = samplesheet.get_samplesheet_errors()
            if len(sheet_errors) > 0:
                outfile.write("General errors found in the samplesheet:\n")
                for errortype in sheet_errors:
                    for errormessage in sheet_errors[errortype]:
                        outfile.write(f"\t[{errortype}]: {errormessage}\n")
    except IOError:
        print(f"Could not write to output file {pathtofile}")


def split_samplesheet(samplesheet, splitsheetby, outdir):
    """Splits a provided samplesheet by either family_id or project_id.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
    splitsheetby : str
        What column to split the samplesheet by (family_id or project_id)
    """
    splitbysampledata = {}
    if splitsheetby == "family_id":
        splitbysampledata = samplesheet.get_familyid_to_sample_list()
    else:
        splitbysampledata = samplesheet.get_projectid_to_sample_list()
    
    for splitbygroup in splitbysampledata:
        samplesheetfilename = samplesheet.get_file_path().split("/")[-1]
        outfilepath = f"{outdir}/{splitbygroup}_{samplesheetfilename}"
        write_sub_samplesheet(samplesheet, splitbysampledata[splitbygroup], outfilepath)


def write_sub_samplesheet(samplesheet, samplestowrite, outfilepath):
    """Writes a subset samplesheet to a file.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
        Samplesheet to write a sub section from to file
    samplestowrite : dict of str
        Line numbers of the samples to write to file
    outfilepath : str
        Path to write output file to
    """
    try:
        with open(outfilepath, "w") as subsamplesheetfile:
            subsamplesheetfile.write("\t".join(samplesheet.get_header_fields()) + "\n")
            for samplenum in samplestowrite:
                subsamplesheetfile.write(f"{samplesheet.get_sample_by_linenumber(samplenum).get_sampledata_as_filelinestr(samplesheet.get_header_fields())}\n")
    except IOError:
        print("Could not write sub samplesheet")


def correct_for_nonprintable_characters(samplesheet, outfilepath):
    """Rewrites the samplesheet to an output file with non printable characters removed.
    
    Parameters
    ----------
    samplesheet : VIPSamplesheet
        Samplesheet containing the sample data to write
    outfilepath : str
        Path to write corrected samplesheet to
    """
    try:
        with open(outfilepath, "w") as correctedoutfile:
            correctedoutfile.write("\t".join(samplesheet.get_header_fields()) + "\n")
            for x in range(1, samplesheet.get_number_of_samples()+1):
                correctedoutfile.write(f"{samplesheet.get_sample_by_linenumber(x).get_sampledata_as_filelinestr(samplesheet.get_header_fields())}\n")
    except IOError:
        print("[ERROR]: Could not write correct samplesheet file")


def main():
    """Does the actual work.
    
    The process has three steps.
    (1): Read and save the data as is
    (2): Check values for each sample and throughout the samplesheet
    (3): Make the report table and report found errors
    """
    cli_args = get_parameters()
    params_ok = check_parameters(cli_args)
    runmodes_samplesheets = {}
    
    # Only start doing work if the cli parameters are correct.
    if params_ok:
        if cli_args["infile"]:
            runmodes_samplesheets = read_infile(cli_args["infile"])
        else:
            runmodes_samplesheets[cli_args["runmode"]] = cli_args["samplesheets"]
        
        vip_checker = VIPSamplesheetChecker()
        for runmode in runmodes_samplesheets:
            # print(f"[INFO]: Checking samplesheets for runmode {runmode}")
            for samplesheetfile in runmodes_samplesheets[runmode]:
                print(f"[INFO]: Checking samplesheet \"{samplesheetfile}\" for runmode \'{runmode}\'")
                vip_samplesheet = VIPSamplesheet(samplesheetfile)
                if not vip_samplesheet.file_was_read_succesfully():
                    print(f"[INFO]: Skipping samplesheet {samplesheetfile}")
                else:
                    has_required_cols = header_cols_ok(vip_checker, runmode, vip_samplesheet)
                    if not has_required_cols:
                        print(f"Skipping samplesheet {samplesheetfile} due to missing required columns")
                    else:
                        # Check each sample in the samplesheet for errors
                        sheetsamples = vip_samplesheet.get_samplesheet_samples()
                        for samplenum in sheetsamples:
                            # print(f"[INFO]: Checking sample {sheetsamples[samplenum].get_individual_id()}")
                            vip_checker.check_sample_column_values(runmode, vip_samplesheet.get_header_fields(), vip_samplesheet, sheetsamples[samplenum])
                            #print("\n")
                        
                        # Check overall samplesheet errors
                        # vip_checker.check_sheet_consistency(vip_samplesheet)
                        # vip_checker.check_sheet_duplicate_individual_ids(vip_samplesheet)
                        # vip_checker.check_sheet_trios(vip_samplesheet)
                        vip_checker.check_sheet_sequencing_method_consistency(vip_samplesheet)
                        vip_checker.check_sheet_sequencing_platform_consistency(vip_samplesheet)
                        vip_checker.check_sheet_assembly_consistency(vip_samplesheet)
                        vip_checker.check_sheet_individualid_consistency(vip_samplesheet)
                        
                        # Start making the report
                        report_table = make_report_table_v2(vip_samplesheet, cli_args["printvalues"])
                        print(report_table)
                        # vip_samplesheet.display_all_sample_errors()
                        print_samplesheet_error_messages(vip_samplesheet)
                        print_samples_error_messsages(vip_samplesheet)
                        
                        if cli_args["showinfo"]:
                            print_samples_info_messages(vip_samplesheet)
                    
                        # Check whether to write to output file, if so do so
                        if cli_args["outdir"]:
                            outputfilepath = cli_args["outdir"] + "/checked_" + samplesheetfile.split("/")[-1]
                            write_output_file(outputfilepath, vip_samplesheet, report_table, cli_args["showinfo"])
                            print(f"Wrote output file with checks to: {outputfilepath}")
                        
                            if cli_args["dividesamplesheet"]:
                                print(f"Splitting samplesheet on {cli_args["dividesamplesheet"]}")
                                split_samplesheet(vip_samplesheet, cli_args["dividesamplesheet"], cli_args["outdir"])
                            
                            if cli_args["correctnonprintable"]:
                                print(f"Rewriting samplesheet {samplesheetfile} to remove non printable characters")
                                sheetfilename = samplesheetfile.split("/")[-1]
                                outfilepath = cli_args["outdir"] + "/corrected_" + sheetfilename
                                correct_for_nonprintable_characters(vip_samplesheet, outfilepath)
                        
                        print("")
                        print("**************************************************")
    

main()
