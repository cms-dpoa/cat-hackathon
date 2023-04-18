import ROOT

# Enable multi-threading
# The default here is set to a single thread. You can choose the number of threads based on your system.
ROOT.ROOT.EnableImplicitMT(1)

# Open input file
fname = "data/doubleeg_nanoaod_eg.root"
df = ROOT.RDataFrame("Events", fname)

# Book histogram of dimuon mass spectrum
bins = 3000 # Number of bins in the histogram
low = 0.39 # Lower edge of the histogram
up = 250.0 # Upper edge of the histogram
hist = df.Histo1D(ROOT.RDF.TH1DModel("", "", bins, low, up), "PFCands_pt")

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
label.SetNDC(True)
label.SetTextSize(0.04)
label.DrawLatex(0.10, 0.92, "#bf{PFCands Plotting}")
label.SetTextAlign(31)

# Save plot
c.SaveAs("PFCands_pt.png")

# Book histogram of dimuon mass spectrum
bins = 200 # Number of bins in the histogram
low = 10 # Lower edge of the histogram
up = 10.0 # Upper edge of the histogram
hist = df.Histo1D(ROOT.RDF.TH1DModel("", "", bins, low, up), "nPFCands")

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
label.SetNDC(True)
label.SetTextAlign(11)
label.SetTextSize(0.04)
label.DrawLatex(0.10, 0.92, "#bf{PFCands Plotting}")
label.SetTextAlign(31)

# Save plot
c.SaveAs("nPFCands.png")
