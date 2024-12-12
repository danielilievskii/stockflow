import React from "react";
import { Container, Row, Col, Card, Button } from "react-bootstrap";
import "./ChooseAnalysisMain.css"
import TechnicalAnalysis from "../technical/technicalAnalysis";
import technicalAnalysis from "../technical/technicalAnalysis";
import {Link} from "react-router-dom";

const AnalysisOptions = () => {
    return (
        <Container className="py-5" style={{marginTop: "150px",marginBottom: "100px"}} id="targetSection">
            <Row className="text-center">
                <Col md={4} sm={12} className="mb-4">
                    <Card className="h-100 shadow-sm">
                        <Card.Body>
                            <Card.Img
                                variant="top"
                                src="../../../../../tehnicka.png"
                                alt="Техничка анализа"
                                className="mb-3"
                                style={{width: "270px"}}
                            />
                            <Card.Title style={{fontSize: "28px", fontWeight: "bold"}}>ТЕХНИЧКА АНАЛИЗА</Card.Title>
                            <Card.Text style={{fontSize: "20px"}}>
                                Техничката анализа се заснова на анализа на историските податоци
                                за акциите на компанијата и ги предвидува моменталните движења
                                на пазарот врз основа на минатото.
                            </Card.Text>
                            <div>
                                <Link to="technical" className="custom-link"> ОДБЕРИ </Link>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={4} sm={12} className="mb-4">
                    <Card className="h-100 shadow-sm">
                        <Card.Body>
                            <Card.Img
                                variant="top"
                                src="../../../../../fundamentalna.png"
                                alt="Фундаментална анализа"
                                className="mb-3"
                                style={{width: "270px"}}
                            />
                            <Card.Title style={{fontSize: "28px", fontWeight: "bold"}}>ФУНДАМЕНТАЛНА
                                АНАЛИЗА</Card.Title>
                            <Card.Text style={{fontSize: "20px"}}>
                                Фундаменталната анализа се фокусира на оценување на вредноста
                                на компанијата преку анализа на финансиските извештаи.
                            </Card.Text>
                            <div>
                                <Link to="fundamental" className="custom-link"> ОДБЕРИ </Link>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>

                <Col md={4} sm={12} className="mb-4">
                    <Card className="h-100 shadow-sm">
                        <Card.Body>
                            <Card.Img
                                variant="top"
                                src="../../../../../model.png"
                                alt="Модел"
                                className="mb-3"
                                style={{width: "270px"}}
                            />
                            <Card.Title style={{fontSize: "28px", fontWeight: "bold"}}>МОДЕЛ</Card.Title>
                            <Card.Text style={{fontSize: "20px"}}>
                                Моделот се обучува со користење на историски податоци за
                                акциите, економски индикатори и други релевантни фактори, со помош на LSTM (Long Short Term Memory).
                            </Card.Text>
                            <div>
                                <Link to="model" className="custom-link"> ОДБЕРИ </Link>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default AnalysisOptions;