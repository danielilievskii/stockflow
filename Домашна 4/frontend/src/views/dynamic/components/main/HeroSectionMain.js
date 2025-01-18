import React from "react";
import "./HeroSectinMain.css"
import {AnalysisButton} from "./AnalysisButton";

export const HeroSectionMain = () => {
    return (
        <div className="hero-section">
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-8 col-sm-12 p-5">
                        <div className="d-flex flex-column">
                            <h1 className="text-center">Прецизно анализирање за паметно инвестирање</h1>
                            <p className="text-center">Оваа платформа е наменета за анализа на
                                финансиските податоци на македонските компании,
                                која ви овозможува преглед на предвидени идни
                                трендови за вредноста на акциите на достапните
                                компании. Сите податоци се автоматски ажурирани,
                                со цел да се обезбедат најнови информации од
                                берзата.</p>
                            <div className="d-flex justify-content-center">
                                <AnalysisButton></AnalysisButton>
                            </div>
                        </div>

                    </div>
                    <div className="col-md-4 col-sm-12">
                        <div className="picture">
                            <img src="../../../../../background.png"/>
                        </div>
                    </div>
                </div>

            </div>

        </div>
    );
};