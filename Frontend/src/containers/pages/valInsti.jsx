import React, { useState } from 'react';
import Layout4 from "hocs/Layouts/Layout4";
import axios from 'axios';

function valInsti() {
    const [nombre, setNombre] = useState('');
    const [dane, setDane] = useState('');
    const [mensaje, setMensaje] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMensaje('');
        setError('');

        try {
            const response = await axios.post(`${process.env.REACT_APP_API_URL}/res/crearinsti/`, {
                nombre: nombre,
                DANE: dane,
            });

            setMensaje('Institución creada con éxito.');
            setNombre('');
            setDane('');
        } catch (err) {
            setError('Hubo un error al crear la institución.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout4>
            <div style={styles.container}>
                <h1 style={styles.title}>Crear Institución Educativa</h1>

                <form onSubmit={handleSubmit} style={styles.form}>
                    <label style={styles.label}>Nombre de la Institución</label>
                    <input
                        type="text"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        style={styles.input}
                        required
                    />

                    <label style={styles.label}>Código DANE</label>
                    <input
                        type="number"
                        value={dane}
                        onChange={(e) => setDane(e.target.value)}
                        style={styles.input}
                        required
                    />

                    <button type="submit" style={styles.button} disabled={loading}>
                        {loading ? 'Creando...' : 'Crear Institución'}
                    </button>
                </form>

                {mensaje && <p style={styles.success}>{mensaje}</p>}
                {error && <p style={styles.error}>{error}</p>}
            </div>
        </Layout4>
    );
}

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '90vh',
        backgroundColor: '#F8F8F8',
        padding: '20px',
    },
    title: {
        color: '#1B8830',
        fontSize: '2rem',
        marginBottom: '20px',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
        width: '300px',
    },
    label: {
        fontSize: '1rem',
        color: '#1B8830',
    },
    input: {
        padding: '10px',
        fontSize: '1rem',
        border: '1px solid #ccc',
        borderRadius: '5px',
    },
    button: {
        backgroundColor: '#1B8830',
        color: 'white',
        border: 'none',
        padding: '10px',
        fontSize: '1rem',
        cursor: 'pointer',
        borderRadius: '5px',
    },
    success: {
        marginTop: '20px',
        color: 'green',
        fontWeight: 'bold',
    },
    error: {
        marginTop: '20px',
        color: 'red',
        fontWeight: 'bold',
    },
};

export default valInsti;
