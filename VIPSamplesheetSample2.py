import re

class VIPSamplesheetSample2:
    def __init__(self):
        self.number_of_columns = 0
        self.sampledata = {}
        self.sample_affected = False
        self.is_proband = False
        self.pcr_is_performed = False
        self.hpo_ids = {}
        self.sample_errors = {}
        self.sample_info = {}
    
    
    def get_data(self):
        """Returns all saved sample data.
        
        Returns
        -------
        self.sampledata : dict of str
            Saved sample data per column name
        """
        return self.sampledata
    
    
    def has_datafield(self, headerfield):
        """Returns whether a certain datafield is present.
        
        Parameters
        ----------
        headerfield : str
            Column name to check
        """
        return headerfield in self.sampledata
    
    
    def get_datafield(self, headerfield):
        """Returns the data for the specified column. Will return None if not available.
        
        Parameters
        ----------
        headerfield : str
            Column name indicating which data to get
        """
        if headerfield in self.sampledata:
            return re.sub(r"[\x00-\x1f]", "", self.sampledata[headerfield])
        return None
    
    
    def get_datafield_raw(self, headerfield):
        """Returns the data for the specified column. Will return None if not available.
        
        Parameters
        ----------
        headerfield : str
            Column name indicating which data to get
        """
        if headerfield in self.sampledata:
            return self.sampledata[headerfield]
        return None
    
    
    def get_number_of_columns(self):
        """Returns the number of columns the sample has.
        
        Returns
        -------
        self.number_of_columns : int
            The number of columns the sample has
        """
        return self.number_of_columns
    
    
    def set_number_of_columns(self, numofcols):
        """Sets the number of samplesheet columns the sample has.
        
        Parameters
        ----------
        numofcols : int
            The number of columns
        """
        self.number_of_columns = numofcols
    
    
    def get_project_id(self):
        """Returns the saved project_id stripped of non printable characters.
        
        Returns
        -------
        str
            self.project_id stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["project_id"].strip())
    
    
    def get_project_id_raw(self):
        """Returns the saved project_id as is (potentially with non printable characters).
        
        Returns
        -------
        self.project_id : str
            Project ID as is.
        """
        return self.sampledata["project_id"]
    
    
    def set_project_id(self, projectid):
        """Saves the supplied sample project id.
        
        Parameters
        ----------
        projectid : str
            Project ID to save
        """
        self.sampledata["project_id"] = projectid
    
    
    def get_family_id(self):
        """Returns the saved family id stripped of non printable characters.
        
        Returns
        -------
        str
            self.family_id stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["family_id"].strip())
    
    
    def get_family_id_raw(self):
        """Returns the saved family_id as is (potentially with non printable characters).
        
        Returns
        -------
        self.family_id : str
            Family ID as is.
        """
        return self.sampledata["family_id"]
    
    
    def set_family_id(self, famid):
        """Saves the supplied family_id.
        
        Parameters
        ----------
        famid : str
            Family ID to save
        """
        self.sampledata["family_id"] = famid
    
    
    def get_individual_id(self):
        """Returns the saved individual_id stripped of non printable characters.
        
        Returns
        -------
        str
            Saved individual_id stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["individual_id"].strip())
    
    
    def get_individual_id_raw(self):
        """Returns the saved individual_id as is (potentially with non printable characters).
        
        Returns
        -------
        self.individual_id : str
            Saved individual_id as is
        """
        return self.sampledata["individual_id"]
    
    
    def set_individual_id(self, individualid):
        """Saves the supplied individual id.
        
        Parameters
        ----------
        individualid : str
            Individual ID to save
        """
        self.sampledata["individual_id"] = individualid
    
    
    def get_paternal_id(self):
        """Returns the saved paternal id stripped of non printable characters.
        
        Returns
        -------
        str
            Saved paternal_id stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["paternal_id"].strip())
    
    
    def get_paternal_id_raw(self):
        """Returns the saved paternal_id as is (potentially with non printable characters).
        
        Returns
        -------
        self.paternal_id : str
            Saved paternal_id as is
        """
        return self.sampledata["paternal_id"]
    
    
    def set_paternal_id(self, patid):
        """Saves the supplied paternal id.
        
        Parameters
        ----------
        patid : str
            Paternal ID to save
        """
        self.sampledata["paternal_id"] = patid
    
    
    def get_maternal_id(self):
        """Returns the saved maternal id stripped of non printable characters.
        
        Returns
        -------
        str
            Saved maternal_id stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["maternal_id"].strip())
    
    
    def get_maternal_id_raw(self):
        """Returns the saved maternal_id as is (potentially with non printable characters).
        
        Returns
        -------
        self.maternal_id : str
            Saved maternal_id as is
        """
        return self.sampledata["maternal_id"]
    
    
    def set_maternal_id(self, matid):
        """Saves the supplied maternal_id
        
        Parameters
        ----------
        matid : str
            Maternal ID to save
        """
        self.sampledata["maternal_id"] = matid
    
    
    def get_sample_sex(self):
        """Returns the saved sample sex stripped of non printable characters.
        
        Returns
        -------
        str
            Saved sample sex stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["sex"].strip())
    
    
    def get_sample_sex_raw(self):
        """Returns the saved sample sex as is
        
        Returns
        -------
        self.sample_sex : str
            Saved sample sex as is
        """
        return self.sampledata["sex"]
    
    
    def set_sample_sex(self, samplesex):
        """Saves the supplied sample sex.
        
        Parameters
        ----------
        sex : str
            Sample sex to save
        """
        self.sampledata["sex"] = samplesex
    
    
    def get_affected(self):
        """Returns the saved affected status stripped of non printable characters.
        
        Returns
        -------
        str
            Saved affected status stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["affected"].strip())
    
    
    def get_affected_raw(self):
        """Returns the affected status as is (potentially with non printable characters)
        
        Returns
        -------
        self.affected : str
            Saved affected status
        """
        return self.sampledata["affected"]
    
    
    def is_affected(self):
        """Returns boolean representation whether the sample has an affected status.
        
        Returns
        -------
        self.sample_affected : bool
            Whether the sample has affected status or not
        """
        return self.sample_affected
    
    
    def set_affected(self, aff):
        """Saves the supplied affected status.
        Parameters
        ----------
        aff : str
            Affected status to save
        """
        self.sampledata["affected"] = aff
    
    
    def set_is_affected(self):
        """Sets the boolean for affected status to true."""
        self.sample_affected = True
    
    
    def get_proband(self):
        """Returns the saved proband status stripped of non printable characters.
        
        Returns
        -------
        str
            Saved proband status stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["proband"].strip())
    
    
    def get_proband_raw(self):
        """Returns the saved proband status as is (potentially with non printable characters)
        
        Returns
        -------
        self.proband : str
            
        """
        return self.sampledata["proband"]
    
    
    def is_proband(self):
        """Returns whether the sample is a proband.
        
        Returns
        -------
        self.is_proband : bool
            Whether the sample is a proband
        """
        return self.is_proband
    
    
    def set_proband(self, proba):
        """Saves the supplied proband value.
        
        Parameters
        ----------
        proba : str
            Proband status to save
        """
        self.sampledata["proband"] = proba
    
    
    def set_is_proband(self):
        """Sets the boolean for proband to true"""
        self.is_proband = True
    
    
    def get_hpo(self):
        """Returns the HPO terms stripped of non printable characters.
        
        Returns
        -------
        str
            HPO terms stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["hpo_ids"].strip())
    
    
    def get_hpo_raw(self):
        """Returns the save HPPO terms as is (potentially with non pintable characters)
        
        Returns
        -------
        str
            HPO terms as is
        """
        return self.sampledata["hpo_ids"]
    
    
    def set_hpo(self, hpostr):
        """Saves the supplied HPO terms.
        
        Parameters
        ----------
        hpostr : str
            HPO terms to save
        """
        self.sampledata["hpo_ids"] = hpostr
    
    
    def get_hpo_ids(self):
        """Returns the set of split HPO terms.
        
        Returns
        -------
        self.hpo_ids
        """
        return self.hpo_ids
    
    
    def set_hpo_ids(self, hpoids):
        """Saves the supplied hpo ids.
        
        Parameters
        ----------
        hpoids : dict of str
            Split HPO terms
        """
        self.hpo_ids = hpoids
    
    
    def get_sequencing_method(self):
        """Returns the saved sequencing method stripped of non printable characters.
        
        Returns
        -------
        str
            Sequencing method stripped of potential non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["sequencing_method"].strip())
    
    
    def get_sequencing_method_raw(self):
        """Returns the saved sequencing method as is.
        
        Returns
        -------
        str
            Saved sequencing method as is (potentially with non printable characters)
        """
        return self.sampledata["sequencing_method"]
    
    
    def set_sequencing_method(self, seqmethod):
        """Saves the supplied sequencing method.
        
        Parameters
        ----------
        seqmethod : str
            Sequencing method to save
        """
        self.sampledata["sequencing_method"] = seqmethod
    
    
    def get_pcr_performed(self):
        """Returns the saved pcr_performed value stripped of non printable characters.
        
        Returns
        -------
        str
            Saved pcr performed value stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["pcr_performed"])
    
    
    def get_pcr_performed_raw(self):
        """Returns the saved pcr_performed value as is (potentially with non printable characters).
        
        Returns
        -------
        str
            Saved pcr_performed value as is
        """
        return self.sampledata["pcr_performed"]
    
    
    def get_pcr_is_performed(self):
        """Returns whether the pcr_performed value is set to true.
        
        Returns
        -------
        self.pcr_is_performed : bool
            Whether the pcf_performed is set to true
        """
        return self.pcr_is_performed
    
    
    def set_pcr_performed(self, pcrperformed):
        """Saves the supplied prc performed value.
        
        Parameters
        ----------
        pcrperformed : str
            pcr_performed status to save
        """
        self.sampledata["pcr_performed"] = pcrperformed
    
    
    def set_pcr_is_performed(self):
        """Sets the pcr_performed status to true."""
        self.pcr_is_performed = True
    
    
    def get_bed_file(self):
        """Returns the saved BED file stripped of non printable characters.
        
        Returns
        -------
        str
            Path to BED file stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["regions"].strip())
    
    
    def get_bed_file_raw(self):
        """Returns the saved path to the BED file as is (potentially with non printable characters)\
        
        Returns
        -------
        str
            Path to the saved BED file
        """
        return self.sampledata["regions"]
    
    
    def set_bed_file(self, bedfile):
        """Saves the supplied path to the BED file.
        
        Parameters
        ----------
        bedfile : str
            Path to the BED file to save
        """
        self.sampledata["regions"] = bedfile
    
    
    def get_adaptive_sampling(self):
        """Returns the saved adaptive_sampling value stripped of non printable characters.
        
        Returns
        -------
        str
            Adaptive sampling value stripped of non printable characters
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["adaptive_sampling"].strip())
    
    
    def get_adaptive_sampling_raw(self):
        """Returns the saved adaptive_sampling value as is.
        
        Returns
        -------
        str
            Saved adaptive_sampling value as is
        """
        return self.sampledata["adaptive_sampling"]
    
    
    def set_adaptive_sampling(self, adsampling):
        """Saves the supplied adaptive_sampling value.
        
        Parameters
        ----------
        adsampling : str
            The adaptive_sampling value to save
        """
        self.sampledata["adaptive_sampling"] = adsampling
    
    
    def get_fastq_files(self):
        """Returns the saved paths to fastq files as string stripped of non printable characters.
        
        Returns
        -------
        str
            Paths to fastq files as string
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["fastq"])
        # return [re.sub(r"[\x00-\x1f]", "", x.strip()) for x in self.sampledata["fastq"]]
    
    
    def get_fastq_files_raw(self):
        """Returns the paths to the fastq files as string as is (potentially with non printable characters).
        
        Returns
        -------
        str
            Paths to fastq files as string
        """
        return self.sampledata["fastq"]
    
    
    def set_fastq_files(self, fastqfiles):
        """Saves the supplied paths to fastq files.
        
        Parameters
        ----------
        fastqfiles : str
            Paths to fastq files as string
        """
        self.sampledata["fastq"] = fastqfiles
    
    
    def get_fastq_r1_files(self):
        """Returns the saved paths to fastq r1 files stripped of non printable characters.
        
        Returns
        -------
        str
            Paths to fastq r1 files as string
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["fastq_r1"])
        # return [re.sub(r"[\x00-\x1f]", "", x.strip()) for x in self.sampledata["fastq_r1"]]
    
    
    def get_fastq_r1_files_raw(self):
        """Returns the paths to the saved fastq r1 files as is (potentially with non printable characters).
        
        Returns
        -------
        str
            Paths to fastq r1 files as string
        """
        return self.sampledata["fastq_r1"]
    
    
    def set_fastq_r1_files(self, r1files):
        """Saves the paths to the supplied fastq r1 files.
        
        Parameters
        ----------
        str
            Paths to the fastq r1 files as string
        """
        self.sampledata["fastq_r1"] = r1files
    
    
    def get_fastq_r2_files(self):
        """Returns the saved paths to the fastq r2 files as string stripped of non printable characters.
        
        Returns
        -------
        str
            Paths to the fastq r2 files as string
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["fastq_r2"])
        # return [re.sub(r"[\x00-\x1f]", "", x.strip()) for x in self.sampledata["fastq_r2"]]
    
    
    def get_fastq_r2_files_raw(self):
        """Returns the saved paths to the fastq r2 files as string as is (potentially with non printable characters). 
        
        Returns
        -------
        str
            Paths to the fastq r2 files as string as is
        """
        return self.sampledata["fastq_r2"]
    
    
    def set_fastq_r2_files(self, r2files):
        """Saves the supplied paths to the fastq r2 files as string.
        
        Parameters
        ----------
        r2files : str
            Paths to the fastq r2 files as string
        """
        self.sampledata["fastq_r2"] = r2files
    
    
    def get_sequencing_platform(self):
        """Returns the saved value for sequencing_platform stripped of non printable characters.
        
        Returns
        -------
        str
            The value for sequencing_platform
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["sequencing_platform"].strip())
    
    
    def get_sequencing_platform_raw(self):
        """Returns the saved value for sequencing_platform as is (potentially with non printable characters).
        
        Parameters
        ----------
        str
            Saved value for sequencing_platform as is
        """
        return self.sampledata["sequencing_platform"]
    
    
    def set_sequencing_platform(self, seqplatform):
        """Saves the supplied value for sequencing_platform.
        
        Parameters
        ----------
        seqplatform : str
            Value for sequencing_platform to save
        """
        self.sampledata["sequencing_platform"] = seqplatform
    
    
    def get_cram_file(self):
        """Returns the saved path to the CRAM file stripped of non printable characters.
        
        Returns
        -------
        str
            Saved path to the CRAM file
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["cram"].strip())
    
    
    def get_cram_file_raw(self):
        """Returns the saved path to the CRAM file as is (potentially with non printable characters).
        
        Returns
        -------
        str
            Saved path to the CRAM file
        """
        return self.sampledata["cram"]
    
    
    def set_cram_file(self, cramfile):
        """Saves the supplied path to the CRAM file.
        
        Parameters
        ----------
        cramfile : str
            Path to the CRAM file to save
        """
        self.sampledata["cram"] = cramfile
    
    
    def get_assembly(self):
        """Returns the saved assembly value stripped of non printable characters.
        
        Returns
        -------
        str
            Saved assembly value
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["assembly"].strip())
    
    
    def get_assembly_raw(self):
        """Returns the saved assembly value as is (potentially with non printable characters).
        
        Returns
        -------
        str
            Saves assembly value
        """
        return self.sampledata["assembly"]
    
    
    def set_assembly(self, assem):
        """Saves the supplied assembly value.
        
        Parameters
        ----------
        assem : str
            Value for assembly to save
        """
        self.sampledata["assembly"] = assem
    
    
    def get_gvcf_file(self):
        """Returns the saved path to the GVCF file stripped of non printable characters.
        
        Returns
        -------
        str
            Saves path to the GVCF file
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["gvcf"].strip())
    
    
    def get_gvcf_file_raw(self):
        """Returns the saved path to the GVCF file as is (potentially with non printable characters).
        
        Returns
        -------
        str
            Saved path to the GVCF file
        """
        return self.sampledata["gvcf"]
    
    
    def set_gvcf_file(self, gvcffile):
        """Saves the supplied path to the GVCF file.
        
        Parameters
        ----------
        gvcffile : str
            Path to the GVCF file
        """
        self.sampledata["gvcf"] = gvcffile
    
    
    def get_vcf_file(self):
        """Returns the saved path to the VCF file stripped of non printable characters.
        
        Returns
        -------
        str
            Saved path to the VCF file
        """
        return re.sub(r"[\x00-\x1f]", "", self.sampledata["vcf"].strip())
    
    
    def get_vcf_file_raw(self):
        """Returns the saved path to the VCF file as is (potentially with non printable characters).
        
        Returns
        -------
        str
            Saved path to the VCF file 
        """
        return self.sampledata["vcf"]
    
    
    def set_vcf_file(self, vcffile):
        """Sets the pat
        
        Parameters
        ----------
        vcffile : str
            
        """
        self.sampledata["vcf"] = vcffile
    
    
    def add_sample_error(self, columnname, errormessage):
        """Add an error message for a column.
        
        Parameters
        ----------
        columnname : str
            Name of the column where the error occured
        errormessage : str
            The error message to save
        """
        if columnname not in self.sample_errors:
            self.sample_errors[columnname] = []
        self.sample_errors[columnname].append(errormessage)
    
    
    def get_sample_errors(self):
        """Returns the dictionary with all sample errors.
        
        Returns
        -------
        self.sample_errors : dict of str
            Dictionary containing the sample errors per column name
        """
        return self.sample_errors
    
    
    def get_sample_column_errors(self, columnname):
        """Returns the error messages of the sample for a specified column.
        
        If the columnname had no error for the sample (and can therefore not be found)
        an empty list will be returned.
        
        Parameters
        ----------
        columnname : str
            Name of the samplesheet column to get the error messages for.
        
        Returns
        -------
        list of str
            List of error messages for the column
        """
        if columnname in self.sample_errors:
            return self.sample_errors[columnname]
        return []
    
    
    def add_sample_info(self, columnname, infomessage):
        """Adds the supplied information message.
        
        Parameters
        ----------
        columnname : str
            Name of the column where the info message occured
        infomessage : str
            THe infomessage to save
        """
        if columnname not in self.sample_info:
            self.sample_info[columnname] = []
        self.sample_info[columnname].append(infomessage)
    
    
    def get_sample_infos(self):
        """Returns all sample info messages.
        
        Returns
        -------
        self.sample_info : dict of str
            Info messages of the sample
        """
        return self.sample_info
    
    
    def get_sample_column_infos(self, columnname):
        """Get all info messages of this sample for a specified column.
        
        Parameters
        ----------
        columnname : str
            Name of the column 
        
        Returns
        -------
        list of str
            Info messages for a specified column
        """
        if columnname in self.sample_info:
            return self.sample_info[columnname]
        return []
    
    
    def field_has_errors(self, columnname):
        """Checks whether a supplied column has an error for this sample.
        
        Parameters
        ----------
        columnname : str
            Name of the column to check
        
        Returns
        -------
        bool
            True if sample has one or more errors in the supplied column, False if not
        """
        return columnname in self.sample_errors
    
    
    def field_has_info(self, columnname):
        """Returns whether this sample has one or more info messages for a specified samplesheet column.
        
        Parameters
        ----------
        columnname : str
            Name of the column to check for info messages
        """
        return columnname in self.sample_info
    
    
    def get_sampledata_as_filelinestr(self, headerfields):
        """Returns the requested sample data as a file line.
        
        The requested data is specified by the list of header fields.
        
        Parameters
        ----------
        headerfields : list of str
            List of samplesheet column headers specifying which data to get
        
        Returns
        -------
        sampledatastr : str
            Sample data as a file line
        """
        sampledatastr = ""
        x = 0
        for hf in headerfields:
            if hf in self.sampledata:
                sampledatastr += f"{self.get_datafield(hf)}"
            else:
                sampledatastr += ""
            if x < len(headerfields) -1:
                sampledatastr += "\t"
            x += 1
        return sampledatastr
