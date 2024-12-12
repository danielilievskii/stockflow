import React from "react";
import "./HeroSectinMain.css"
import {AnalysisButton} from "./AnalysisButton";

export const HeroSectionMain = () => {
    return (
        <div>
            <div className="container-fluid">
                <div className="row d-flex justify-content-center align-items-center">
                    <div className="col-md-8 padding-left">
                        <h1 className="text-center">"Прецизно анализирање за паметно инвестирање"</h1>
                        <p className="text-center">Оваа платформа е наменета за анализа на
                            финансиските податоци на македонските компании,
                            која Ви овозможува преглед на предвидени идни
                            трендови за вредноста на акциите на достапните
                            компании. Сите податоци се автоматски ажурирани,
                            со цел да се обезбедат најнови информации од
                            берзата.</p>
                        <div className="wrapper">
                            <AnalysisButton></AnalysisButton>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="picture">
                            <img src="../../../../../background.png"/>
                        </div>
                    </div>
                </div>

            </div>

        </div>
    );
};