import ROOT

# Enable multi-threading
# The default here is set to a single thread. You can choose the number of threads based on your system.
ROOT.ROOT.EnableImplicitMT(1)

# Open input file
fname = "../../data/doubleeg_nanoaod_eg.root"
df = ROOT.RDataFrame("Events", fname)
# Book histogram of dimuon mass spectrum
bins = 3000 # Number of bins in the histogram
low = 0.35 # Lower edge of the histogram
up = 300.0 # Upper edge of the histogram
hist = df.Histo1D(ROOT.RDF.TH1DModel("", "", bins, low, up), "PFCands_pt")

# Request cut-flow report
report = df.Report()

# Create canvas for plotting
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)
c.SetLogx()
c.SetLogy()

# Draw histogram
hist.GetXaxis().SetTitle("PFCands_pt")
hist.GetXaxis().SetTitleSize(0.04)
hist.Draw()
# Draw labels
label = ROOT.TLatex()
label.SetTextAlign(22)
label.DrawLatex(0.55, 3.0e4, "#eta")
label.DrawLatex(0.77, 7.0e4, "#rho,#omega")
label.DrawLatex(1.20, 4.0e4, "#phi")
label.DrawLatex(4.40, 1.0e5, "J/#psi")
label.DrawLatex(4.60, 1.0e4, "#psi'")
label.DrawLatex(12.0, 2.0e4, "Y(1,2,3S)")
label.DrawLatex(91.0, 1.5e4, "Z")
label.SetNDC(True)
label.SetTextAlign(11)
label.SetTextSize(0.04)
label.DrawLatex(0.10, 0.92, "#bf{PFCands Plotting}")
label.SetTextAlign(31)

# Save plot
c.SaveAs("PFCands_pt.png")

# Print cut-flow report
report.Print()

# Book histogram of dimuon mass spectrum
bins = 200 # Number of bins in the histogram
low = 10 # Lower edge of the histogram
up = 10.0 # Upper edge of the histogram
hist = df.Histo1D(ROOT.RDF.TH1DModel("", "", bins, low, up), "nPFCands")

# Request cut-flow report
report = df.Report()

# Create canvas for plotting
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)
c.SetLogx()
c.SetLogy()

# Draw histogram
hist.GetXaxis().SetTitle("nPFCands")
hist.GetXaxis().SetTitleSize(0.04)
hist.Draw()

# Draw labels
label = ROOT.TLatex()
label.SetTextAlign(22)
label.DrawLatex(0.55, 3.0e4, "#eta")
label.DrawLatex(0.77, 7.0e4, "#rho,#omega")
label.DrawLatex(1.20, 4.0e4, "#phi")
label.DrawLatex(4.40, 1.0e5, "J/#psi")
label.DrawLatex(4.60, 1.0e4, "#psi'")
label.DrawLatex(12.0, 2.0e4, "Y(1,2,3S)")
label.DrawLatex(91.0, 1.5e4, "Z")
label.SetNDC(True)
label.SetTextAlign(11)
label.SetTextSize(0.04)
label.DrawLatex(0.10, 0.92, "#bf{PFCands Plotting}")
label.SetTextAlign(31)

# Save plot
c.SaveAs("nPFCands.png")
# Print cut-flow report
report.Print()