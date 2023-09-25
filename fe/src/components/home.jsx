import React, { useState } from 'react';
import { Container, Row, Col, Button, Form, Card } from 'react-bootstrap';
import axios from 'axios';
import moment from 'moment';

function Home() {
    const [inputText, setInputText] = useState('');
    const [prediction, setPrediction] = useState('');

    const handleTextSubmit = () => {
        axios.post('http://localhost:5000/predict', { text: inputText })
            .then((response) => {
                setPrediction(response.data.prediction);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };
    const handleRetrainSubmit = () => {
        const currentDateTime = moment().format('YYYY-MM-DD HH:mm:ss');
        axios.post('http://localhost:5000/retrain', { time: currentDateTime })
            .then((response) => {
                setPrediction(response.data.prediction);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };
    return (
        <div>
            <Container>
                <Row>
                    <Col md={6} className="d-flex justify-content-center align-items-center">
                        <Card>
                            <Card.Body>
                                <div id="intro" className="text-center">
                                    <h2 className="mb-4">Rate your news!</h2>
                                    <p>NewsFresh is just like Rotten Tomatoes for news! Users can read, rate, post news & also, keep themselves aware of fake news</p>
                                </div>
                                <Form>
                                    <Form.Group controlId="formText">
                                        <Form.Control
                                            as="textarea"
                                            rows={20}
                                            placeholder="Enter your text here"
                                            value={inputText}
                                            onChange={(e) => setInputText(e.target.value)}
                                        />
                                    </Form.Group>
                                    <div className="text-center">
                                        <Button variant="primary" id="btn-2" className="mr-3" onClick={() => handleTextSubmit()}>
                                            Predict
                                        </Button>
                                        <Button variant="primary" id="btn-2" onClick={() => handleRetrainSubmit('retrain')}>
                                            Retrain
                                        </Button>
                                    </div>
                                </Form>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={6} className="d-flex justify-content-center align-items-center">
                        <img src="/img/man-read.png" alt="vector" />
                    </Col>
                </Row>
                {prediction && (
                    <Row className="mt-4">
                        <Col md={12} className="d-flex justify-content-center">
                            <Card>
                                <Card.Body>
                                    <h3 className="mb-4">Prediction:</h3>
                                    <p>{prediction}</p>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                )}
            </Container>
        </div>
    );
}

export default Home;
