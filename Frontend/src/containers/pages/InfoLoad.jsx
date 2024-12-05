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
    genero: '',  // Cambié 'sexo' por 'genero'
    edad: '',
    fechacargue: '',
    respuestas: Array(20).fill(''), // Respuestas independientes
  });

  const [ciudades, setCiudades] = useState([]);  // Estado para almacenar las ciudades
  const [cuadernillos, setCuadernillos] = useState([]); // Estado para almacenar los cuadernillos
  const [mensajeExito, setMensajeExito] = useState(''); // Estado para mostrar mensaje de éxito

  // Llamada para obtener proyectos cuando se monta el componente
  useEffect(() => {
    getProyectos(); // Llamamos a la acción para obtener los proyectos de la API

    // Verificamos si hay proyectos en localStorage y si es así, actualizamos el estado
    const info = localStorage.getItem('proyectos');
    const proyectos = info ? JSON.parse(info) : [];

    if (proyectos.length > 0 && !formData.nombreProyecto) {
      // Si hay proyectos y el nombre del proyecto aún no se ha seleccionado
      setFormData(prevState => ({
        ...prevState,
        nombreProyecto: '',  // Asegúrate de que el valor inicial sea vacío para mostrar la opción predeterminada
      }));
    }

    // Llamada para obtener cuadernillos
    const fetchCuadernillos = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/res/cuader/`); // Endpoint para los cuadernillos
        console.log("Datos recibidos:", response.data);
        const data = Array.isArray(response.data) ? response.data : []; // Asegúrate de que sea un arreglo
        setCuadernillos(data); // Guardar los nombres de cuadernillos
      } catch (error) {
        console.error("Error al obtener los cuadernillos:", error);
        setCuadernillos([]); // Asegúrate de manejar errores
      }
    };

    fetchCuadernillos();
  }, [getProyectos]);

  // Este useEffect se activa cuando el nombre del proyecto cambia
  useEffect(() => {
    if (formData.nombreProyecto) {
      // Buscar el proyecto seleccionado
      const proyectoSeleccionado = proyectos.find(proyecto => proyecto.nombre === formData.nombreProyecto);

      if (proyectoSeleccionado) {
        setCiudades(proyectoSeleccionado.ciudades); // Actualizamos las ciudades con las del proyecto
      }
    } else {
      setCiudades([]);  // Si no hay proyecto seleccionado, limpiamos las ciudades
    }
  }, [formData.nombreProyecto, proyectos]);

  const isFormComplete = () => {
    const fields = [
      'nombreProyecto', 'ciudad', 'departamento', 'fechaAplicacion',
      'apli', 'prueba', 'nombreInstitucion', 'numeroCuadernillo',
      'nombreEstudiante', 'grado', 'genero', 'edad'
    ];

    // Verificar que todos los campos de texto estén llenos
    for (let field of fields) {
      if (!formData[field]) return false;
    }

    // Verificar que todas las respuestas estén seleccionadas
    for (let respuesta of formData.respuestas) {
      if (!respuesta) return false;
    }

    return true;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Si el nombre del campo es uno de los select de respuestas (respuesta0, respuesta1, etc.)
    if (name.startsWith('respuesta')) {
      const index = parseInt(name.replace('respuesta', ''), 10);  // Extraemos el índice de la respuesta (ej. respuesta0 -> 0)

      // Actualizamos solo el campo de respuestas
      setFormData(prevState => {
        const newRespuestas = [...prevState.respuestas];  // Copiamos el array de respuestas
        newRespuestas[index] = value;  // Actualizamos la respuesta correspondiente en el índice
        return { ...prevState, respuestas: newRespuestas };  // Retornamos el nuevo estado con las respuestas actualizadas
      });
    } else {
      // Para los demás campos, como ciudad, departamento, etc.
      setFormData(prevState => {
        const newFormData = {
          ...prevState,
          [name]: value,  // Actualizamos el valor del campo correspondiente
        };

        // Si se selecciona una ciudad, actualizamos el departamento
        if (name === 'ciudad') {
          const ciudadSeleccionada = ciudades.find(ciudad => ciudad.nombreProyecto === value);
          // Asignamos el departamento de la ciudad seleccionada
          newFormData.departamento = ciudadSeleccionada ? ciudadSeleccionada.departamento : '';
        }

        return newFormData;
      });
    }
  };

  // Manejador de envío del formulario
  const handleSubmit = (e) => {
    e.preventDefault();

    // Crear un objeto para almacenar las respuestas transformadas
    const respuestasObj = {};
    formData.respuestas.forEach((respuesta, index) => {
      respuestasObj[`respuesta_${index + 1}`] = respuesta;
    });

    const correo = localStorage.getItem('correo');
    const fechaCargue = new Date().toISOString();
    // Crear un objeto con todos los datos del formulario, incluyendo las respuestas
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
      documento_estudiante: formData.tiEstudiante,
      grado: formData.grado,
      edad: formData.edad,
      genero: formData.genero,
      fecha_cargue: fechaCargue, // Agregar fecha de cargue 
      ...respuestasObj,
    };

    // Enviar los datos al backend
    postProyecto(proyectoData)
      .then(response => {
        setMensajeExito('La información fue cargada correctamente.');
        setTimeout(() => {
          // Reiniciar campos específicos
          setFormData(prevState => ({
            ...prevState,
            numeroCuadernillo: '',
            nombreEstudiante: '',
            tiEstudiante: '',
            grado: '',
            genero: '',  // Reiniciar 'genero'
            edad: '',
            respuestas: Array(20).fill(''), // Reiniciar las respuestas
          }));
          // Limpiar el mensaje de éxito después de 3 segundos
          setMensajeExito('');
        }, 2000);
      })
      .catch(error => {
        if (error.response) {
          // Error del backend
          alert(`Error al cargar la encuesta: ${error.response.data.error}`);
        } else {
          // Error en la red o no respuesta
          alert('Error de conexión o servidor');
        }
      });
};

  // Estilos del botón
  const buttonStyle = {
    width: '100%',
    padding: '10px',
    backgroundColor: '#1B8830',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: isFormComplete() ? 'pointer' : 'not-allowed',  // Cambiar el cursor según la validez del formulario
    transition: 'background-color 0.3s',  // Añadir transición para suavizar el cambio de color
  };

  const formContainerStyle = {
    maxHeight: '100vh', // Define la altura máxima de la ventana visible
    overflowY: 'auto', // Habilita el scroll vertical
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
                          <option value="A">A</option>
                          <option value="B">B</option>
                          <option value="C">C</option>
                          <option value="D">D</option>
                          <option value="Blanco">Blanco</option>
                          <option value="Multi Marca">Multi Marca</option>
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
  proyectos: state.proyectos.data || [],  // Asegúrate de que proyectos nunca sea undefined
  loading: state.proyectos.loading,
  error: state.proyectos.error,
});

const mapDispatchToProps = {
  getProyectos,
  postProyecto    
};

export default connect(mapStateToProps, mapDispatchToProps)(InfoLoad);
