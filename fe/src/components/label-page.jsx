import React from 'react';
import { Button, Container, InputGroup, Table, Form } from 'react-bootstrap';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useAuth } from './auth-context';

function LabelPage() {
  const { getUser } = useAuth()
  const user = getUser()

  const [labels, setLabels] = React.useState([]);
  const [key, setKey] = React.useState('');
  React.useEffect(() => {
    axios.get('http://localhost:5000/label', {
      auth: user
    })
      .then((response) => {
        setLabels(response.data);
      })
      .catch((error) => {
        console.error(error);
        alert('Get failed. Please try again.');
      });
  }, []);

  const handleSearch = () => {
    axios.get(`http://localhost:5000/label?search=${key}`, {
      auth: user
    })
      .then((res) => {
        setLabels(res.data);
      }).catch((error) => {
        console.error('Error:', error);
        alert('Search failed. Please try again.');
      });
  };

  const handleDelete = (id) => {
    const confirmDelete = window.confirm("Bạn có muốn xóa không?");
    if (confirmDelete) {
      axios.delete(`http://localhost:5000/label/${id}`, {
        auth: user
      })
        .then(() => {
          let updatedLabels = [...labels].filter(i => i.id !== id);
          setLabels(updatedLabels);
        }).catch((error) => {
          console.error('Error:', error);
          alert('Delete failed. Please try again.');
        });
    }
  };

  return (
    <Container>
      <h1>Label</h1>
      <div className='flex gap-4'>
        <InputGroup className='w-50'>
          <Form.Control
            placeholder="Find by name..."
            aria-label="Find by name..."
            aria-describedby="basic-addon1"
            value={key}
            onChange={e => setKey(e.target.value)}
          />
          <Button variant="primary" onClick={handleSearch}>
            Search
          </Button>
        </InputGroup>
        <Button variant="primary" as={Link} to={'new'}>
          Create label
        </Button>
      </div>
      <Table striped bordered>
        <thead>
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Description</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {labels.map((label, index) => (
            <tr key={index}>
              <td>{label.id}</td>
              <td>{label.name}</td>
              <td>{label.description}</td>
              <td>
                {/* <Button className="btn btn-primary" as={Link} to={`/label/${label.id}`}>Edit</Button> {' '} */}
                <Button className="btn btn-primary" as={Link} to={`/label/${label.id}`}>Edit</Button> {' '}
                <Button className="btn btn-danger" onClick={() => handleDelete(label.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
}

export default LabelPage;