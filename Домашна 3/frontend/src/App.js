import './App.css';
import React, {useState} from "react";
import {BrowserRouter, BrowserRouter as Router, Route, Routes} from "react-router-dom";
import {LandingPage} from "./views/static/LandingPage";
import {Header} from "./views/static/Header";
import {StockData} from "./views/stock_data/StockData";

function App() {
  return (
    <div className="App">
        <BrowserRouter>
            <Header/>
            <Routes>
                <Route path="/" element={<LandingPage/>}/>
                <Route path="/stock-data" element={<StockData/>}/>
            </Routes>
        </BrowserRouter>

    </div>
  );
}

export default App;
