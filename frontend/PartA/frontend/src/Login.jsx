import React from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Form, Container, Col } from 'react-bootstrap';
import logo from './img/bigbrain_logo_1.png';
import { Formik, Field, ErrorMessage, Form as FormikForm } from 'formik';
import * as Yup from 'yup';
import {
  useNavigate,
} from 'react-router-dom';

const BACKEND_PORT = 5005;
// this file allows users to login
async function callLogin (email, password) {
  try {
    const response = await axios.post(`http://localhost:${BACKEND_PORT}/admin/auth/login`, {
      email,
      password,
    }, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });
    const token = response.data.token;
    localStorage.setItem('token', token);
    console.log('Token saved to local storage:', token);
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}

function Signin () {
  const navigate = useNavigate();
  const routeRegister = () => {
    navigate('/Register');
  };

  const validationSchema = Yup.object().shape({
    email: Yup.string().email('Invalid email').required('Required'),
    password: Yup.string().required('Required'),
  });

  const [loginError, setLoginError] = React.useState('');

  return (
    <>
      <Container>
        <Col lg={5} md={12} sm={12} className="p-5 m-auto">
          <Container className="pt-5">
            <div>
              <img src={logo} alt="bigbrain_logo" className="fluid mb-1 w-100" />
            </div>
            <Formik
              initialValues={{ email: '', password: '' }}
              validationSchema={validationSchema}
              onSubmit={async (values, { setSubmitting }) => {
                const loginSuccessful = await callLogin(values.email, values.password);
                setSubmitting(false);
                if (loginSuccessful) {
                  navigate('/Dashboard');
                } else {
                  setLoginError('Invalid email or password.');
                }
              }}
            >
              {({ isSubmitting }) => (
                <FormikForm noValidate className='bg-light rounded rounded-lg p-3 pt-1'>
                  <Form.Group className="mb-1" controlId="formEmail">
                    <Form.Label className="mb-1 w-100 login" style={{ fontFamily: 'Alfa Slab One', fontSize: '30px' }}>Login</Form.Label>
                    <Field as={Form.Control} type="email" name="email" placeholder="Enter email" required />
                    <ErrorMessage name="email" component="div" className="text-danger small" />
                  </Form.Group>
                  <Form.Group className="mb-3" controlId="formPassword">
                    <Field as={Form.Control} type="password" name="password" placeholder="Password" required />
                    <ErrorMessage name="password" component="div" className="text-danger small" />
                  </Form.Group>
                  {loginError && <div className="text-danger mb-2">{loginError}</div>}
                  <Button variant="dark" type="submit" className="w-100" disabled={isSubmitting}>
                    Login
                  </Button>
                </FormikForm>
              )}
            </Formik>
            <Button className="w-100 btn btn-link text-decoration-none" variant="Link" onClick={routeRegister} style={{ color: 'white' }}>
                No account? Register
            </Button>
          </Container>
        </Col>
      </Container>
    </>
  );
}

const Login = () => {
  return <Signin />
}

export default Login;
