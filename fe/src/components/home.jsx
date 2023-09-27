import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import axios from 'axios';
import moment from 'moment';
import './home.css'

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
        if (!inputText) {
            alert('Please enter text');
            return;
        }
        axios.post('http://localhost:5000/predict', { text: inputText, model: selectedModel })
            .then((response) => {
                axios.get('http://localhost:5000/getmodel')
                    .then((response) => {
                        setModels(response.data);
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                        alert('Failed to fetch models. Please try again.');
                    });
                setPrediction(response.data.prediction);
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Prediction failed. Please try again.');
            });
    };

    const handleRetrainSubmit = () => {
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
                    <Col md={6} className="">
                        <Card>
                            <Card.Body>
                                <div>
                                    <select
                                        value={selectedModel}
                                        onChange={(e) => setSelectedModel(e.target.value)}
                                        className="custom-select"
                                    >
                                        <option value="">Select a model</option>
                                        {models.map((model, index) => (
                                            <option key={index} value={model.name}>{`${model.name} ${model.date}`}</option>
                                        ))}
                                    </select>
                                </div>
                                <textarea
                                    rows={20}
                                    placeholder="Enter your news here"
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    className="custom-textarea"
                                />
                                <div className="text-center">
                                    <Button variant="primary" id="btn-2" className="mr-3 custom-button" onClick={() => handleTextSubmit()}>
                                        Predict
                                    </Button>
                                    <Button variant="primary" id="btn-2" className="custom-button" onClick={() => handleRetrainSubmit('retrain')}>
                                        Retrain
                                    </Button>
                                </div>
                                {prediction && (
                                    <Row className="mt-4">
                                        <Col md={12} className="d-flex justify-content-center">
                                            <h5 className="mb-4">Prediction: </h5>
                                            <p>{prediction}</p>
                                        </Col>
                                    </Row>
                                )}
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={6} className="d-flex justify-content-center align-items-center">
                        <img src="/img/man-read.png" alt="vector" />
                    </Col>
                </Row>
                {models.length > 0 ? (
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Date</th>
                                <th>Accuracy</th>
                                <th>Precision</th>
                                <th>Recall</th>
                                <th>F1 Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {models.map((model, index) => (
                                <tr key={index}>
                                    <td>{model.name}</td>
                                    <td>{model.date}</td>
                                    <td>{model.acc}</td>
                                    <td>{model.pre}</td>
                                    <td>{model.re}</td>
                                    <td>{model.f1}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No models available.</p>
                )}

            </Container>
        </div>
    );
}

export default Home;
