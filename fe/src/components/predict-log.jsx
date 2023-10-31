import React from 'react';
import { Button, Container, Table } from 'react-bootstrap';
import axios from 'axios';
import { Link } from 'react-router-dom';

function PredictLogPage() {
  const [predictLogs, setPredictLogs] = React.useState([]);

  React.useEffect(() => {
    axios.get('http://localhost:5000/predict-log/all')
      .then((response) => {
        setPredictLogs(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <Container>
      <h1>PredictLog</h1>
      <Table striped bordered>
        <thead>
          <tr>
            <th>Id</th>
            <th>Text</th>
            <th>Model</th>
            <th>Prediction</th>
            <th>Probability</th>
            <th>Create at</th>
          </tr>
        </thead>
        <tbody>
          {predictLogs.map((predictLog, index) => (
            <tr key={index}>
              <td>{predictLog.id}</td>
              <td>{predictLog.text}</td>
              <td>{predictLog.model_used}</td>
              <td>{predictLog.prediction}</td>
              <td>{Math.round(predictLog.probability * 10000)/100}%</td>
              <td>{predictLog.create_at}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
}

export default PredictLogPage;