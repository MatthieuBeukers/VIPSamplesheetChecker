import os
import re
from pathlib import Path

class VIPSamplesheetChecker:
    GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS = ["individual_id"]
    REQUIRED_SAMPLESHEET_COLUMNS = {
        "fastq": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["fastq", "fastq_r1", "fastq_r2"],
        "cram": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["cram"],
        "gvcf": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["gvcf"],
        "vcf": GLOBAL_REQUIRED_SAMPLESHEET_COLUMNS + ["vcf"]
    }
    
    GLOBAL_OPTIONAL_SAMPLESHEET_COLUMNS = ["project_id", "family_id", "paternal_id", "maternal_id", "sex", "affected", "proband", "hpo_ids", "sequencing_method", "regions", "pcr_performed"]
    OPTIONAL_SAMPLE_SHEET_COLUMNS = {
        "fastq": GLOBAL_OPTIONAL_SAMPLESHEET_COLUMNS + ["adaptive_sampling", "sequencing_platform"],
        "cram": GLOBAL_OPTIONAL_SAMPLESHEET_COLUMNS + ["sequencing_platform"],
        "gvcf": GLOBAL_OPTIONAL_SAMPLESHEET_COLUMNS + ["assembly", "cram"],
        "vcf": GLOBAL_OPTIONAL_SAMPLESHEET_COLUMNS + ["assembly", "cram"]
    }
    
    VALID_COLUMN_VALUES = {
        "sex": ["male", "female", ""],
        "affected": ["true", "false", ""],
        "proband": ["true", "false", ""],
        "sequencing_method": ["WGS", "WES", ""],
        "sequencing_platform": ["illumina", "nanopore", "pacbio_hifi", ""],
        "assembly": ["GRCh37", "GRCh38", "T2T", ""],
        "pcr_performed": ["true", "false", ""]
    }
    
    VALID_FILE_EXTENSIONS = {
        "fastq": ["fastq", "fastq.gz", "fq", "fq.gz"],
        "bed": ["bed"],
        "cram": ["sam", "bam", "cram"],
        "gvcf": ["gvcf", "gvcf.gz", "gvcf.bgz", "vcf", "vcf.gz", "vcf.bgz", "bcf", "bcf.gz", "bcf.bgz"],
        "vcf": ["vcf", "vcf.gz", "vcf.bgz", "bcf", "bcf.gz", "bcf.bgz"]
    }
    
    DEFAULT_SEQPLATFORM_VALUES = {
        "fastq": "nanopore",
        "cram": "illumina",
        "gvcf": "",
        "vcf": ""
    }
    
    
    def check_sample_column_values(self, runmode, headerfields, samplesheet, samplesheetsample):
        """Checks all the values in the columns of a single samlpesheet sample.
        
        Parameters
        ----------
        runmode : str
            Specific runmode
        headerfields : list of str
            List of headerfields of the samplesheet
        samplesheet : VIPSamplesheet
            Samplesheet to check the colum values of
        samplesheetsample : VIPSamplesheetSample
            Specific samplesheet sample to check the values of
        """
        for hf in headerfields:
            match hf:
                case "individual_id":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_individual_id())
                    self.check_individual_id(samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_individual_id_raw())
                case "paternal_id":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_paternal_id_raw())
                    self.check_paternal(samplesheetsample, samplesheet.get_individual_ids())
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_paternal_id())
                case "maternal_id":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_maternal_id_raw())
                    self.check_maternal(samplesheetsample, samplesheet.get_individual_ids())
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_maternal_id())
                case "sex":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_sample_sex_raw())
                    self.check_sex_value(samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_sample_sex())
                case "affected":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_affected_raw())
                    self.check_affected_value(samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_affected())
                case "proband":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_proband_raw())
                    self.check_proband_value(samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_proband())
                case "sequencing_method":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_sequencing_method_raw())
                    self.check_sequencing_method_value(samplesheet, samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_sequencing_method())
                case "pcr_performed":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_pcr_performed_raw())
                    self.check_pcr_performed_value(samplesheet, samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_pcr_performed())
                case "sequencing_platform":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_sequencing_platform_raw())
                    self.check_sequencing_platform_value(runmode, samplesheet, samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_sequencing_platform())
                case "assembly":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_assembly_raw())
                    self.check_assembly_value(samplesheet, samplesheetsample)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_assembly())
                case "regions":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_bed_file_raw())
                    self.check_bed_file(samplesheetsample, hf)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_bed_file())
                case "fastq":
                    self.check_fastq_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_fastq_files_raw())
                    self.check_fastq_files(samplesheetsample, hf, samplesheetsample.get_fastq_files())
                case "fastq_r1":
                    self.check_fastq_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_fastq_r1_files_raw())
                    self.check_fastq_files(samplesheetsample, hf, samplesheetsample.get_fastq_r1_files())
                case "fastq_r2":
                    self.check_fastq_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_fastq_r2_files_raw())
                    self.check_fastq_files(samplesheetsample, hf, samplesheetsample.get_fastq_r2_files())
                case "cram":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_cram_file_raw())
                    self.check_cram_file(samplesheetsample, hf, runmode)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_cram_file())
                case "gvcf":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_gvcf_file_raw())
                    self.check_gvcf_file(samplesheetsample, hf, runmode)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_gvcf_file())
                case "vcf":
                    self.check_for_nonprintable_chars(samplesheetsample, hf, samplesheetsample.get_vcf_file_raw())
                    self.check_vcf_file(samplesheetsample, hf)
                    self.check_for_multiple_values(samplesheetsample, hf, samplesheetsample.get_vcf_file())
    
    
    # Checks whether the values for ('sequencing_method', 'sequencing_platform', 'assembly') are consistent across the samplesheet.
    def check_sheet_consistency(self, samplesheet):
        """Checks whether the samplesheet contains different values for columns that should only contain one.
        
        In specific, the columns for sequencing_method, sequencing_platform and assembly are checked. These
        columns should contain only one value per samplesheet (?).
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet with columns to check
        """
        if len(samplesheet.get_sheet_sequencing_methods()) > 1:
            print(samplesheet.get_sheet_sequencing_methods())
            samplesheet.add_samplesheet_error("sequencing_method", "Samplesheet contains multiple values for sequencing method.")
        if len(samplesheet.get_sheet_sequencing_platforms()) > 1:
            samplesheet.add_samplesheet_error("sequencing_platform", "Samplesheet contains multiple values for sequencing_platform.")
        if len(samplesheet.get_sheet_assemblies()) > 1:
            samplesheet.add_samplesheet_error("assembly", "Samplesheet contains multiple values for assembly.")
    
    
    def check_sheet_projectid_consistency(self, samplesheet, projectids_multi_value, columnname):
        """Checks the samplesheet for project_id column consistency.
        
        This means that it checks whether a column that should have only one value for
        project_id has indeed one value and adds sample error message if not.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet to check project_id consistency for
        projectids_multi_value : dict of str
            Field with multipe values for project_id
        columnname : str
            Name of the column to check for multiple values
        """
        if len(projectids_multi_value) > 0:
            sheetsamples = samplesheet.get_samplesheet_samples()
            projectid_to_sample = samplesheet.get_projectid_to_sample_list()
            for projid in projectids_multi_value:
                for samplenum in projectid_to_sample[projid]:
                    sheetsamples[samplenum].add_sample_error(columnname, f"There is more than one value for project \"{projid}\".")
    
    
    def check_sheet_sequencing_method_consistency(self, samplesheet):
        """Checks the samplesheet for sequencing_method consistency.
        
        In this case, it is checked that each project_id only has one value for
        the sequencing_method across its samples.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet to check
        """
        self.check_sheet_projectid_consistency(samplesheet, samplesheet.get_projectid_with_multiple_sequencing_method_values(), "sequencing_method")
    
    
    def check_sheet_sequencing_platform_consistency(self, samplesheet):
        """Checks the samplesheet for sequencing_platform consistency.
        
        In this case, it is checked that each project_id only has one value for
        the sequencing_platform across its samples.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet to check
        """
        self.check_sheet_projectid_consistency(samplesheet, samplesheet.get_projectid_with_multiple_sequencing_platform_values(), "sequencing_platform")
    
    
    def check_sheet_assembly_consistency(self, samplesheet):
        """Checks the samplesheet for assembly consistency
        
        In this case, it is checked that each project_id only has one value for
        the assembly across its samples.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet to check
        """
        self.check_sheet_projectid_consistency(samplesheet, samplesheet.get_projectid_with_multiple_assembly_values(), "assembly")
    
    
    def check_sheet_duplicate_individual_ids(self, samplesheet):
        """Checks whether a samplesheet contains duplicate individual_id values.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet to check
        """
        dupindivids = samplesheet.get_duplicate_individual_ids()
        if len(dupindivids) > 0:
            for individ in dupindivids:
                for samplenum in dupindivids[individ]:
                    sheetsample = samplesheet.get_sample_by_linenumber(samplenum)
                    sheetsample.add_sample_error("individual_id", f"Value \"{sheetsample.get_individual_id()}\" appears more than once in the samplesheet.")
                    # samplesheet.add_samplesheet_error("individual_id", f"Value for individual_id appears more than once in the samplesheet.")
    
    
    def check_sheet_trios(self, samplesheet):
        """Checks that families in the sample sheet has three members.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet containing the families
        """
        familyids = samplesheet.get_family_ids()
        for familyid in familyids:
            if len(familyids[familyid]) < 3:
                print(f"[ERROR]: Family with id {familyid} has less than three members.")
            elif len(familyids[familyid]) > 3:
                print(f"[ERROR]: Family with id {familyid} has more than three members.")
    
    
    def check_individual_id(self, sheetsample):
        """Checks whether the value for individual_id of a given sample is empty.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Sample for which to check the individual_id of
        """
        if sheetsample.get_individual_id() == "":
            sheetsample.add_sample_error("individual_id", "Value for individual_id cannot be empty.")
    
    
    def check_maternal(self, sheetsample, samplesheet_individuals):
        """Checks whether the set maternal_id of a sample is also present in the samplesheet as an individual_id.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Sample to check maternal_id of
        samplesheet_individuals : list of str
            List of all individual ids found in the samplesheet
        """
        maternalid = sheetsample.get_maternal_id()
        if maternalid != "":
            if maternalid not in samplesheet_individuals:
                sheetsample.add_sample_error("maternal_id", f"Maternal id \"{maternalid}\" was not found in the samplesheet as individual.")
    
    
    def check_paternal(self, sheetsample, samplesheet_individuals):
        """Checks whether the set paternal_id of a sample is also present in the samplesheet as an individual_id.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Sample to check paternal_id of
        samplesheet_individuals : list of str
            List of all individual ids found in the samplesheet
        """
        paternalid = sheetsample.get_paternal_id()
        if paternalid != "":
            if paternalid not in samplesheet_individuals:
                sheetsample.add_sample_error("paternal_id", f"Paternal id \"{paternalid}\" was not found in the samplesheet as individual.")
    
    
    def check_header_fields(self, runmode, headerfields):
        """Checks whether all required header fields are present in the samplesheet.
        
        Parameters
        ----------
        runmode : str
            Specific runmode to check header columns for
        headerfields : list of str
            List of header fields found in the samplesheet
        """
        missing_columns = {}
        if runmode == "fastq":
            missing_columns = self.check_fastq_header_fields(headerfields)
        else:
            missing_columns = set(VIPSamplesheetChecker.REQUIRED_SAMPLESHEET_COLUMNS[runmode]) - set(headerfields)
        return missing_columns
    
    
    def check_fastq_header_fields(self, headerfields):
        """Specifically checks whether all required header columns are present in the samplesheet if the runmode is fastq.
        
        This is because in fastq runmode either fastq or fastq_r1 and fastq_r2 are required.
        
        Parameters
        ----------
        headerfields : list of str
            List of header fields to perform fastq header check for
        """
        missing_columns = set(VIPSamplesheetChecker.REQUIRED_SAMPLESHEET_COLUMNS["fastq"]) - set(headerfields)
        if missing_columns == {"fastq"}:
            missing_columns = {}
        elif missing_columns == {"fastq_r1", "fastq_r2"}:
            missing_columns = {}
        return missing_columns
    
    
    def check_sex_value(self, sheetsample):
        """Checks if the set value for sex of a sample is valid.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample to check sex value for
        """
        sexvalue = sheetsample.get_sample_sex()
        if sexvalue not in VIPSamplesheetChecker.VALID_COLUMN_VALUES["sex"]:
            sheetsample.add_sample_error("sex", f"Assigned value for sex is incorrect. Please use one of the following values: {VIPSamplesheetChecker.VALID_COLUMN_VALUES["sex"]}")
        elif sexvalue == "":
            sheetsample.add_sample_info("sex", "No assigned value for sex, by default this sample will be treated as female.")
    
    
    def check_affected_value(self, sheetsample):
        """Checks if the set value for affected of a sample is valid.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample with an affected value
        """
        if sheetsample.get_affected() not in VIPSamplesheetChecker.VALID_COLUMN_VALUES["affected"]:
            sheetsample.add_sample_error("affected", f"Assigned value for affectede is incorrect. Please use one of the following values: {VIPSamplesheetChecker.VALID_COLUMN_VALUES["affected"]}")
    
    
    def check_proband_value(self, sheetsample):
        """Check if the set value for proband of a sample is valid.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample with a proband value
        """
        probandvalue = sheetsample.get_proband()
        if probandvalue not in VIPSamplesheetChecker.VALID_COLUMN_VALUES["proband"]:
            sheetsample.add_sample_error("proband", f"Assigned value is incorrect. Please use one of the following values: {VIPSamplesheetChecker.VALID_COLUMN_VALUES["proband"]}")
    
    
    def check_sequencing_method_value(self, samplesheet, sheetsample):
        """Checks if the set value for sequencing_method of a sample is valid.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet containing the sample
        sheetsample : VIPSamplesheetSample
            Samplesheet sample with a sequencing_method value
        """
        seqmethodvalue = sheetsample.get_sequencing_method()
        if seqmethodvalue not in VIPSamplesheetChecker.VALID_COLUMN_VALUES["sequencing_method"]:
            sheetsample.add_sample_error("sequencing_method", f"Assigned value is incorrect. Please use one of the following values: {VIPSamplesheetChecker.VALID_COLUMN_VALUES["sequencing_method"]}")
        elif seqmethodvalue == "":
            sheetsample.add_sample_info("sequencing_method", "No assigned value, will be WGS by default.")
        # samplesheet.add_sequencing_method(seqmethodvalue)
    
    
    def check_sequencing_platform_value(self, runmode, samplesheet, sheetsample):
        """Checks if the sample's value for sequencing_platform is correct.
        
        Parameters
        ----------
        runmode
        samplesheet : VIPSamplesheet
            Samplesheet containing the sample
        sheetsample : VIPSamplesheetSample
            Samplesheet sample containing the sequencing_platform value
        """
        seqplatformvalue = sheetsample.get_sequencing_platform()
        if seqplatformvalue not in VIPSamplesheetChecker.VALID_COLUMN_VALUES["sequencing_platform"]:
            sheetsample.add_sample_error("sequencing_platform", f"Assigned value is incorrect. Please supply one of the following values: {VIPSamplesheetChecker.VALID_COLUMN_VALUES["sequencing_platform"]}")
        elif seqplatformvalue.strip() == "":
            sheetsample.add_sample_info(f"No assigned value, will be {DEFAULT_SEQPLATFORM_VALUES[runmode]} by default.")
        # samplesheet.add_sequencing_platform(seqplatformvalue.strip())
    
    
    def check_assembly_value(self, samplesheet, sheetsample):
        """Checks if the sample's assembly value is valid.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet containing the sample
        sheetsample : VIPSamplesheetSample
            Samplesheet sample containing the assembly value
        """
        assemblyvalue = sheetsample.get_assembly()
        if assemblyvalue not in VIPSamplesheetChecker.VALID_COLUMN_VALUES["assembly"]:
            sheetsample.add_sample_error("assembly", f"Assigned value is incorrect. Please use one of the following values: {VIPSamplesheetChecker.VALID_COLUMN_VALUES["assembly"]}.")
        elif assemblyvalue == "":
            sheetsample.add_sample_info("assembly", "No assigned value, will be assumed to be GRCh38 by default.")
        # samplesheet.add_assembly(assemblyvalue)
    
    
    def check_pcr_performed_value(self, samplesheet, sheetsample):
        """Checks if the sample's pcr_performed value is valid.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet containing the sample
        sheetsample : VIPSamplesheetSample
            Samplesheet sample containing the pcr_peformed value
        """
        pcrperformedvalue = sheetsample.get_pcr_performed()
        if pcrperformedvalue not in VIPSamplesheetChecker.VALID_COLUMN_VALUES["pcr_performed"]:
            sheetsample.add_sample_error("pcr_performed", f"Assigned value is incorrect. Please use one of the following values: {VIPSamplesheetChecker.VALID_COLUMN_VALUES["pcr_performed"]}")
        elif pcrperformedvalue == "":
            sheetsample.add_sample_info("pcr_performed", "No assigned value, will be set to false by default.")
    
    
    def check_fastq_files(self, sheetsample, columnname, fastqfiles):
        """Checks whether the list of fastq files exist.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample containing the fastq files
        columnname : str
            Name of te column containing the fastq files
        fastqfiles : list of str
            List of fastq files to check
        """
        fastqfiles = fastqfiles.split(",")
        if len(fastqfiles) > 0:
            for fastqfile in fastqfiles:
                self.check_file_exists(sheetsample, columnname, "FASTQ", fastqfile, VIPSamplesheetChecker.VALID_FILE_EXTENSIONS["fastq"])
        else:
            sheetsample.add_sample_error(columnname, "There are no fastq files.")
    
    
    def check_bed_file(self, sheetsample, columnname):
        """Checks whether the provided BED file of a sample exists.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample with a BED file
        columnname : str
            Name of the samplesheet column containing the BED file
        """
        self.check_file_exists(sheetsample, columnname, "BED", sheetsample.get_bed_file(), VIPSamplesheetChecker.VALID_FILE_EXTENSIONS["bed"])
    
    
    def check_cram_file(self, sheetsample, columnname, runmode):
        """Checks whether the provided SAM/BAM/CRAM file of a sample exists.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample with a SAM/BAM/CRAM file
        columnname : str
            Name of the samplesheet column containing the CRAM file
        runmode : str
            Specific runmode to check the sample for
        """
        if runmode == "cram":
            self.check_file_exists(sheetsample, columnname, "SAM/BAM/CRAM", sheetsample.get_cram_file(), VIPSamplesheetChecker.VALID_FILE_EXTENSIONS["cram"])
        elif runmode != "cram" and sheetsample.get_cram_file() != "":
            self.check_file_exists(sheetsample, columnname, "SAM/BAM/CRAM", sheetsample.get_cram_file(), VIPSamplesheetChecker.VALID_FILE_EXTENSIONS["cram"])
    
    
    def check_gvcf_file(self, sheetsample, columnname, runmode):
        """Checks whether the provided GVCF of a sample file exists.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Sampelsheet sample with a GVCF file
        columnname : str
            Name of the samplesheet column containing the GVCF file
        runmode : str
            Specific runmode to check the sample for
        """
        if runmode == "gvcf":
            self.check_file_exists(sheetsample, columnname, "GVCF", sheetsample.get_gvcf_file(), VIPSamplesheetChecker.VALID_FILE_EXTENSIONS["gvcf"])
        elif runmode != "gvcf" and sheetsample.get_gvcf_file() != "":
            self.check_file_exists(sheetsample, columnname, "GVCF", sheetsample.get_gvcf_file(), VIPSamplesheetChecker.VALID_FILE_EXTENSIONS["gvcf"])
    
    
    def check_vcf_file(self, sheetsample, columnname):
        """Checks whether the provided VCF file of a sample exists.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample with a VCF file
        columnname : str
            Name of the samplesheet column containing the VCF file
        """
        self.check_file_exists(sheetsample, columnname, "VCF", sheetsample.get_vcf_file(), VIPSamplesheetChecker.VALID_FILE_EXTENSIONS["vcf"])
    
    
    def check_file_exists(self, sheetsample, columnname, filetype, filetocheck, fileexts):
        """Checks whether a supplied file exists.
        
        The filepath is checked whether the file exists or whether the path
        contains a bash variable (making it not possible to check).
        It is also checked whether the file is of the correct type via its extension.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample with a file to check
        columnname : str
            Name of the samplesheet column containing the file
        filetype : str
            Filetype (BED, CRAM, etc)
        filetocheck : str
            Path to the file to check
        fileexts : list of str
            List of valid file extensions
        """
        if "$" in filetocheck or "${" in filetocheck:
            sheetsample.add_sample_info(columnname, f"Path to {filetype} file \"{filetocheck}\" contains a bash variable and might exist but could not be checked.")
        elif not Path(filetocheck).is_file():
            sheetsample.add_sample_error(columnname, f"{filetype} file \"{filetocheck}\" does not exist.")
        elif Path(filetocheck).is_file():
            if os.stat(filetocheck).st_size == 0:
                sheetsample.add_sample_error(columnname, f"{filetype} file \"{filetocheck}\" has a size of 0 bytes.")
        #if filetocheck.split(".")[-1] not in fileexts or filetocheck.split(".")[-2] + "." + filetocheck.split(".")[-1] not in fileexts:
        #    print(f"{filetype} file \"{filetocheck}\" doesn't seem to be of the correct type.\n")
        if filetocheck.split(".")[-1] not in fileexts:
            if len(filetocheck.split(".")) > 2:
                if filetocheck.split(".")[-2] + "." + filetocheck.split(".")[-1] not in fileexts:
                    sheetsample.add_sample_error(columnname, f"{filetype} file \"{filetocheck}\" doesn't seem to be of the correct type.")
            else:
                sheetsample.add_sample_error(columnname, f"{filetype} file \"{filetocheck}\" doesn't seem to be of the correct type.")
    
    
    def check_for_multiple_values(self, sheetsample, columnname, columnvalue):
        """Checks a provided field in the samplesheet sample for multiple values separated by comma and space.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample that to check
        columnname : str
            Name of the column to check for multiple values
        columnvalue : str
            Specific column value to check for multiple values
        """
        self.check_multivalues_by_separator(",", sheetsample, columnname, columnvalue)
        self.check_multivalues_by_separator(" ", sheetsample, columnname, columnvalue)
    
    
    def check_multivalues_by_separator(self, separator, sheetsample, columnname, columnvalue):
        """Checks whether a field of a sample has multiple values based on a provided separator.
        
        Parameters
        ----------
        separator : str
            Separator to use to check for multiple values
        sheetsample : VIPSamplesheetSample
            Sample containing the value
        columnname : str
            Name of the column containing the value to check
        columnvalue : str
            Specific value to check
        """
        separated_values = columnvalue.split(separator)
        if len(separated_values) > 1:
            sheetsample.add_sample_error(columnname, f"Contains multiple values separated by {separator}.")
    
    
    def check_for_nonprintable_chars(self, sheetsample, columnname, columnvalue):
        """Check a provided value for non printable characters.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Samplesheet sample containing the value to check
        columnname : str
            Name of the samplesheet column containing the value
        columnvalue : str
            Specific value to check
        """
        if not columnvalue.isprintable():
            sheetsample.add_sample_error(columnname, f"Value {re.sub(r"[\x00-\x1f]", "", columnvalue.strip())} contains nonprintable characters and might cause unexpected things.")
            # print(f"[ERROR]: Value {re.sub(r"[\x00-\x1f]", "", columnvalue.strip())} for {columnname} contains nonprintable characters and might cause unexpected things.")
    
    # Check for number of columns per sample
    def check_number_of_columns(self, samplesheet):
        """
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet to check the number of columns for
        """
        num_of_headerfields = samplesheet.get_number_of_columns()
        samplesheetsamples = samplesheet.get_samplesheet_samples()
        for samplenum in samplesheetsamples:
            if num_of_headerfields > samplesheetsamples[samplenum].get_number_of_columns():
                print(f"[ERROR]: Sample {samplesheetsamples[samplenum].get_individual_id().strip()} fewer columns than the header.")
            elif num_of_headerfields < samplesheetsamples[samplenum].get_number_of_columns():
                print(f"[ERROR]: Sample {samplesheetsamples[samplenum].get_individual_id().strip()} more columns than the header.")
    
    
    def check_fastq_for_nonprintable_chars(self, sheetsample, columnname, fastqfiles):
        """Checks the fastq files in a sample for non printable characters.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Sample containing the fastq files
        columnname : str
            Name of the column containing the fastq files
        """
        for fqfile in fastqfiles:
            if not fqfile.isprintable():
                sheetsample.add_sample_error(columnname, f"Path to FASTQ file {re.sub(r"[\x00-\x1f]", "", fqfile.strip())} contains nonprintable characters and might cause unexpected things.")
    
    
    def check_sheet_individualid_consistency(self, samplesheet):
        """Checks if there are duplicate individual_ids per project_id and adds error messages.
        
        Parameters
        ----------
        samplesheet : VIPSamplesheet
            Samplesheet containing the samplesheet data
        """
        sheetsamples = samplesheet.get_samplesheet_samples()
        dupindivids = samplesheet.get_project_duplicate_individualids()
        projectids_samplenums = samplesheet.get_projectid_to_sample_list()
        
        for projid in dupindivids:
            for samplenum in projectids_samplenums[projid]:
                if sheetsamples[samplenum].get_datafield("individual_id") in dupindivids[projid]:
                    sheetsamples[samplenum].add_sample_error("individual_id", f"Individual ID {sheetsamples[samplenum].get_datafield("individual_id")} occurs more than once for project_id {projid}")
    
    
