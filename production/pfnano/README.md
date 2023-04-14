This script is used to run a particle flow (PF) analysis on CMS open data. It can be used to create NanoAOD files containing only PF candidates, which can be used for further analysis with other tools like Coffea. The script uses CMS software to process the data, and requires a Docker image to run.

## Prerequisites

To use this script, you will need the following:

-   A working Docker installation
-   An input file in the NanoAOD format (this can be obtained from the CERN Open Data portal)
-   A record ID from the CERN Open Data portal (this is used to access the input file)

## Usage

To use this script, follow these steps:

1.  Clone the repository containing the `pf_production.sh` script:
    
    bashCopy code
    
    `git clone https://github.com/DAZSLE/PFNano.git`
    
2.  Change to the `production/pfnano` directory:
    
    bashCopy code
    
    `cd PFNano/production/pfnano`
    
3.  Set the `runas`, `nevents`, and `inputfile` variables in the script as needed. These variables control how the script runs and what data it processes.
    
    -   `runas`: This controls the user that the script runs as. By default, the script runs as the user who executes it, but you can also specify `github` to run the script as the `github` user. This is used to set the correct permissions when running the script in a Docker container.
        
    -   `nevents`: This controls how many events the script processes. By default, the script processes 20 events.
        
    -   `inputfile`: This is the path to the input NanoAOD file. By default, the script uses a file from the CERN Open Data portal, but you can change this to use your own input file.
        
4.  Start the Docker container and run the script:
    
    bashCopy code
    
    `docker run -v $(pwd):/mnt/vol -w /home/cmsusr gitlab-registry.cern.ch/cms-cloud/cmssw-docker/cmssw_10_6_30-slc7_amd64_gcc700 /bin/bash /mnt/vol/production/pfnano/pf_production.sh github && cp output.root outputs/production/`
    
    This command starts a Docker container, mounts the current directory to the `/mnt/vol` directory in the container, sets the working directory to `/home/cmsusr`, and runs the `pf_production.sh` script. The `github` parameter tells the script to run as the `github` user. Finally, the script copies the output file to the `outputs/production` directory.
    
    Note that the Docker image used by the script is quite large (several GB), so it may take some time to download if you don't already have it.
    
5.  Once the script has finished running, the output file (`output.root`) will be in the `outputs/production` directory.

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

### Troubleshooting

If you encounter any issues while running the script, here are some things you can try:

-   Make sure that you have the correct version of ROOT installed on your machine. You can check the version by running `root-config --version` in a terminal. The version used in the script is ROOT 6.22/06.
-   Check that you have the required packages installed. These include `git`, `curl`, `python3-dev`, and `python3-pip`.
-   If you're running the script on a macOS machine, you may encounter issues with `curl`. In this case, you can try using `brew` to install `curl-openssl` instead.
-   If you're running the script on a Windows machine, you'll need to use a Linux environment such as Windows Subsystem for Linux (WSL).

### Conclusion

With this script, you should be able to process CMS Open Data and produce NanoAOD files that can be used for analysis. If you have any questions or encounter any issues while running the script, feel free to reach out to the CMS Open Data team. Happy analyzing!
