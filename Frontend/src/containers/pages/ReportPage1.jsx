import React, { useState, useEffect } from 'react';
import Layout4 from "hocs/Layouts/Layout4";
import axios from 'axios';

function ReportPage1() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState('');
    const [municipalities, setMunicipalities] = useState([]);
    const [selectedMunicipality, setSelectedMunicipality] = useState('');
    const [institutions, setInstitutions] = useState([]);
    const [selectedInstitution, setSelectedInstitution] = useState('');
    const [applicationType, setApplicationType] = useState('');

    const fetchProjects = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`);
            setProjects(response.data);
        } catch (error) {
            setError("Hubo un error al obtener los proyectos");
        }
    };

    const fetchMunicipalities = async (projectName) => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/municipios/?proyecto_id=${projectName}`);
            setMunicipalities(response.data);
            console.log(projectName);
        } catch (error) {
            setError("Hubo un error al obtener los municipios");
        }
    };

    const fetchInstitutions = async (projectName, municipalityName) => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/instituciones/?proyecto_id=${projectName}&municipio=${municipalityName}`);
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
            fetchMunicipalities(selectedProject);
            setSelectedMunicipality('');
            setSelectedInstitution('');
            setApplicationType('');
        }
    }, [selectedProject]);

    useEffect(() => {
        if (selectedProject && selectedMunicipality) {
            fetchInstitutions(selectedProject, selectedMunicipality);
            setSelectedInstitution('');
            setApplicationType('');
        }
    }, [selectedMunicipality]);

    const fetchData = async () => {
        if (!selectedProject || !selectedMunicipality || !selectedInstitution || !applicationType) {
            setError("Por favor, completa todas las selecciones");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/reporte1/?institucion=${selectedInstitution}&proyecto=${selectedProject}&aplicacion=${applicationType}`, {
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `reporte_${selectedInstitution}_${selectedProject}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            setError("Hubo un error al generar el reporte PDF");
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
                        onChange={(e) => setSelectedProject(e.target.value)}
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
                        <label htmlFor="municipio" style={styles.selectLabel}>Selecciona un Municipio</label>
                        <select
                            id="municipio"
                            value={selectedMunicipality}
                            onChange={(e) => setSelectedMunicipality(e.target.value)}
                            style={styles.select}
                        >
                            <option value="">-- Selecciona un municipio --</option>
                            {municipalities.map((municipio, index) => (
                                <option key={index} value={municipio}>
                                    {municipio}
                                </option>
                            ))}
                        </select>
                    </div>
                )}

                {selectedMunicipality && (
                    <div style={styles.selectContainer}>
                        <label htmlFor="institucion" style={styles.selectLabel}>Selecciona una Institución Educativa</label>
                        <select
                            id="institucion"
                            value={selectedInstitution}
                            onChange={(e) => setSelectedInstitution(e.target.value)}
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

                <button onClick={fetchData} disabled={loading || !selectedProject || !selectedMunicipality || !selectedInstitution || !applicationType} style={styles.button}>
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
