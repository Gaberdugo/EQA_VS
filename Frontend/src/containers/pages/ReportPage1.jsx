import React, { useState, useEffect } from 'react';
import Layout4 from "hocs/Layouts/Layout4";
import axios from 'axios';

function ReportPage1() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState('');
    const [institutions, setInstitutions] = useState([]);
    const [selectedInstitution, setSelectedInstitution] = useState('');
    const [applicationType, setApplicationType] = useState(''); // Nueva variable para Entrada o Salida

    const fetchProjects = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`);
            setProjects(response.data);
        } catch (error) {
            setError("Hubo un error al obtener los proyectos");
        }
    };

    const fetchInstitutions = async (projectName) => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/instituciones/?proyecto_id=${projectName}`);
            setInstitutions(response.data);
        } catch (error) {
            setError("Hubo un error al obtener las instituciones educativas");
        }
    };

    useEffect(() => {
        fetchProjects();
    }, []);

    useEffect(() => {
        if (selectedProject) {
            fetchInstitutions(selectedProject);
        }
    }, [selectedProject]);

    const fetchData = async () => {
        if (!selectedProject || !selectedInstitution || !applicationType) {
            setError("Por favor, selecciona un proyecto, una institución educativa y el tipo de aplicación");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/respuesta/exportar/?nombre_proyecto=${selectedProject}&nombre_institucion=${selectedInstitution}&tipo_aplicacion=${applicationType}`, {
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `reporte_general.xlsx`);
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
                <h1 style={styles.title}>Generador de Reportes por Institución</h1>

                <div style={styles.selectContainer}>
                    <label htmlFor="proyecto" style={styles.selectLabel}>Selecciona un Proyecto</label>
                    <select
                        id="proyecto"
                        value={selectedProject}
                        onChange={(e) => {
                            setSelectedProject(e.target.value);
                            setSelectedInstitution('');
                            setApplicationType('');
                        }}
                        style={styles.select}
                    >
                        <option value="">-- Selecciona un proyecto --</option>
                        {projects.map((project) => (
                            <option key={project.id} value={project.nombre}>
                                {project.nombre}
                            </option>
                        ))}
                    </select>
                </div>

                {selectedProject && (
                    <div style={styles.selectContainer}>
                        <label htmlFor="institucion" style={styles.selectLabel}>Selecciona una Institución Educativa</label>
                        <select
                            id="institucion"
                            value={selectedInstitution}
                            onChange={(e) => {
                                setSelectedInstitution(e.target.value);
                                setApplicationType('');
                            }}
                            style={styles.select}
                        >
                            <option value="">-- Selecciona una institución --</option>
                            {institutions.map((institution, index) => (
                                <option key={index} value={institution}>
                                    {institution}
                                </option>
                            ))}
                        </select>
                    </div>
                )}

                {/* Nuevo selector para tipo de aplicación */}
                {selectedInstitution && (
                    <div style={styles.selectContainer}>
                        <label htmlFor="tipoAplicacion" style={styles.selectLabel}>Selecciona el Tipo de Aplicación</label>
                        <select
                            id="tipoAplicacion"
                            value={applicationType}
                            onChange={(e) => setApplicationType(e.target.value)}
                            style={styles.select}
                        >
                            <option value="">-- Selecciona un tipo --</option>
                            <option value="Entrada">Entrada</option>
                            <option value="Salida">Salida</option>
                        </select>
                    </div>
                )}

                <button onClick={fetchData} disabled={loading || !selectedProject || !selectedInstitution || !applicationType} style={styles.button}>
                    {loading ? "Cargando..." : "Obtener Reporte"}
                </button>

                {error && <p style={styles.errorText}>{error}</p>}
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

export default ReportPage1;
