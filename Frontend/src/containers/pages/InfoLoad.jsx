import Layout3 from "hocs/Layouts/Layout3";
import React, { useState, useEffect } from 'react';
import { connect } from "react-redux";
import { getProyectos, postProyecto } from 'redux/actions/info/info';
import axios from "axios";

function InfoLoad({ 
  getProyectos, proyectos, loading, error, postProyecto 
}) {
  const [formData, setFormData] = useState({
    responsable: '',
    nombreProyecto: '',
    ciudad: '',
    departamento: '',
    fechaAplicacion: '',
    apli: '',
    prueba: '',
    nombreInstitucion: '',
    numeroCuadernillo: '',
    nombreEstudiante: '',
    tiEstudiante: '',
    grado: '',
    genero: '', 
    edad: '',
    fecha_carge: '',
    respuestas: Array(20).fill(''),
  });

  const [ciudades, setCiudades] = useState([]);
  const [cuadernillos, setCuadernillos] = useState([]);
  const [mensajeExito, setMensajeExito] = useState('');

  useEffect(() => {
    getProyectos();

    const info = localStorage.getItem('proyectos');
    const proyectos = info ? JSON.parse(info) : [];

    if (proyectos.length > 0 && !formData.nombreProyecto) {
      setFormData(prevState => ({
        ...prevState,
        nombreProyecto: '',
      }));
    }

    const fetchCuadernillos = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/cuader/`);
        const data = Array.isArray(response.data) ? response.data : [];
        setCuadernillos(data);
      } catch (error) {
        console.error("Error al obtener los cuadernillos:", error);
        setCuadernillos([]);
      }
    };

    fetchCuadernillos();
  }, [getProyectos]);

  function formatDateToSQL(isoString) {
    const date = new Date(isoString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  }

  useEffect(() => {
    if (formData.nombreProyecto) {
      const proyectoSeleccionado = proyectos.find(p => p.nombre === formData.nombreProyecto);
      if (proyectoSeleccionado) {
        setCiudades(proyectoSeleccionado.ciudades);
      }
    } else {
      setCiudades([]);
    }
  }, [formData.nombreProyecto, proyectos]);

  const isFormComplete = () => {
    const fields = [
      'nombreProyecto', 'ciudad', 'departamento', 'fechaAplicacion',
      'apli', 'prueba', 'nombreInstitucion', 'numeroCuadernillo',
      'nombreEstudiante', 'grado', 'genero'
    ];

    for (let field of fields) {
      if (!formData[field]) return false;
    }

    for (let respuesta of formData.respuestas) {
      if (!respuesta) return false;
    }

    return true;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name.startsWith('respuesta')) {
      const index = parseInt(name.replace('respuesta', ''), 10);
      setFormData(prevState => {
        const newRespuestas = [...prevState.respuestas];
        newRespuestas[index] = value;
        return { ...prevState, respuestas: newRespuestas };
      });
    } else {
      setFormData(prevState => {
        const newFormData = { ...prevState, [name]: value };

        if (name === 'ciudad') {
          const ciudadSeleccionada = ciudades.find(c => c.nombre === value);
          newFormData.departamento = ciudadSeleccionada ? ciudadSeleccionada.departamento : '';
        }

        return newFormData;
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const isoDate = new Date();
    const formattedDate = formatDateToSQL(isoDate);
    const correo = localStorage.getItem('correo');
    const documentoEstudiante = Math.floor(Math.random() * 10_000_000_001).toString();

    const respuestasObj = {};
    formData.respuestas.forEach((respuesta, index) => {
      respuestasObj[`respuesta_${index + 1}`] = respuesta;
    });

    const proyectoData = {
      responsable: correo,
      nombre: formData.nombreProyecto,
      fecha: formData.fechaAplicacion,
      ciudad: formData.ciudad,
      departamento: formData.departamento,
      aplicacion: formData.apli,
      prueba: formData.prueba,
      nombre_institucion: formData.nombreInstitucion,
      numero_cuadernillo: formData.numeroCuadernillo,
      nombre_estudiante: formData.nombreEstudiante,
      documento_estudiante: documentoEstudiante,
      grado: formData.grado,
      edad: formData.edad,
      genero: formData.genero,
      fecha_cargue: formattedDate,
      ...respuestasObj,
    };

    postProyecto(proyectoData)
      .then(() => {
        setMensajeExito('La información fue cargada correctamente.');
        setTimeout(() => {
          setFormData(prevState => ({
            ...prevState,
            numeroCuadernillo: '',
            nombreEstudiante: '',
            tiEstudiante: '',
            grado: '',
            genero: '',
            edad: '',
            respuestas: Array(20).fill(''),
          }));
          setMensajeExito('');
        }, 2000);
      })
      .catch(error => {
        if (error.response) {
          alert(`Error al cargar la encuesta: ${error.response.data.error}`);
        } else {
          alert('Error de conexión o servidor');
        }
      });
  };

  const buttonStyle = {
    width: '100%',
    padding: '10px',
    backgroundColor: '#1B8830',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: isFormComplete() ? 'pointer' : 'not-allowed',
    transition: 'background-color 0.3s',
  };

  const formContainerStyle = {
    maxHeight: '100vh',
    overflowY: 'auto',
    padding: '15px',
    backgroundColor: '#A4D7B2',
    borderRadius: '8px',
  };

  return (
    <Layout3>
      <form onSubmit={handleSubmit} style={formContainerStyle}>
        {/* Tu JSX permanece sin cambios desde aquí */}
        {/* ... */}
      </form>
    </Layout3>
  );
}

const mapStateToProps = (state) => ({
  proyectos: state.proyectos.data || [],
  loading: state.proyectos.loading,
  error: state.proyectos.error,
});

const mapDispatchToProps = {
  getProyectos,
  postProyecto
};

export default connect(mapStateToProps, mapDispatchToProps)(InfoLoad);
