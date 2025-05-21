import Layout4 from "hocs/Layouts/Layout4";
import React, { useState, useEffect } from 'react';
import axios from "axios";

function ValForm() {
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

  const [proyectos, setProyectos] = useState([]);
  const [ciudades, setCiudades] = useState([]);
  const [cuadernillos, setCuadernillos] = useState([]);
  const [mensajeExito, setMensajeExito] = useState('');
  const [instituciones, setInstituciones] = useState([]);

  useEffect(() => {
    const fetchProyectos = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`);
        setProyectos(res.data);
      } catch (error) {
        console.error("Error al cargar proyectos:", error);
      }
    };

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

    fetchProyectos();
    fetchCuadernillos();
  }, []);

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

  useEffect(() => {
    const fetchInstituciones = async () => {
      if (!formData.ciudad) {
        setInstituciones([]);
        return;
      }
  
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/ins/municipio/`, {
          params: { municipio: formData.ciudad }
        });
  
        const data = Array.isArray(response.data) ? response.data : [];
        setInstituciones(data);
      } catch (error) {
        console.error("Error al obtener instituciones:", error);
        setInstituciones([]);
      }
    };
  
    fetchInstituciones();
  }, [formData.ciudad]);  

  const formatDateToSQL = (isoString) => {
    const date = new Date(isoString);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}:${String(date.getSeconds()).padStart(2, '0')}`;
  };

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
      setFormData(prev => {
        const newRespuestas = [...prev.respuestas];
        newRespuestas[index] = value;
        return { ...prev, respuestas: newRespuestas };
      });
    } else {
      setFormData(prev => {
        const updated = { ...prev, [name]: value };
        if (name === 'ciudad') {
          const ciudadSeleccionada = ciudades.find(c => c.nombre === value);
          updated.departamento = ciudadSeleccionada ? ciudadSeleccionada.departamento : '';
        }
        return updated;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formattedDate = formatDateToSQL(new Date());
    const respuestasObj = {};
    formData.respuestas.forEach((r, i) => {
      respuestasObj[`respuesta_${i + 1}`] = r;
    });

    const correo = localStorage.getItem('correo');
    formData.tiEstudiante = Math.floor(Math.random() * 10_000_000_001).toString();

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
      fecha_cargue: formattedDate,
      ...respuestasObj,
    };

    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/info/proyectos/`, proyectoData);
      setMensajeExito('La información fue cargada correctamente.');
      setTimeout(() => {
        setFormData(prev => ({
          ...prev,
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
    } catch (error) {
      console.error("Error al enviar el formulario:", error);
      alert('Error al cargar la encuesta. Intente nuevamente.');
    }
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
    <Layout4>
      <form onSubmit={handleSubmit} style={formContainerStyle}>
        <h1 style={{ color: '#666666' }}>Cargue Prueba EQA</h1>
        {mensajeExito && (
          <div style={{ color: 'green', marginBottom: '15px' }}>
            <strong>{mensajeExito}</strong>
          </div>
        )}

        {/* Sección Proyecto y Fecha */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <select name="nombreProyecto" value={formData.nombreProyecto} onChange={handleChange} style={{ flex: '1', marginRight: '10px' }}>
            <option value="">Seleccione un proyecto</option>
            {proyectos.map(p => <option key={p.id} value={p.nombre}>{p.nombre}</option>)}
          </select>

          <input type="date" name="fechaAplicacion" value={formData.fechaAplicacion} onChange={handleChange} style={{ flex: '1' }} />
        </div>

        {/* Ciudad y Departamento */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <select name="ciudad" value={formData.ciudad} onChange={handleChange} disabled={!ciudades.length} style={{ flex: '1', marginRight: '10px' }}>
            <option value="">Seleccione una ciudad</option>
            {ciudades.map((c, i) => (
              <option key={i} value={c.nombre}>{c.nombre}</option>
            ))}
          </select>

          <input type="text" name="departamento" placeholder="Departamento" value={formData.departamento} readOnly style={{ flex: '1' }} />
        </div>

        {/* Aplicación y Prueba */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <label style={{ marginRight: '10px', flex: '1' }}>
            Aplicación:
            <select name="apli" value={formData.apli} onChange={handleChange} style={{ width: '100%' }}>
              <option value="">Seleccione</option>
              <option value="entrada">Entrada</option>
              <option value="salida">Salida</option>
            </select>
          </label>
          <label style={{ flex: '1' }}>
            Prueba:
            <select name="prueba" value={formData.prueba} onChange={handleChange} style={{ width: '100%' }}>
              <option value="">Seleccione</option>
              <option value="Matemáticas">Matemáticas</option>
              <option value="Lenguaje">Lenguaje</option>
            </select>
          </label>
        </div>

        {/* Institución y Cuadernillo */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <select name="nombreInstitucion" value={formData.nombreInstitucion} onChange={handleChange} style={{ flex: '1', marginRight: '10px' }}>
            <option value="">Seleccione una institución</option>
            {instituciones.map((inst, index) => (
              <option key={index} value={inst.nombre}>{inst.nombre}</option>
            ))}
          </select>
          <select name="numeroCuadernillo" value={formData.numeroCuadernillo} onChange={handleChange} style={{ flex: '1' }}>
            <option value="">Seleccione un cuadernillo</option>
            {cuadernillos.map((c, i) => <option key={i} value={c}>{c}</option>)}
          </select>
        </div>

        {/* Estudiante */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <input type="text" placeholder="Nombre del Estudiante" name="nombreEstudiante" value={formData.nombreEstudiante} onChange={handleChange} style={{ flex: '1', marginRight: '10px' }} />
          <input type="text" placeholder="Documento del Estudiante" name="tiEstudiante" value={formData.tiEstudiante} onChange={handleChange} style={{ flex: '1' }} />
        </div>

        {/* Grado, Género, Edad */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <label style={{ flex: '1', marginRight: '10px' }}>
            Grado:
            <select name="grado" value={formData.grado} onChange={handleChange} style={{ width: '100%' }}>
              <option value="">Seleccione</option>
              <option value="Tercero">Tercero</option>
              <option value="Quinto">Quinto</option>
            </select>
          </label>
          <label style={{ flex: '1', marginRight: '10px' }}>
            Género:
            <select name="genero" value={formData.genero} onChange={handleChange} style={{ width: '100%' }}>
              <option value="">Seleccione</option>
              <option value="Masculino">Masculino</option>
              <option value="Femenino">Femenino</option>
              <option value="No responde">No responde</option>
            </select>
          </label>
          <label style={{ flex: '1' }}>
            Fecha de nacimiento:
            <input type="date" name="edad" value={formData.edad} onChange={handleChange} style={{ width: '100%' }} />
          </label>
        </div>

        {/* Tabla de Respuestas */}
        <h2 style={{ color: '#B3B3B3' }}>Respuestas</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <tbody>
            {Array.from({ length: 5 }, (_, rowIndex) => (
              <tr key={rowIndex}>
                {Array.from({ length: 4 }, (_, colIndex) => {
                  const index = rowIndex * 4 + colIndex;
                  return (
                    <td key={colIndex} style={{ padding: '5px', border: '1px solid #ccc' }}>
                      <label>
                        Respuesta {index + 1}:
                        <select className="notranslate" name={`respuesta${index}`} value={formData.respuestas[index]} onChange={handleChange} style={{ width: '100%' }}>
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

        <button type="submit" style={buttonStyle} disabled={!isFormComplete()}>
          Enviar
        </button>

        {!isFormComplete() && (
          <p style={{ color: 'red', marginTop: '10px' }}>Por favor, complete todos los campos antes de enviar.</p>
        )}
      </form>
    </Layout4>
  );
}

export default ValForm;
