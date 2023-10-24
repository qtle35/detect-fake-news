import { useEffect, useState } from 'react';
import { Container, Row, Col, Button, Card, Spinner } from 'react-bootstrap';
import axios from 'axios';
import moment from 'moment';
import './home.css'
import { FaTrash } from 'react-icons/fa';

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
                setSelectedModel(`${response.data[0].name} ${response.data[0].date}`)
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
                setLoading(false);
                alert('Prediction failed. Please try again.');
                
            });
    };

    const handleRetrainSubmit = () => {
        setLoading(true);
        const currentDateTime = moment().format('YYYY-MM-DD HH:mm:ss');
        axios.post('http://localhost:5000/retrain', { time: currentDateTime, model: selectedModel })
            .then((response) => {
                axios.get('http://localhost:5000/getmodel')
                    .then((response) => {
                        setModels(response.data);
                        setLoading(false);
                        setSelectedModel(`${response.data[0].name} ${response.data[0].date}`)
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                        alert('Failed to fetch models. Please try again.');
                        setLoading(false);
                    });
                setPrediction(response.data.prediction);
            })
            .catch((error) => {
                console.error('Error:', error);
                setLoading(false);
                alert('Retraining failed. Please try again.');
                
            });
    };

    const handleDeleteModel = (model) => {
        const confirmDelete = window.confirm("Co chac?");

        if (confirmDelete) {
            axios
                .post('http://localhost:5000/deletemodel', { model: model })
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
                    alert('Deletion failed. Please try again.');
                });
        }
    };

    return (
        <Container>
            <h1 className="d-flex justify-content-center mt-[5rem] mb-4 text-3xl font-extrabold dark:text-indigo-800 md:text-5xl lg:text-6xl">
                <span className="text-transparent bg-clip-text bg-gradient-to-r to-violet-600 from-blue-900">
                    Machine Learning Detect FakeNews
                </span>
            </h1>
            <Row >
                <Col lg={8} md={7} >
                    <Card >
                        <Card.Body>
                            <div>
                                <select
                                    className="custom-select"
                                    onChange={(e) => setSelectedModel(e.target.value)}
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
                                <Button variant="primary" className="mx-2 custom-button" onClick={() => handleTextSubmit()} disabled={loading} >
                                    Predict
                                    {loading && <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>}
                                </Button>
                                <Button variant="primary" className="custom-button" onClick={() => handleRetrainSubmit('retrain')} disabled={loading}>
                                    Retrain
                                    {loading && <Spinner animation="border" role="status" className="ms-2" />}
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
                <Col lg={4} className="d-flex justify-content-center align-items-center">
                    <img src="/img/man-read.png" alt="vector" />
                </Col>

            </Row>
            {models.length > 0 ? (
                <table className="table table-hover table-bordered">
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
                                    <Button className="btn btn-danger" onClick={() => handleDeleteModel(model)}><FaTrash /></Button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No models available.</p>
            )}

        </Container>
    );
}

export default Home;
