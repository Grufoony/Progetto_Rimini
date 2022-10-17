#include <TCanvas.h>
#include <TGraph.h>
#include <TF1.h>
#include <TPaveStats.h>
#include <TStyle.h>
#include <TROOT.h>

void rho_r()
{
    gStyle->SetOptFit(0000);
    gStyle->SetStatX(0.475);
    gStyle->SetStatY(0.3);
    gStyle->SetStatW(0.2);

    auto canv = new TCanvas("canv", "canv", 920, 780);
    canv->SetGrid();
    canv->SetLogx(true);
    canv->SetLogy(true);
    auto graph = new TGraph("./real_distance.dat", "%lg %lg");
    graph->SetTitle("Population density vs distance travelled; Distance travelled (m); Density");
    graph->SetMarkerStyle(20);
    graph->GetXaxis()->SetLimits(1e2, 1e4);

    auto exp = new TF1("exp", "[0]*TMath::Exp([1]*x)", 290, 3e3);
    exp->SetParNames("Amplitude", "Phase");
    exp->SetParameters(1, 0);
    graph->Fit(exp, "R");

    auto power = new TF1("power", "[0]*TMath::Power(x,[1])", 3e3, 1e4);
    power->SetParNames("A", "alpha");
    power->SetParameters(1e3, -1);
    graph->Fit(power, "R+");

    std::cout << "Exponential law: " << exp->GetParameter(1) << '\n';
    std::cout << "Power law: " << power->GetParameter(1) << '\n';

    graph->Draw("ap");
    canv->Print("./img/rho_r.png");
}