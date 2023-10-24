import axios from 'axios';
import React from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import { Navigate, useNavigate, useParams } from 'react-router-dom';

function LabelEdit() {
  const initialState = {
    id: '',
    name: '',
    description: ''
  };

  const { id } = useParams()
  const [label, setLabel] = React.useState(initialState)
  const navigate = useNavigate();
  
  React.useEffect(() => {
    if (id !== 'new') {
      axios.get(`http://localhost:5000/label/${id}`)
        .then(res => {
          setLabel(res.data)
        }).catch(err => {
          console.log(err)
        })
    }
  }, [])

  const handleChange = (event) => {
    setLabel({ ...label, [event.target.name]: event.target.value })
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    let checkError = false;
    if (id !== 'new') {
      await axios.post(`http://localhost:5000/label/${id}`, label)
        .catch(err => {
          checkError = true;
          console.log(err)
        })
    } else {
      await axios.post(`http://localhost:5000/label/new`, label)
        .catch(err => {
          checkError = true;
          console.log(err)
        })
    }
    if (!checkError)
      navigate('/label')
  }

  return (
    <div>
      <Container>
        <Form onSubmit={handleSubmit}>
          <Form.Group className='mb-3'>
            {id !== 'new' &&
              <>
                <Form.Label htmlFor="idLabel">Id</Form.Label>
                <Form.Control
                  id="idLabel"
                  value={label?.id}
                  className='required'
                  readOnly={true}
                />
              </>
            }
            <Form.Label htmlFor="nameLabel">Name</Form.Label>
            <Form.Control
              id="nameLabel"
              name="name"
              value={label?.name}
              onChange={handleChange}
            />
            <Form.Label htmlFor="descriptionLabel">Description</Form.Label>
            <Form.Control
              id="descriptionLabel"
              name="description"
              value={label?.description}
              onChange={handleChange}
            />
          </Form.Group>
          <Button variant="primary" type="submit">
            {id == 'new' ? 'Create' : 'Update'}
          </Button>
        </Form>
      </Container>
    </div>
  );
}

export default LabelEdit;