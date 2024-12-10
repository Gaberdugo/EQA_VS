import React, { useEffect, useState } from 'react';
import { Link, Navigate, useAuth } from 'react-router-dom';
import { connect } from 'react-redux';
import Footer from 'components/navigation/Footer';
import Layout from 'hocs/Layouts/Layout';
import '../../styles/login.css';
import { login } from 'redux/actions/login/auth';

function Login({
    login,
    isAuthenticated,
    loading
}){

    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });

    const {
        email,
        password
    } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value});

    const onSubmit = e => {
        e.preventDefault();
        login(email, password)
    }

    if(isAuthenticated){
        const role = localStorage.getItem('role');
        if (role === 'admin') {
            return <Navigate to='/admin' />;
        } else if (role === 'digitador') {
            return <Navigate to='/digi' />;
        } else if (role === 'val') {
            return <Navigate to='/valPage' />
        } else if (role === 'terpel') {
            return <Navigate to='/terPage' />
        }
    }

    return (
        <Layout>
            <div className="login-container">
                <h1 className="login-title">Iniciar Sesión</h1>
                <form onSubmit={e=>{onSubmit(e)}} className="login-form">
                    <div className="form-group">
                        <label htmlFor="username">Correo</label>
                        <input
                            id="email-address"
                            name="email"
                            value={email}
                            type="email"
                            required
                            onChange={(e) => onChange(e)}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Contraseña</label>
                        <input
                            id="password"
                            name="password"
                            value={password}
                            type="password"
                            required
                            onChange={(e) => onChange(e)}
                        />
                    </div>
                    <button type="submit" className="login-button">Ingresar</button>
                </form>
                <Link to="/" className="home-button">Regresar a Inicio</Link> {/* Botón de regresar */}
            </div>
            <Footer/>
        </Layout> 
    );
}
const mapStateToProps=state=>({
    isAuthenticated: state.auth.isAuthenticated,
    loading: state.auth.loading
})
export default connect(mapStateToProps,{
    login
}) (Login);