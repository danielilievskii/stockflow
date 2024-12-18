import './App.css';
import React, {useState} from "react";
import {BrowserRouter, BrowserRouter as Router, Route, Routes} from "react-router-dom";
import {Header} from "./views/static/components/header/Header";
import {StockData} from "./views/static/components/stock-data/StockData";
import MainPage from "./views/static/pages/MainPage";
import TechnicalAnalysis from "./views/static/components/technical/technicalAnalysis";
import FundamentalAnalysis from "./views/static/components/fundamentalAnalysis/fundamentalAnalysis";
import ModelAnalysis from "./views/static/components/model/modelAnalysis";

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
            </Routes>
        </BrowserRouter>

    </div>
  );
}

export default App;
