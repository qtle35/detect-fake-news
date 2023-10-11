import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Button, Card, Spinner } from 'react-bootstrap';
import axios from 'axios';
import moment from 'moment';
import './home.css'

function Home() {
    const [inputText, setInputText] = useState('');
    const [prediction, setPrediction] = useState('');
    const [loading, setLoading] = useState(false);
    const [models, setModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState('');

    useEffect(() => {
        axios.get('http://localhost:5000/getmodel')
            .then((response) => {
                setModels(response.data);
                console.log(response.data);
                handleSelectModel(`${response.data[0].name} ${response.data[0].date}`)

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, []);

    const handleTextSubmit = () => {
        if (!inputText) {
            alert('Please enter text');
            return;
        }
        setLoading(true);
        setPrediction('');
        axios.post('http://localhost:5000/predict', { text: inputText, model: selectedModel })
            .then((response) => {
                setPrediction(response.data.prediction);
                setLoading(false);
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
                alert('Retraining failed. Please try again.');
            });
    };

    const handleSelectModel = (url) => {
        setSelectedModel(url)
    }

    return (
        <div className='py-2'>
            <Container>
                <h1 className=" mt-[5rem] mb-4 text-3xl font-extrabold dark:text-indigo-800 md:text-5xl lg:text-6xl">
                    <span className="text-transparent bg-clip-text bg-gradient-to-r to-violet-600 from-blue-900">
                        Machine Learning Detect FakeNews
                    </span>
                </h1>
                <Row>
                    <Col md={6} className="">
                        <Card>
                            <Card.Body>
                                <div>
                                    <select
                                        className="custom-select"
                                        onChange={(e) => handleSelectModel(e.target.value)}
                                    >
                                        {models.map((model, index) => (
                                            <option key={index} value={`${model.name} ${model.date}`} >{`${model.id} ${model.name} ${model.date}`}</option>
                                        ))}
                                    </select>
                                </div>
                                <textarea
                                    rows={10}
                                    placeholder="Enter your news here"
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    className="custom-textarea"
                                />
                                <div className="text-center">
                                    <Button variant="primary" id="btn-2" className="mx-2 custom-button" onClick={() => handleTextSubmit()} disabled={loading} >
                                        Predict
                                        {loading && <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>}
                                    </Button>
                                    <Button variant="primary" id="btn-2" className="custom-button" onClick={() => handleRetrainSubmit('retrain')}>
                                        Retrain
                                    </Button>
                                </div>
                                {prediction && (
                                    <Row className="mt-4">
                                        <Col md={12} className="d-flex justify-content-center">
                                            <h5 className="mb-4">Prediction: {prediction}</h5>
                                        </Col>
                                    </Row>
                                )}
                                {loading && (
                                    <div className='d-flex justify-content-center my-2'>
                                        <Spinner animation="border" role="status">
                                            <span className="visually-hidden">Loading...</span>
                                        </Spinner>
                                    </div>
                                )}
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={6} className="d-none d-md-flex justify-content-center align-items-center ">
                        <img src="/img/man-read.png" alt="vector" />
                    </Col>
                </Row>
                {models.length > 0 ? (
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Id</th>
                                <th>Name</th>
                                <th>Date</th>
                                <th>Accuracy</th>
                                <th>Precision</th>
                                <th>Recall</th>
                                <th>F1 Score</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {models.map((model, index) => (
                                <tr key={index}>
                                    <td>{model.id}</td>
                                    <td>{model.name}</td>
                                    <td>{model.date}</td>
                                    <td>{model.acc}</td>
                                    <td>{model.pre}</td>
                                    <td>{model.re}</td>
                                    <td>{model.f1}</td>
                                    <td>
                                        <Button className="btn btn-danger">Delete</Button>
                                    </td>
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
