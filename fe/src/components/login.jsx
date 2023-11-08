import React, { useState, useContext, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from './auth-context';
import { Button, Container, Form } from 'react-bootstrap';
import axios from 'axios';

const Login = () => {
  const { userIsAuthenticated, userLogin } = useContext(AuthContext);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const isLoggedIn = userIsAuthenticated();
    setLoggedIn(isLoggedIn);
  }, [userIsAuthenticated]);

  const handleInputChange = (e) => {
    if (e.target.name === 'username') {
      setUsername(e.target.value);
    } else if (e.target.name === 'password') {
      setPassword(e.target.value);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    setErrorMessage('');
    axios.post('http://localhost:5000/login', { username, password })
      .then((response) => {
        const user = response.data;

        userLogin(user);
        setUsername('');
        setPassword('');
        setLoggedIn(true);
      })
      .catch((error) => {
        console.log(error);
        setErrorMessage('Tài khoản hoặc mật khẩu không chính xác');
      });
  };

  if (isLoggedIn) {
    return <Navigate to={'/'} />;
  } else {
    return (
      <Container>
        <Form size='large' onSubmit={handleSubmit}>
          <Form.Group className='mb-3'>
            <Form.Label htmlFor='username'>Username</Form.Label>
            <Form.Control
              id='username'
              name='username'
              value={username}
              onChange={handleInputChange}
            />
            <Form.Label htmlFor='password'>Password</Form.Label>
            <Form.Control
              id='password'
              name='password'
              type='password'
              value={password}
              onChange={handleInputChange}
            />
          </Form.Group>
          <Button variant="primary" type="submit">
            Đăng nhập
          </Button>
        </Form>
        {errorMessage !== '' && <p>{errorMessage}</p>}
      </Container>
    );
  }
};

export default Login;