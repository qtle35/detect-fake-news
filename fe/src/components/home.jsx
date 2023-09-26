import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Button, Form, Card } from 'react-bootstrap';
import axios from 'axios';
import moment from 'moment';

function Home() {
    const [inputText, setInputText] = useState('');
    const [prediction, setPrediction] = useState('');
    const [models, setModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState('');

    useEffect(() => {
        axios.get('http://localhost:5000/getmodel')
            .then((response) => {
                setModels(response.data);
                console.log(response.data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, []);

    const handleTextSubmit = () => {
        if (!selectedModel) {
            alert('Please select a model.');
            return;
        }

        axios.post('http://localhost:5000/predict', { text: inputText, model: selectedModel })
            .then((response) => {
                setPrediction(response.data.prediction);
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Prediction failed. Please try again.');
            });
    };

    const handleRetrainSubmit = () => {
        if (!selectedModel) {
            alert('Please select a model.');
            return;
        }

        const currentDateTime = moment().format('YYYY-MM-DD HH:mm:ss');
        axios.post('http://localhost:5000/retrain', { time: currentDateTime, model: selectedModel })
            .then((response) => {
                setPrediction(response.data.prediction);
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Retraining failed. Please try again.');
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
                                <div>
                                    <Form.Group controlId="formModel">
                                        <Form.Label>Select a Model:</Form.Label>
                                        <Form.Control
                                            as="select"
                                            value={selectedModel}
                                            onChange={(e) => setSelectedModel(e.target.value)}
                                        >
                                            <option value="">Select a model</option>
                                            {models.map((model, index) => (
                                                <option key={index} value={model.name}>{`${model.name} ${model.date}`}</option>
                                            ))}
                                        </Form.Control>
                                    </Form.Group>
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
