import './App.css';
import React, {useState} from "react";
import {BrowserRouter, BrowserRouter as Router, Route, Routes} from "react-router-dom";
import {Header} from "./views/dynamic/components/header/Header";
import {StockData} from "./views/dynamic/components/stock-data/StockData";
import MainPage from "./views/dynamic/pages/MainPage";
import TechnicalAnalysis from "./views/dynamic/components/analysis/technicalAnalysis";
import FundamentalAnalysis from "./views/dynamic/components/analysis/fundamentalAnalysis";
import ModelAnalysis from "./views/dynamic/components/analysis/modelAnalysis";
import ResultChart from "./views/dynamic/components/analysis/result/ResultChart";

function App() {


  return (
    <div className="App">
        <BrowserRouter>
            <Header/>
            <Routes>
                <Route path="/" element={<MainPage/>}/>
                <Route path="/technical" element={<TechnicalAnalysis/>}/>
                <Route path="/stock-data" element={<StockData/>}/>
                <Route path="/fundamental" element={<FundamentalAnalysis/>}/>
                <Route path="/model" element={<ModelAnalysis/>}/>
                <Route path="/chart-data" element={<ResultChart />} />
            </Routes>
        </BrowserRouter>

    </div>
  );
}

export default App;
