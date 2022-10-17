#include <TCanvas.h>
#include <TGraph.h>
#include <TF1.h>
#include <TPaveStats.h>
#include <TStyle.h>
#include <TROOT.h>

void rho_v()
{
    gStyle->SetOptFit(0001);

    auto canv = new TCanvas("canv", "canv", 920, 780);
    canv->SetGrid();
    canv->SetLogx(true);
    canv->SetLogy(true);
    auto graph = new TGraph("./speed.dat", "%lg %lg");
    graph->SetTitle("Grafico; Velocity (m/s); Density");
    graph->SetMarkerStyle(20);
    graph->GetXaxis()->SetLimits(1., 100.);

    auto exp = new TF1("func", "[0]*TMath::Exp(x*[1])", 0.83, 40.);
    exp->SetParNames("Amplitude", "Phase");
    exp->SetParameters(1, -2);

    graph->Fit(exp, "R+");

    auto power = new TF1("func", "[0]*TMath::Power(x,[1])", 10., 40.);
    power->SetParNames("A", "alpha");
    power->SetParameters(1, -2);

    graph->Fit(power, "R+");

    graph->Draw("ap");
    canv->Print("./img/rho_v.png");
}