import re
from pathlib import Path
# from VIPSamplesheetSample import VIPSamplesheetSample
from VIPSamplesheetSample2 import VIPSamplesheetSample2

class VIPSamplesheet:
    def __init__(self, path_to_samplesheet):
        """Intializes several variables with default values reads the file.
        
        To read the samplesheet file the method read_samplesheet() is called.
        
        Parameters
        ----------
        path_to_samplesheet : str
            Path to the samplesheet file to read
        """
        self.file_path = path_to_samplesheet
        self.headerfields = []
        self.samplesheet_data = {}
        self.incorrect_files = []
        self.individuals = {}
        self.project_sequencing_methods = {}
        self.project_sequencing_platforms = {}
        self.project_assemblies = {}
        self.project_individualids = {}
        self.samplesheet_errors = {}
        self.projectid_to_samples = {}
        self.read_file = self.read_samplesheet(path_to_samplesheet)
    
    
    def read_samplesheet(self, samplesheet_file):
        """Reads the provided samplesheet file.
        
        Parameters
        ----------
        samplesheet_file : str
            Path to the samplesheet file to read
        
        Returns
        -------
        boolean
            Indicates whether reading the file was succesfull
        """
        headerdata = []
        header = True
        sample_num = 1
        
        has_project_id = False
        project_id_index = None
        
        if Path(samplesheet_file).is_file():
            try:
                with open(samplesheet_file, 'r') as samplesheet:
                    for fileline in samplesheet:
                        if header:
                            headerdata = fileline.strip().split("\t")
                            for headercol in headerdata:
                                self.headerfields.append(headercol)
                            has_project_id = "project_id" in self.headerfields
                            if has_project_id:
                                project_id_index = self.headerfields.index("project_id")
                            header = False
                        else:
                            if not has_project_id:
                                self.add_projectid_to_sample("vip", sample_num)
                            filelinedata = fileline.strip().split("\t")
                            self.samplesheet_data[sample_num] = self.make_vip_sample(headerdata, filelinedata, sample_num, has_project_id, project_id_index)
                            # self.samplesheet_data[filelinedata[self.headerfields.index("individual_id")]] = make_vip_sample(filelinedata)
                            # if self.samplesheet_data[sample_num].has_datafield("individual_id"):
                                # self.add_individualid(self.samplesheet_data[sample_num].get_individual_id(), sample_num)
                            sample_num += 1
                        
            except IOError:
                print("[ERROR]: Could not read samplesheet.")
                return False
        else:
            print("[ERROR]: Samplesheet not found.\n")
            return False
        return True
    
    
    def make_vip_sample(self, headerdata, filelinedata, samplenum, hasprojectid, projectidindex):
        """Makes a samplesheet sample from one samplesheet row.
        
        The list of header columns is used to determine which data 
        the sample contains and should be saved.
        
        Parameters
        ----------
        headerdata : list of str
            List of header columns in the samplesheet
        filelinedata : list of str
            List of values of one samplesheet row
        samplenum : int
            The linenumber of the row to construct a sample from
        
        Returns
        -------
        vipsample : VIPSamplesheetSample
            VIP samplesheet sample with saved data
        """
        vipsample = VIPSamplesheetSample2()
        vipsample.set_number_of_columns(len(filelinedata))
        self.check_number_of_columns(len(headerdata), len(filelinedata), samplenum)
        
        lineindex = 0
        for headerfield in headerdata:
            try:
                match headerfield:
                    case "project_id":
                        vipsample.set_project_id(filelinedata[lineindex])
                        self.add_projectid_to_sample(filelinedata[lineindex], samplenum)
                    case "family_id":
                        vipsample.set_family_id(filelinedata[lineindex])
                    case "individual_id":
                        vipsample.set_individual_id(filelinedata[lineindex])
                        if hasprojectid:
                            self.add_projectid_to_individualid(filelinedata[projectidindex], re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                        else:
                            self.add_projectid_to_individualid("vip", re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                    case "paternal_id":
                        vipsample.set_paternal_id(filelinedata[lineindex])
                    case "maternal_id":
                        vipsample.set_maternal_id(filelinedata[lineindex])
                    case "sex":
                        vipsample.set_sample_sex(filelinedata[lineindex])
                    case "affected":
                        vipsample.set_affected(filelinedata[lineindex])
                        if re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()) == "true":
                            vipsample.set_is_affected()
                    case "proband":
                        vipsample.set_proband(filelinedata[lineindex])
                        if re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()) == "true":
                            vipsample.set_is_proband()
                    case "hpo_ids":
                        vipsample.set_hpo(filelinedata[lineindex])
                        vipsample.set_hpo_ids(self.get_hpo_terms(re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip())))
                    case "sequencing_method":
                        vipsample.set_sequencing_method(filelinedata[lineindex])
                        if hasprojectid:
                            self.add_sequencing_method(filelinedata[projectidindex], re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                        else:
                            self.add_sequencing_method("vip", re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                    case "regions":
                        vipsample.set_bed_file(filelinedata[lineindex])
                    case "adaptive_sampling":
                        vipsample.set_adaptive_sampling(filelinedata[lineindex])
                    case "fastq":
                        vipsample.set_fastq_files(filelinedata[lineindex])
                        # vipsample.set_fastq_files(filelinedata[lineindex].strip().split(","))
                    case "fastq_r1":
                        vipsample.set_fastq_r1_files(filelinedata[lineindex])
                        # vipsample.set_fastq_r1_files(filelinedata[lineindex].strip().split(","))
                    case "fastq_r2":
                        vipsample.set_fastq_r2_files(filelinedata[lineindex])
                        # vipsample.set_fastq_r2_files(filelinedata[lineindex].strip().split(","))
                    case "sequencing_platform":
                        vipsample.set_sequencing_platform(filelinedata[lineindex])
                        if hasprojectid:
                            self.add_sequencing_platform(filelinedata[projectidindex], re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                        else:
                            self.add_sequencing_platform("vip", re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                    case "cram":
                        vipsample.set_cram_file(filelinedata[lineindex])
                    case "assembly":
                        vipsample.set_assembly(filelinedata[lineindex])
                        if hasprojectid:
                            self.add_assembly(filelinedata[projectidindex], re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                        else:
                            self.add_assembly("vip", re.sub(r"[\x00-\x1f]", "", filelinedata[lineindex].strip()))
                    case "gvcf":
                        vipsample.set_gvcf_file(filelinedata[lineindex])
                    case "vcf":
                        vipsample.set_vcf_file(filelinedata[lineindex])
                    case "pcr_performed":
                        vipsample.set_pcr_performed(filelinedata[lineindex])
                        vipsample.set_pcr_is_performed()
            except IndexError:
                print(f"[ERROR]: Could not find data for column {headerfield} for sample on line {samplenum}")
            lineindex += 1
        return vipsample
    
    
    def get_file_path(self):
        """Returns the path of the file that is the current samplesheet.
        
        Returns
        -------
        self.file_path : str
            Path to the file of this samplesheet
        """
        return self.file_path
    
    
    def get_header_fields(self):
        """Returns the list of samplesheet header columns
        
        Returns
        -------
        self.headerfields : list of str
            List of header columns in samplesheet
        """
        return self.headerfields
    
    
    def get_number_of_columns(self):
        """Returns the number of header columns in the samplesheet.
        
        Returns
        -------
        int
            Number of header columns
        """
        return len(self.headerfields)
    
    
    def get_number_of_samples(self):
        """Returns the number of saved samples in the samplesheet.
        
        Returns
        -------
        int
            Number of samples saved in the samplesheet
        """
        return len(self.samplesheet_data)
    
    
    def get_sample_by_linenumber(self, linenumber):
        """Returns a samplesheet sample based on the line number.
        
        Parameters
        ----------
        linenumber : int
            Linenumber of the sample to get
        """
        if linenumber in self.samplesheet_data:
            return self.samplesheet_data[linenumber]
        return None
    
    
    def get_sheet_sequencing_methods(self):
        """Returns the list of sequencing_method values found in the samplesheet.
        
        Returns
        -------
        self.project_sequencing_methods : list of str
            List of read sequencing methods
        """
        return self.project_sequencing_methods
    
    
    def get_sheet_sequencing_platforms(self):
        """Returns the list of sequencing_platform values found in the samplesheet.
        
        Returns
        -------
        self.project_sequencing_platforms : list of str
            List of seuencing_platform values
        """
        return self.project_sequencing_platforms
    
    
    def get_sheet_assemblies(self):
        """Returns a list of unique assembly values found in the samplesheet.
        
        Returns
        -------
        self.project_assemblies : list of str
            List of unique assembly values found in the samplesheet
        """
        return self.project_assemblies
    
    
    def get_samplesheet_samples(self):
        """Returns the samplesheet samples per file line number.
        
        The returned dictionary contains the samplesheet samples as VIPSamplesheetSample
        objects saved per file line number (the line number in the samplesheet).
        
        Returns
        -------
        self.samplesheet_data : dict
            Dictionary containing VIPSamplesheetSample saved per samplesheet line number.
        """
        return self.samplesheet_data
    
    
    def add_sequencing_method(self, projectid, seqmethod):
        """Adds a sequencing method value to the list of sequencing methods found in the samplesheet if not already present.
        
        Parameters
        ----------
        projectid : str
            Project id to add the sequencing method to
        seqmethod : str
            Sequencing method to add
        """
        if projectid == "":
            projectid = "vip"
        if projectid not in self.project_sequencing_methods:
            self.project_sequencing_methods[projectid] = []
        if seqmethod not in self.project_sequencing_methods[projectid]:
            self.project_sequencing_methods[projectid].append(seqmethod)
    
    
    def add_sequencing_platform(self, projectid, seqplatform):
        """Add a sequencing platform value to the list of sequencing platforms found in the samplesheet if not already present.
        
        Parameters
        ----------
        projectid : str
            Project id to add the sequencing platform to
        seqplatform : str
            Sequencing platform to add.
        """
        if projectid == "":
            projectid = "vip"
        if projectid not in self.project_sequencing_platforms:
            self.project_sequencing_platforms[projectid] = []
        if seqplatform not in self.project_sequencing_platforms[projectid]:
            self.project_sequencing_platforms[projectid].append(seqplatform)
    
    
    def add_assembly(self, projectid, assembly):
        """Adds an assembly value to the list of assemblies found in the samplesheet if not already present.
        
        Parameters
        ----------
        assembly : str
            Assembly value to add to the list of assembly values.
        """
        if projectid == "":
            projectid = "vip"
        if projectid not in self.project_assemblies:
            self.project_assemblies[projectid] = []
        if assembly not in self.project_assemblies[projectid]:
            self.project_assemblies[projectid].append(assembly)
        
    
    
    def get_hpo_terms(self, hpostring):
        """Parses a string containing one or more HPO terms and save them in a structures way.
        
        The terms are saved with the prefix as key. The prefix is for example the HPO part in HPO:123456.
        
        Returns
        -------
        hpodata : dict of str
            Dictionary of HPO terms per prefix
        """
        hpodata = {}
        if hpostring != "":
            hpoterms = hpostring.split(",")
            for hpoterm in hpoterms:
                hpotermchunks = hpoterm.split(":")
                if hpotermchunks[0] not in hpodata:
                    hpodata[hpotermchunks[0]] = []
                hpodata[hpotermchunks[0]].append(hpotermchunks[1])
        return hpodata
    
    
    def get_fastq_files(self):
        """Returns a dictionary of all fastq files in the samplesheet per individual_id.
        
        Note: this is the fastq files list in the fastq column, not a combination of R1 and R2.
        
        Returns
        -------
        fastqfiles : dict of str
            Dictionary of fastq files per individual_id
        """
        fastqfiles = {}
        for samplenum in self.samplesheet_data:
            fastqfiles[self.samplesheet_data[samplenum].get_individual_id()] = self.samplesheet_data[samplenum].get_fastq_files()
        return fastqfiles
    
    
    def get_fastq_r1_files(self):
        """Returns a dictionary of all R1 fastq files in the samplesheet per individual_id.
        
        Returns
        -------
        fastqfiles : dict of str
            Dictionary of R1 fastq files per individual_id
        """
        fastqfiles = {}
        for samplenum in self.samplesheet_data:
            fastqfiles[self.samplesheet_data[samplenum].get_individual_id()] = self.samplesheet_data[samplenum].get_fastq_r1_files()
        return fastqfiles
    
    
    def get_fastq_r2_files(self):
        """Returns a dictionary of all R2 fastq files in the samplesheet per individual_id.
        
        Returns
        -------
        fastqfiles : dict of str
            Dictionary of R2 fastq files per individual_id
        """
        fastqfiles = {}
        for samplenum in self.samplesheet_data:
            fastqfiles[self.samplesheet_data[samplenum].get_individual_id()] = self.samplesheet_data[samplenum].get_fastq_r2_files()
        return fastqfiles
    
    
    def get_cram_files(self):
        """Returns a dictionary of all sam/bam/cram files in the samplesheet per individual_id.
        
        Returns
        -------
        cramfiles : dict of str
            Dictionary of sam/bam/cram files per individual_id.
        """
        cramfiles = {}
        for samplenum in self.samplesheet_data:
            cramfiles[self.samplesheet_data[samplenum].get_individual_id()] = self.samplesheet_data[samplenum].get_cram_file()
        return cramfiles
    
    
    def get_gvcf_files(self):
        """Returns a dictionary of all gvcf files in the samplesheet per individual_id.
        
        Returns
        -------
        gvcffiles : dict of str
            Dictionary of gvcf files per individual_id
        """
        gvcffiles = {}
        for samplenum in self.samplesheet_data:
            gvcffiles[self.samplesheet_data[samplenum].get_individual_id()] = gvcffiles.append(samplesheet_data[samplenum].get_gvcf_file())
        return gvcffiles
    
    
    def get_vcf_files(self):
        """Returns a dictionary of all vcf files in the samplesheet per individual_id.
        
        Returns
        -------
        vcffiles : dict of str
            Dictionary of vcf files per individual_id
        """
        vcffiles = {}
        for samplenum in self.samplesheet_data:
            vcffiles[self.samplesheet_data[samplenum].get_individual_id()] = vcffiles.append(samplesheet_data[samplenum].get_vcf_file())
        return vcffiles
    
    
    def get_individual_ids(self):
        """Returns all individual_id values in the samplesheet.
        
        Returns
        -------
        individuals : list of str
            List of individual_id values
        """
        individuals = []
        for samplenum in self.samplesheet_data:
            individuals.append(self.samplesheet_data[samplenum].get_individual_id())
        return individuals
    
    
    def get_proband_individuals(self):
        """Returns all proband individuals in the samplesheet.
        
        Returns
        -------
        probands : list of VIPSamplesheetSamples
            All proband individuals
        """
        probands = []
        for sample in self.samplesheet_data:
            if self.samplesheet_data[sample].is_proband():
                probands.append(self.samplesheet_data[sample])
        return probands
    
    
    def get_family_ids(self):
        """Returns a list of all family_id values and associated individual_id values in the samplesheet.
        
        Returns
        -------
        family_ids : dict of str
            Dictionary of family_id values as keys and associated individual_id values as value
        """
        family_ids = {}
        for samplenum in self.samplesheet_data:
            familyid = self.samplesheet_data[samplenum].get_family_id()
            if familyid != "":
                if familyid not in family_ids:
                    family_ids[familyid] = []
                family_ids[familyid].append(self.samplesheet_data[samplenum].get_individual_id())
        return family_ids
    
    
    def get_maternal_ids(self):
        """Returns a list of all maternal_id values in the samplesheet.
        
        Returns
        -------
        maternal_ids : list of str
            List of maternal_id values
        """
        maternal_ids = []
        for samplenum in self.samplesheet_data:
            maternal_id = samplesheet_data[samplenum].get_maternal_id()
            if maternal_id != "":
                maternal_ids.append(maternal_id)
        return maternal_ids
    
    
    def get_paternal_ids(self):
        """Returns all paternal_id values read from the samplesheet.
        
        Returns
        -------
        paternal_ids : list of str
            List of read paternal_id values
        """
        paternal_ids = []
        for samplenum in self.samplesheet_data:
            paternal_id = samplesheet_data[samplenum].get_paternal_id()
            if paternal_id != "":
                paternal_ids.append(paternal_id)
        return paternal_ids
    
    
    def check_number_of_columns(self, numofheadercols, numofsamplecols, samplenum):
        """Checks whether the number of header columns and sample columns differ.
        
        Parameters
        ----------
        numofheadercols : int
            Number of header columns
        numofsamplesols : int
            Number of sample columns
        samplenum : int
            Fileline number of the sample
        """
        if numofheadercols > numofsamplecols:
            print(f"[ERROR]: Sample on line {samplenum} has less columns than it should have.")
        elif numofheadercols < numofsamplecols:
            print(f"[ERROR]: Sample on line {samplenum} has more columns than it should have.")
    
    
    def check_input_files(self, list_of_files):
        """Checks the inout files whether the exist
        
        """
        incorrect_files = []
        for inputfile in list_of_files:
            if Path(inputfile).is_file():
                print(f"{inputfile} exists")
            elif "$" in inputfile or "${" in inputfile:
                print(f"{inputfile} may exist but is unknown due to inclusion of bash variable")
            else:
                print(f"{inputfile} does not exist!")
                incorrect_files.append(inputfile)
        return incorrect_files
    
    
    def file_was_read_succesfully(self):
        """Returns whether the file was read succesfully
        
        Returns
        -------
        self.read_file : boolean
            Was the file read succesfully?
        """
        return self.read_file
    
    
    def add_individualid(self, individualid, samplenum):
        """Adds a supplied individual id to the list of individual ids found in the samplesheet.
        
        The samplenum that needs to be supplied is also saved to the program can check
        whether there are duplicate individual_id values in the samplesheet.
        
        Parameters
        ----------
        individualid : str
            Individual ID to add to the list
        samplenum : int
            Sample number of the sample with the individual id to add
        """
        if individualid not in self.individuals:
            self.individuals[individualid] = []
        self.individuals[individualid].append(samplenum)
    
    
    def get_duplicate_individual_ids(self):
        """Returns the duplicate individual_id values in the samplesheet.
        
        Returns
        -------
        dict
            List of duplicate individual ids
        """
        return {i: self.individuals[i] for i in self.individuals if len(self.individuals[i]) > 1}
    
    
    def add_samplesheet_error(self, errortype, errormessage):
        """Adds a samplesheet error message.
        
        The type is for example trio or duplicate individual_id.
        
        Parameters
        ----------
        errortype : str
            Type of error in the samplesheet
        errormessage : str
            The specific error message
        """
        if errortype not in self.samplesheet_errors:
            self.samplesheet_errors[errortype] = []
        self.samplesheet_errors[errortype].append(errormessage)
    
    
    def get_samplesheet_errors(self):
        """Returns the found samplesheet errors.
        
        Returns
        -------
        self.samplesheet_errors : dict of str
            Dictionary containing samplesheet errors
        """
        return self.samplesheet_errors
    
    
    def display_sample_errors(self, sheetsample):
        """Displays the errors found in a sample.
        
        Parameters
        ----------
        sheetsample : VIPSamplesheetSample
            Sample whose errors should be printed
        """
        sample_errors = sheetsample.get_sample_errors()
        if len(sample_errors) > 0:
            for columnname in sample_errors:
                print(f"Print found errors for sample on line {samplenum} | individual_id: {self.samplesheet_data[samplenum].get_individual_id()}:")
                for errormessage in sample_error:
                    print(f"\t[{columnname}]: {errormessage}")
    
    
    def display_all_sample_errors(self):
        """Display the error messages of all samples."""
        for samplenum in self.samplesheet_data:
            self.display_sample_errors(self.samplesheet_data[samplenum])
            print("")
    
    
    def display_samplesheet_errors(self):
        """Displays all samplesheet errors."""
        if len(self.samplesheet_errors) > 0:
            print(f"Print overall samplesheet errors for samplesheet {self.file_path}:")
            for errortype in self.samplesheet_errors:
                for errormessage in self.samplesheet_errors[errortype]:
                    print(f"\t[{errortype}]: {errormessage}")
    
    
    def get_projectid_with_multiple_sequencing_method_values(self):
        """Returns the project_ids that have more than one sequencing_method value.
        
        Returns
        -------
        dict of str
            Project IDs with more than one sequencing_method value
        """
        return {x: self.project_sequencing_methods[x] for x in self.project_sequencing_methods if len(self.project_sequencing_methods[x]) > 1}
    
    
    def get_projectid_with_multiple_sequencing_platform_values(self):
        """Returns the project_ids that have more than one sequencing platform value.
        
        Returns
        -------
        dict of str
            Project IDs with more than one sequencing_platform value
        """
        return {x: self.project_sequencing_platforms[x] for x in self.project_sequencing_platforms if len(self.project_sequencing_platforms[x]) > 1}
    
    
    def get_projectid_with_multiple_assembly_values(self):
        """Returns the project_ids that have more than one assembly value.
        
        Returns
        -------
        dict of str
            Project IDs with more than one assembly value
        """
        return {x: self.project_assemblies[x] for x in self.project_assemblies if len(self.project_assemblies[x]) > 1}
    
    
    def get_projectid_to_sample_list(self):
        """Returns the project_id to samples map.
        
        Returns
        -------
        self.projectid_to_samples : dict of str
            Dict containing the project_id to sample map
        """
        return self.projectid_to_samples
    
    
    def get_project_to_individualid_list(self):
        """Returns the project_id to individual_id map.
        
        Returns
        -------
        self.project_individualids
            Dict with project_id to individual_id
        """
        return self.project_individualids
    
    
    def add_projectid_to_individualid(self, projectid, individualid):
        """Saves a supplied individual_id under the supplied project_id.
        
        Parameters
        ----------
        projectid : str
            Specific project_id to save the individual_id under
        individualid : str
            Specific individual_id to save
        """
        if projectid == "":
            projectid = "vip"
        if projectid not in self.project_individualids:
            self.project_individualids[projectid] = []
        self.project_individualids[projectid].append(individualid)
    
    
    def get_project_duplicate_individualids(self):
        """Returns a dict with duplicate individual_ids per project_id.
        
        Returns
        -------
        duplicate_values : dict of str
            Dict of duplicate individual_id per project_id
        """
        duplicate_values = {}
        for projid in self.project_individualids:
            dupvalues = []
            for individ in self.project_individualids[projid]:
                if individ in dupvalues:
                    if projid not in duplicate_values:
                        duplicate_values[projid] = []
                    duplicate_values[projid].append(individ)
                else:
                    dupvalues.append(individ)
        return duplicate_values
    
    
    def add_projectid_to_sample(self, projectid, samplenum):
        """Saves a supplied sample number under a supplied project_id
        
        Parameters
        ----------
        projectid : str
            Specific project_id to save the sample number to
        samplenum : int
            Specific sample number to save
        """
        if projectid == "":
            projectid = "vip"
        if projectid not in self.projectid_to_samples:
            self.projectid_to_samples[projectid] = []
        if samplenum not in self.projectid_to_samples[projectid]:
            self.projectid_to_samples[projectid].append(samplenum)
    
