#include <TCanvas.h>
#include <TGraph.h>
#include <TF1.h>
#include <TPaveStats.h>
#include <TStyle.h>
#include <TROOT.h>


void rt() {
    gStyle->SetOptFit(0001);

    auto canv = new TCanvas("canv", "canv", 920, 780);
    canv->SetGrid();
    canv->SetLogx(true);
    canv->SetLogy(true);
    auto graph = new TGraph("./rt.dat", "%lg %lg");
    graph->SetTitle("Grafico; Time (s); Distance travelled (m)");
    graph->SetMarkerStyle(20);

    auto power = new TF1("func", "[0]*TMath::Power(x,[1])", 1e2 ,1e3);
    power->SetParNames("A", "alpha");
    power->SetParameters(1, -2);
    power->SetLineWidth(2);
    power->SetLineColor(kRed);
    
    graph->Fit(power, "R");

    graph->Draw("ap");
    
    gPad->Update();
    TPaveStats *stats = (TPaveStats *)graph->FindObject("stats");
    stats->SetX1NDC(0.712418);
    stats->SetY1NDC(0.656085);
    stats->SetX2NDC(0.899782);
    stats->SetY2NDC(0.810847); 

    graph->Draw("AP,SAME");
    
    canv->Print("./img/rt.png");
}