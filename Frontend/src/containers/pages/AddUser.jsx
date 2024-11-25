import React, { useState } from 'react';
import AdminNav from 'components/navigation/AdminNav';
import Footer from 'components/navigation/Footer';
import Layout from 'hocs/Layouts/Layout';
import '../../styles/addUser.css';

function AddUser() {
    const [username, setUsername] = useState('');
    const [role, setRole] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!username || !role || !password) {
            setError('Por favor, completa todos los campos.');
            return;
        }

        // Aquí iría la lógica para enviar los datos al servidor
        console.log('Agregando usuario:', { username, role, password });
        setError(''); // Reiniciar error si todo está bien

        // Aquí puedes agregar la lógica para limpiar los campos después de enviar
        setUsername('');
        setRole('');
        setPassword('');
    };

    return (
        <Layout>
            <AdminNav />
            <div className="add-user-container pt-40">
                <h2 className="add-user-title">Agregar Usuario</h2>
                {error && <p className="error-message">{error}</p>}
                <form onSubmit={handleSubmit} className="add-user-form">
                    <div className="form-group">
                        <label htmlFor="username">Nombre de Usuario</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="form-input"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="role">Rol</label>
                        <input
                            type="text"
                            id="role"
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            className="form-input"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Contraseña</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="form-input"
                            required
                        />
                    </div>
                    <button type="submit" className="add-user-button">Agregar Usuario</button>
                </form>
            </div>
            <Footer />
        </Layout>
    );
}

export default AddUser;