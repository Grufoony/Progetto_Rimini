#include <TCanvas.h>
#include <TGraph.h>
#include <TF1.h>
#include <TPaveStats.h>
#include <TStyle.h>
#include <TROOT.h>

void vt() {
    gStyle->SetOptFit(0001);
    auto canv = new TCanvas("canv", "canv", 920, 780);
    canv->SetGrid();
    canv->SetLogx(true);
    canv->SetLogy(true);
    auto graph = new TGraph("./vt.dat", "%lg %lg");
    graph->SetTitle("Grafico; Distance travelled (m); Velocity (m/s)");
    graph->SetMarkerStyle(20);

    auto power = new TF1("func", "[0]*TMath::Power(x,[1])", 0.1, 1.5e4);
    power->SetParNames("A", "alpha");
    power->SetParameters(1, -2);
    power->SetLineWidth(2);
    power->SetLineColor(kRed);

    graph->Fit(power, "R");

    graph->Draw("ap");

    gPad->Update();
    TPaveStats *stats = (TPaveStats *)graph->FindObject("stats");
    stats->SetX1NDC(0.406318);
    stats->SetY1NDC(0.751323);
    stats->SetX2NDC(0.754902);
    stats->SetY2NDC(0.900794); 

    graph->Draw("AP,SAME");

    canv->Print("./img/vt.png");
}