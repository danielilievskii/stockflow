import React from "react";
import { Container, Row, Col, Card, Button } from "react-bootstrap";
import "./ChooseAnalysisMain.css"
import TechnicalAnalysis from "../technical/technicalAnalysis";
import technicalAnalysis from "../technical/technicalAnalysis";
import {Link} from "react-router-dom";

const AnalysisOptions = () => {
    return (
        <div className="cards-section">
            <Container className="py-5" id="targetSection">
                <Row className="text-center g-4">
                    <Col md={4} sm={12} className="mb-4">
                        <Card className="h-100 shadow-sm d-flex flex-column">
                            <Card.Body className="flex-grow-1">
                                <Card.Img
                                    variant="top"
                                    src="../../../../../tehnicka.png"
                                    alt="Техничка анализа"
                                    className="mb-3"
                                    style={{ width: "270px" }}
                                />
                                <Card.Title style={{ fontSize: "28px", fontWeight: "bold" }}>ТЕХНИЧКА АНАЛИЗА</Card.Title>
                                {/*TODO: Change card description*/}
                                <Card.Text style={{ fontSize: "20px" }}>
                                    Техничката анализа се фокусира на проучување на историските податоци за цените
                                    на акциите и обемот на тргување за идентификување трендови и идни движења на цената.
                                </Card.Text>
                            </Card.Body>
                            <div className="mt-auto text-center" style={{ marginBottom: "10px" }}>
                                <Link to="technical" className="custom-link">ОДБЕРИ</Link>
                            </div>
                        </Card>
                    </Col>

                    <Col md={4} sm={12} className="mb-4">
                        <Card className="h-100 shadow-sm d-flex flex-column">
                            <Card.Body className="flex-grow-1">
                                <Card.Img
                                    variant="top"
                                    src="../../../../../fundamentalna.png"
                                    alt="Фундаментална анализа"
                                    className="mb-3"
                                    style={{ width: "270px" }}
                                />
                                <Card.Title style={{ fontSize: "28px", fontWeight: "bold" }}>ФУНДАМЕНТАЛНА АНАЛИЗА</Card.Title>
                                {/*TODO: Change card description*/}
                                <Card.Text style={{ fontSize: "20px" }}>
                                    Фундаменталната анализа се фокусира на оценување на вредноста
                                    на компанијата преку анализа на нејзини финансиски извештаи како и информации од јавни вести.
                                </Card.Text>
                            </Card.Body>
                            <div className="mt-auto text-center" style={{ marginBottom: "10px" }}>
                                <Link to="fundamental" className="custom-link">ОДБЕРИ</Link>
                            </div>
                        </Card>
                    </Col>

                    <Col md={4} sm={12} className="mb-4">
                        <Card className="h-100 shadow-sm d-flex flex-column">
                            <Card.Body className="flex-grow-1">
                                <Card.Img
                                    variant="top"
                                    src="../../../../../model.png"
                                    alt="Модел"
                                    className="mb-3"
                                    style={{ width: "270px" }}
                                />
                                <Card.Title style={{ fontSize: "28px", fontWeight: "bold" }}>ЦЕНОВНА АНАЛИЗА</Card.Title>
                                {/*TODO: Change card description*/}
                                <Card.Text style={{ fontSize: "20px" }}>
                                    Ценовната анализа, базирана на вештачка интелигенција, користи историски податоци за вредноста на акциите за прецизни предвидувања на идните трендови на акциите.                                </Card.Text>
                            </Card.Body>
                            <div className="mt-auto text-center d-flex justify-content-center" style={{ marginBottom: "10px" }}>
                                <Link to="model" className="custom-link">ОДБЕРИ</Link>
                            </div>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default AnalysisOptions;