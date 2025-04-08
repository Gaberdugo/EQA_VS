import React, { useState, useEffect } from 'react';
import Layout4 from "hocs/Layouts/Layout4";
import axios from 'axios';

function ReportPage2() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [projects, setProjects] = useState([]); // Lista de proyectos
    const [selectedProject, setSelectedProject] = useState(''); // Proyecto seleccionado

    // Función para obtener la lista de proyectos
    const fetchProjects = async () => {
        try {
            // Suponiendo que la API devuelve los proyectos
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`); // Cambia la URL según corresponda
            setProjects(response.data);
        } catch (error) {
            setError("Hubo un error al obtener los proyectos");
        }
    };

    // Llamada a la API para obtener los proyectos cuando el componente se monta
    useEffect(() => {
        fetchProjects();
    }, []);

    // Función para manejar el click en el botón y hacer la solicitud GET para el reporte
    const fetchData = async () => {
        if (!selectedProject) {
            setError("Por favor, selecciona un proyecto");
            return;
        }

        setLoading(true);
        setError(null); // Limpiar cualquier error previo

        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/respuesta/exportar/?nombre_proyecto=${selectedProject}`, {
                responseType: 'blob', // Esto es lo que cambia para manejar un archivo binario
            });

            // Crear un enlace temporal para descargar el archivo
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `reporte_general.xlsx`); // El nombre que quieres para el archivo descargado
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            setError("Hubo un error al obtener los datos");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout4>
            <div style={styles.container}>
                <h1 style={styles.title}>Generador de Reportes Generales</h1>

                {/* Selector de proyectos */}
                <div style={styles.selectContainer}>
                    <label htmlFor="proyecto" style={styles.selectLabel}>Selecciona un Proyecto</label>
                    <select
                        id="proyecto"
                        value={selectedProject}
                        onChange={(e) => setSelectedProject(e.target.value)}  // Ahora capturamos el nombre
                        style={styles.select}
                    >
                        <option value="">-- Selecciona un proyecto --</option>
                        {projects.map((project) => (
                            <option key={project.id} value={project.nombre}> {/* Pasamos el nombre aquí */}
                                {project.nombre}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Botón para hacer la solicitud GET */}
                <button onClick={fetchData} disabled={loading || !selectedProject} style={styles.button}>
                    {loading ? "Cargando..." : "Obtener Reporte"}
                </button>

                {/* Mostrar error si ocurre alguno */}
                {error && <p style={styles.errorText}>{error}</p>}
            </div>
        </Layout4>
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
};

export default ReportPage2;