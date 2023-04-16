#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooExtendPdf.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
using namespace RooFit ;

void gendata(int numevents, const char* outfilename)
{
   // Declare observable x
  RooRealVar x("x","x",0,10) ;

  // Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma) and their parameters
  RooRealVar mean("mean","mean of gaussians",5) ;
  RooRealVar sigma1("sigma1","width of gaussians",0.5) ;
  // RooRealVar sigma2("sigma2","width of gaussians",1) ;

  RooGaussian sig1("sig1","Signal component 1",x,mean,sigma1) ;
  //RooGaussian sig2("sig2","Signal component 2",x,mean,sigma2) ;

  // Build Chebychev polynomial p.d.f.
  RooRealVar a0("a0","a0",0.5,0.,1.) ;
  RooRealVar a1("a1","a1",-0.2,0.,1.) ;
  RooChebychev bkg("bkg","Background",x,RooArgSet(a0,a1)) ;

  // Sum the signal components into a composite signal p.d.f.
  RooRealVar sig1frac("sig1frac","fraction of component 1 in signal",0.8,0.,1.) ;
  //RooAddPdf sig("sig","Signal",RooArgList(sig1,sig2),sig1frac) ;
  RooAddPdf sig("sig","Signal",RooArgList(sig1),sig1frac) ;

  // Sum the composite signal and background into an extended pdf nsig*sig+nbkg*bkg
  RooRealVar nsig("nsig","number of signal events",500,0.,10000) ;
  RooRealVar nbkg("nbkg","number of background events",500,0,10000) ;
  RooAddPdf  model("model","(g1+g2)+a",RooArgList(bkg,sig),RooArgList(nbkg,nsig)) ;

  RooDataSet *data = model.generate(x, numevents) ;

  // Create a new workspace
  RooWorkspace *w = new RooWorkspace("w","workspace") ;
  w->import(model) ;
  w->import(*data) ;

  // Print workspace contents
  w->Print() ;
  // Save the workspace into a ROOT file
  w->writeToFile(outfilename) ;
  // Workspace will remain in memory after macro finishes
  gDirectory->Add(w) ;

}
