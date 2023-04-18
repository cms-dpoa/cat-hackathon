This script is used to run a particle flow (PF) analysis on CMS open data. It can be used to create NanoAOD files containing only PF candidates, which can be used for further analysis with other tools like Coffea. The script uses CMS software to process the data, and requires a Docker image to run.

## Prerequisites

To use this script, you will need the following:

-   A working Docker installation
-   An input file in the NanoAOD format (this can be obtained from the CERN Open Data portal)
-   A record ID from the CERN Open Data portal (this is used to access the input file)

## Script details

The `pf_production.sh` script is designed to run on a CERN computing system with a pre-installed CMS environment. It takes three input parameters:

-   `$1` (optional): The user to run the script as. Defaults to `other`.
-   `$2` (optional): The number of events to process. Defaults to 20.
-   `$3` (optional): The path to the input file. Defaults to a publicly available dataset on the CERN EOS system.

The script sets up the CMS environment, initializes a CMSSW release, and clones the PFNano code from the DAZSLE repository. It then generates a python configuration file `doubleeg_cfg.py` using `cmsDriver.py` with the specified number of events, input file, and customizations. Finally, it executes the `cmsRun` command to process the events and create the output ROOT file.

If the script is run in a GitHub Actions environment, it will copy the output ROOT file to the `/mnt/vol/output.root` path to make it available to subsequent workflow steps.

The script includes comments throughout to explain each step and provide context for the commands being executed. It is intended to be used as a reference for users looking to run PFNano on their own datasets, and can be modified to suit different use cases.

Here's a detailed explanation of what the `pf_production.sh` script does:

1.  The script sets some default values for the `runas`, `nevents`, and `inputfile` variables, in case they are not set by the user.
    
2.  The script sets some environment variables and prepares the working directory.
    
3.  The script uses the `cmsrel` command to set up a CMS environment.
    
4.  The script uses the `cmsDriver.py` command to run the PF analysis on the input data. This creates a NanoAOD file containing only PF candidates.

### Running the script

To run the script, open a terminal and navigate to the directory where `pf_production.sh` is located. Then run the following command:

```bash
./pf_production.sh <runas> <nevents> <inputfile>
```

-   `<runas>` is an optional parameter. If running outside of GitHub Actions, you can give any string as the first parameter. This is the username that the script will run as. If not specified, the default value is `other`.
-   `<nevents>` is also an optional parameter. This is the number of events that will be processed by the script. The default value is 20 if not specified.
-   `<inputfile>` is the path to the input file that the script will process. The default value is a file located on the EOS public instance at CERN, but you can specify your own file if you have one.

### Output

After running the script, the output will be stored in a file called `doubleeg_nanoaod.root`. If you're running the script in a GitHub Actions environment, this file will be copied to `/mnt/vol/output.root`.


### Conclusion

With this script, you should be able to process CMS Open Data and produce NanoAOD files that can be used for analysis. If you have any questions or encounter any issues while running the script, feel free to reach out to the CMS Open Data team. Happy analyzing!
