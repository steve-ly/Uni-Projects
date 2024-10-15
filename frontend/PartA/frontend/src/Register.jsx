import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Form, Container, Col } from 'react-bootstrap';
import React from 'react';
import axios from 'axios';
import logo from './img/bigbrain_logo_1.png';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';

const BACKEND_PORT = 5005;
// Allows admins to signup
async function callRegister (email, password, name) {
  try {
    const response = await axios.post(`http://localhost:${BACKEND_PORT}/admin/auth/register`, {
      email,
      password,
      name,
    }, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json',
      },
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

function Signup () {
  const navigate = useNavigate();

  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Name is required'),
    email: Yup.string().email('Invalid email format').required('Email is required'),
    password: Yup.string()
      .min(8, 'Password must be at least 8 characters')
      .required('Password is required'),
  });

  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      password: '',
    },
    validationSchema,
    onSubmit: async (values, { setSubmitting, setErrors }) => {
      const signupSuccessful = await callRegister(values.email, values.password, values.name);
      if (signupSuccessful) {
        navigate('/Dashboard');
      } else {
        setErrors({ server: 'Registration failed. Please try again.' });
      }
      setSubmitting(false);
    },
  });

  const routeLogin = () => {
    navigate('/Login');
  };

  return (
    <>
      <Container>
        <Col lg={6} md={12} sm={12} className="p-5 m-auto">
          <Container className="pt-5">
            <div>
              <img src={logo} alt="bigbrain_logo" className="fluid mb-1 w-100" />
            </div>
            <Form noValidate onSubmit={formik.handleSubmit} className="bg-light rounded rounded-lg p-3 pt-1">
              <Form.Label className="mb-1 w-100" style={{ fontFamily: 'Alfa Slab One', fontSize: '30px' }}>
                Register
              </Form.Label>
              <Form.Group className="mb-3" controlId="formName">
                <Form.Control
                  type="text"
                  placeholder="Enter name"
                  name="name"
                  value={formik.values.name}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  isInvalid={formik.touched.name && formik.errors.name}
                />
                <Form.Control.Feedback type="invalid">{formik.errors.name}</Form.Control.Feedback>
              </Form.Group>
              <Form.Group className="mb-3" controlId="formEmail">
                <Form.Control
                  type="email"
                  placeholder="Enter email"
                  name="email"
                  value={formik.values.email}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  isInvalid={formik.touched.email && formik.errors.email}
                />
                <Form.Control.Feedback type="invalid">{formik.errors.email}</Form.Control.Feedback>
              </Form.Group>
              <Form.Group className="mb-3" controlId="formPassword">
                <Form.Control
                  type="password"
                  placeholder="Password"
                  name="password"
                  value={formik.values.password}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  isInvalid={formik.touched.password && formik.errors.password}
                />
                <Form.Control.Feedback type="invalid">{formik.errors.password}</Form.Control.Feedback>
              </Form.Group>
              {formik.errors.server && (
                <div className="alert alert-danger" role="alert">
                  {formik.errors.server}
                </div>
              )}
              <Button variant="dark" type="submit" className="w-100" disabled={formik.isSubmitting}>
                Register
              </Button>
            </Form>
            <Button className="w-100 btn btn-link text-decoration-none" variant="Link" onClick={routeLogin} style={{ color: 'white' }}>
              Already a Brainiac? Sign in!
            </Button>
          </Container>
        </Col>
      </Container>
    </>
  );
}

const Register = () => {
  return <Signup />;
};

export default Register;
