import axios from 'axios';
import React from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import { Navigate, useNavigate, useParams } from 'react-router-dom';
import { useAuth } from './auth-context';

function LabelEdit() {
  const initialState = {
    id: undefined,
    name: '',
    description: ''
  };

  const { id } = useParams()
  const [label, setLabel] = React.useState(initialState)
  const navigate = useNavigate();
  const { getUser } = useAuth()
  const user = getUser()
  
  React.useEffect(() => {
    if (id !== 'new') {
      axios.get(`http://localhost:5000/label/${id}`, {
        auth: user
      })
        .then(res => {
          setLabel(res.data)
        }).catch(err => {
          console.log(err)
          alert('Get failed. Please try again.');
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
      await axios.put(`http://localhost:5000/label`, label, {
        auth: user
      })
        .then(() => {
          window.alert('Ok')
        }).catch(err => {
          checkError = true;
          console.log(err)
          alert('Update failed. Please try again.');
        })
    } else {
      await axios.post(`http://localhost:5000/label/new`, label, {
        auth: user
      })
        .then(() => {
          window.alert('Ok')
        }).catch(err => {
          checkError = true;
          console.log(err)
          alert('Create failed. Please try again.');
        })
    }
    if (!checkError)
      navigate('/label')
  }

  return (
    <div>
      <Container>
        <h1 className="mb-4">Label</h1>
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