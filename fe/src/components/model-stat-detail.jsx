import React from 'react';
import { Button } from 'react-bootstrap';
import DateTimePicker from 'react-datetime-picker';
import axios from 'axios';
import moment from 'moment';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

function ModelStatDetail(props) {
  const [modelStats, setModelStats] = React.useState([]);
  const [startTime, onChangeStartTime] = React.useState(new Date());
  const [endTime, onChangeEndTime] = React.useState(new Date());

  function handleStat() {
    if (endTime < startTime) {
      alert('End time must be greater than start time. Please try again.');
    }
    axios.get(`http://localhost:5000/model-stat?name=${props.name}&start-time=${moment(startTime).format('YYYY-MM-DD HH:mm:ss')}&end-time=${moment(endTime).format('YYYY-MM-DD HH:mm:ss')}`)
      .then((response) => {
        setModelStats(response.data);
      }).catch((error) => {
        console.error('Error:', error);
        alert('Get failed. Please try again.');
      });
  }
  return (
    <div>
      <DateTimePicker onChange={onChangeStartTime} value={startTime} />
      <strong>{' - '}</strong>
      <DateTimePicker onChange={onChangeEndTime} value={endTime} />
      {' '}
      <Button className="btn btn-primary" onClick={() => handleStat()}>Stat</Button>
      <div>
        <LineChart
          width={500}
          height={300}
          data={modelStats}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" tickFormatter={(date) => {return moment(date).format('YY-MM-DD HH:mm:ss')}}/>
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="acc" stroke="#8884d8" />
          <Line type="monotone" dataKey="pre" stroke="#2ca02c" />
          <Line type="monotone" dataKey="re" stroke="#d62728" />
          <Line type="monotone" dataKey="f1" stroke="#82ca9d" />
        </LineChart>
      </div>
    </div>
  );
}

export default ModelStatDetail;