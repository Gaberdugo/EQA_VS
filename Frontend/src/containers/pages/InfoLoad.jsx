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
        <h1 style={{ color: '#666666' }}>Cargue Prueba EQA</h1>

        {/* Si el formulario fue enviado correctamente, mostrar el mensaje de éxito */}
        {mensajeExito && (
          <div style={{ color: 'green', marginBottom: '15px' }}>
            <strong>{mensajeExito}</strong>
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <select
            name="nombreProyecto"
            value={formData.nombreProyecto}
            onChange={handleChange}
            style={{ flex: '1', marginRight: '10px' }}
          >
            <option value="">Seleccione un proyecto</option>
            {proyectos.length > 0 && proyectos.map(proyecto => (
              <option key={proyecto.id} value={proyecto.nombre}>
                {proyecto.nombre}
              </option>
            ))}
          </select>

          <input
            type="date"
            name="fechaAplicacion"
            value={formData.fechaAplicacion}
            onChange={handleChange}
            onInput={(e) => {
              const input = e.target.value;
              const year = input.split("-")[0]; // Extrae el año
              if (year.length > 4) {
                e.target.value = input.slice(0, 4) + input.slice(5); // Limita el año a 4 caracteres
              }
            }}
            style={{ flex: '1' }}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <select
            name="ciudad"
            value={formData.ciudad}
            onChange={handleChange}
            style={{ flex: '1', marginRight: '10px' }}
            disabled={ciudades.length === 0}
          >
            <option value="">Seleccione una ciudad</option>
            {ciudades.length > 0 && ciudades.map((ciudad, index) => (
              <option key={index} value={ciudad.nombreProyecto}> {/* Cambié 'nombre' por 'nombreProyecto' */}
                {ciudad.nombreProyecto}
              </option>
            ))}
          </select>

          <input
            type="text"
            placeholder="Departamento"
            name="departamento"
            value={formData.departamento}
            readOnly
            style={{ flex: '1', marginRight: '10px' }}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <label style={{ marginRight: '10px', flex: '1' }}>
            Aplicación:
            <select
              name="apli"
              value={formData.apli}
              onChange={handleChange}
              style={{ marginLeft: '5px', width: '100%' }}
            >
              <option value="">Seleccione</option>
              <option value="entrada">Entrada</option>
              <option value="salida">Salida</option>
            </select>
          </label>
          <label style={{ marginRight: '10px', flex: '1' }}>
            Prueba:
            <select
              name="prueba"
              value={formData.prueba}
              onChange={handleChange}
              style={{ marginLeft: '5px', width: '100%' }}
            >
              <option value="">Seleccione</option>
              <option value="Matemáticas">Matemáticas</option>
              <option value="Lenguaje">Lenguaje</option>
            </select>
          </label>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <input
            type="text"
            placeholder="Nombre Institución Educativa"
            name="nombreInstitucion"
            value={formData.nombreInstitucion}
            onChange={handleChange}
            style={{ flex: '1', marginRight: '10px' }}
          />
          <select
            name="numeroCuadernillo"
            value={formData.numeroCuadernillo}
            onChange={handleChange}
            style={{ flex: '1' }}
          >
            <option value="">Seleccione un cuadernillo</option>
            {cuadernillos.map((nombre, index) => (
              <option key={index} value={nombre}>
                {nombre}
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <input
            type="text"
            placeholder="Nombre del Estudiante"
            name="nombreEstudiante"
            value={formData.nombreEstudiante}
            onChange={handleChange}
            style={{ flex: '1', marginRight: '10px' }}
          /> 
          <input
            type="text"
            placeholder="Documento del Estudiante"
            name="tiEstudiante"
            value={formData.tiEstudiante}
            onChange={handleChange}
            style={{ flex: '1' }}
          />
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <label style={{ marginRight: '10px', flex: '1' }}>
            Grado:
            <select
              name="grado"
              value={formData.grado}
              onChange={handleChange}
              style={{ marginLeft: '5px', width: '100%' }}
            >
              <option value="">Seleccione</option>
              <option value="Tercero">Tercero</option>
              <option value="Quinto">Quinto</option>
            </select>
          </label>
          <label style={{ marginRight: '10px', flex: '1' }}>
            Género:
            <select
              name="genero"
              value={formData.genero}  
              onChange={handleChange}
              style={{ marginLeft: '5px', width: '100%' }}
            >
              <option value="">Seleccione</option>
              <option value="Masculino">Masculino</option>
              <option value="Femenino">Femenino</option>
              <option value="No responde">No responde</option>
            </select>
          </label>
          <label style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            Fecha de nacimiento:
            <input
              type="date"
              name="edad"
              value={formData.edad}
              onChange={handleChange}
              onInput={(e) => {
                const input = e.target.value;
                const year = input.split("-")[0]; // Extrae el año
                if (year.length > 4) {
                  e.target.value = input.slice(0, 4) + input.slice(5); // Limita el año a 4 caracteres
                }
              }}
              style={{ flex: '1' }}
            />
          </label>
        </div>

        <h2 style={{ color: '#B3B3B3' }}>Respuestas</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <tbody>
            {Array.from({ length: 5 }, (_, rowIndex) => (
              <tr key={rowIndex}>
                {Array.from({ length: 4 }, (_, colIndex) => {
                  const index = rowIndex * 4 + colIndex; // Calcular el índice de la respuesta
                  return (
                    <td key={colIndex} style={{ padding: '5px', border: '1px solid #ccc' }}>
                      <label>
                        Respuesta {index + 1}:
                        <select
                          name={`respuesta${index}`}
                          value={formData.respuestas[index]}
                          onChange={handleChange}
                          style={{ width: '100%' }}
                        >
                          <option value="">Seleccione</option>
                          <option value="A" translate="no">A</option>
                          <option value="B" translate="no">B</option>
                          <option value="C" translate="no">C</option>
                          <option value="D" translate="no">D</option>
                          <option value="Blanco" translate="no">Blanco</option>
                          <option value="Multi Marca" translate="no">Multi Marca</option>
                        </select>
                      </label>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>

        <button
          type="submit"
          style={buttonStyle}
          disabled={!isFormComplete()} // Deshabilitar si el formulario no está completo
        >
          Enviar
        </button>

        {!isFormComplete() && (
          <p style={{ color: 'red', marginTop: '10px' }}>Por favor, complete todos los campos antes de enviar.</p>
        )}
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
