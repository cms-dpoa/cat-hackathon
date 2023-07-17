# cd /home/cmsusr
echo "Setting up ${CMSSW_VERSION}"
ls ${CMS_INSTALL_DIR}
source ${CMS_INSTALL_DIR}/cmsset_default.sh
scramv1 project CMSSW ${CMSSW_VERSION}
cd ${CMSSW_VERSION}/src
eval `scramv1 runtime -sh`
echo "CMSSW should now be available."
sh $REANA_WORKSPACE/codeRun/pf_production.sh reana
cp output.root $REANA_WORKSPACE/results/production_output/