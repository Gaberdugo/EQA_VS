import React, { useState, useEffect } from 'react';
import Layout5 from "hocs/Layouts/Layout5";
import axios from 'axios';

function TerPrueba() {
    const [proyectos, setProyectos] = useState([]); // Lista de proyectos
    const [selectedPrueba, setSelectedPrueba] = useState(''); // Proyecto seleccionado
    const [loading, setLoading] = useState(false); // Para mostrar el estado de carga
    const [error, setError] = useState(''); // Para manejar errores
    const [reporte, setReporte] = useState(null); // Datos de la encuesta aleatoria

    // Obtener los proyectos de la API
    useEffect(() => {
        axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`)  // Usamos la variable de entorno para la URL base
            .then(response => {
                setProyectos(response.data);  // Guardamos los proyectos en el estado
            })
            .catch(err => {
                setError('Error al cargar los proyectos');
            });
    }, []);

    // Función para hacer la solicitud GET para obtener la encuesta aleatoria
    const fetchData = () => {
        if (!selectedPrueba) {
            setError('Por favor selecciona un proyecto');
            return;
        }

        setLoading(true);
        setError('');
        setReporte(null);

        // Realizar la solicitud GET para obtener la encuesta aleatoria (cambiamos el endpoint)
        axios.get(`${process.env.REACT_APP_API_URL}/res/respuesta/aleatoria/?nombre_proyecto=${selectedPrueba}`)
            .then(response => {
                // Si la solicitud es exitosa, almacenar los datos de la encuesta
                if (response.data.error) {
                    setError(response.data.error); // Mostrar el error si es retornado por la API
                } else {
                    setReporte(response.data);
                }
                setLoading(false);
            })
            .catch(err => {
                // Si hay un error, mostrar un mensaje
                setError('Error al obtener los datos. Intenta nuevamente.');
                setLoading(false);
            });
    };

    // Mapeo de las claves del reporte a sus títulos
    const fields = [
        { label: 'Proyecto', key: 'Proyecto' },
        { label: 'Fecha', key: 'Fecha' },
        { label: 'Ciudad', key: 'Ciudad' },
        { label: 'Departamento', key: 'Departamento' },
        { label: 'Colegio', key: 'Colegio' },
        { label: 'Nombre', key: 'Nombre' },
        { label: 'Edad', key: 'Edad' },
        { label: 'Prueba', key: 'Prueba' },
        { label: 'Grado', key: 'Grado' },
        { label: 'Genero', key: 'Genero' },
        { label: 'Cuadernillo', key: 'Cuadernillo' },
        { label: 'Respuesta 1', key: 'Respuesta 1' },
        { label: 'Respuesta 2', key: 'Respuesta 2' },
        { label: 'Respuesta 3', key: 'Respuesta 3' },
        { label: 'Respuesta 4', key: 'Respuesta 4' },
        { label: 'Respuesta 5', key: 'Respuesta 5' },
        { label: 'Respuesta 6', key: 'Respuesta 6' },
        { label: 'Respuesta 7', key: 'Respuesta 7' },
        { label: 'Respuesta 8', key: 'Respuesta 8' },
        { label: 'Respuesta 9', key: 'Respuesta 9' },
        { label: 'Respuesta 10', key: 'Respuesta 10' },
        { label: 'Respuesta 11', key: 'Respuesta 11' },
        { label: 'Respuesta 12', key: 'Respuesta 12' },
        { label: 'Respuesta 13', key: 'Respuesta 13' },
        { label: 'Respuesta 14', key: 'Respuesta 14' },
        { label: 'Respuesta 15', key: 'Respuesta 15' },
        { label: 'Respuesta 16', key: 'Respuesta 16' },
        { label: 'Respuesta 17', key: 'Respuesta 17' },
        { label: 'Respuesta 18', key: 'Respuesta 18' },
        { label: 'Respuesta 19', key: 'Respuesta 19' },
        { label: 'Respuesta 20', key: 'Respuesta 20' },
    ];

    return (
        <Layout5>
            <div style={styles.container}>
                <h1 style={styles.title}>Verificador de Pruebas</h1>

                {/* Selector de proyectos */}
                <div style={styles.selectContainer}>
                    <label htmlFor="prueba" style={styles.selectLabel}>Selecciona un Proyecto</label>
                    <select
                        id="prueba"
                        value={selectedPrueba}
                        onChange={(e) => setSelectedPrueba(e.target.value)} // Actualiza la prueba seleccionada
                        style={styles.select}
                    >
                        <option value="">-- Seleccione un proyecto --</option>
                        {proyectos.map((proyecto) => (
                            <option key={proyecto.id} value={proyecto.nombre}>
                                {proyecto.nombre}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Botón para hacer la solicitud GET */}
                <button onClick={fetchData} disabled={loading || !selectedPrueba} style={styles.button}>
                    {loading ? "Cargando..." : "Obtener prueba"}
                </button>

                {/* Mostrar error si ocurre alguno */}
                {error && <p style={styles.errorText}>{error}</p>}

                {/* Mostrar los datos de la encuesta aleatoria */}
                {reporte && (
                    <div style={styles.reportContainer}>
                        <h2>Datos de la prueba aleatoria</h2>
                        <div style={styles.tableWrapper}>
                            <table style={styles.table}>
                                <thead>
                                    <tr>
                                        <th style={styles.tableHeader}>Campo</th>
                                        <th style={styles.tableHeader}>Valor</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {fields.map(field => (
                                        <tr key={field.key}>
                                            <td style={styles.tableCell}>{field.label}</td>
                                            <td style={styles.tableCell}>{reporte[field.key]}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>
        </Layout5>
    );
}

// Estilos en línea para centrado y colores personalizados
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
    selectContainer: {
        marginBottom: '20px',
    },
    selectLabel: {
        color: '#1B8830',
        fontSize: '1rem',
        marginBottom: '10px',
    },
    select: {
        padding: '10px',
        fontSize: '1rem',
        border: '1px solid #ccc',
        borderRadius: '5px',
    },
    button: {
        backgroundColor: '#1B8830',
        color: 'white',
        border: 'none',
        padding: '10px 20px',
        fontSize: '1rem',
        cursor: 'pointer',
        borderRadius: '5px',
        transition: 'background-color 0.3s',
    },
    errorText: {
        color: 'red',
        fontSize: '1rem',
        marginTop: '10px',
    },
    reportContainer: {
        marginTop: '30px',
        width: '100%',
        maxWidth: '900px',
    },
    tableWrapper: {
        overflowY: 'auto', // Habilita el scroll vertical
        maxHeight: '400px', // Establece la altura máxima para la tabla
        marginTop: '20px', // Para algo de separación
    },
    table: {
        width: '100%',
        borderCollapse: 'collapse',
    },
    tableHeader: {
        backgroundColor: '#1B8830',
        color: 'white',
        padding: '12px 15px',
        textAlign: 'left',
    },
    tableCell: {
        padding: '12px 15px',
        border: '1px solid #ddd',
        textAlign: 'left',
    },
};

export default TerPrueba;
