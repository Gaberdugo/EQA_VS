import React, { useState, useEffect } from 'react';
import Layout3 from "hocs/Layouts/Layout3";
import axios from "axios";

function InfoLoad() {
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

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`)
      .then(res => {
        setProyectos(res.data);
      })
      .catch(() => alert('Error al cargar los proyectos'));

    axios.get(`${process.env.REACT_APP_API_URL}/res/cuader/`)
      .then(res => {
        setCuadernillos(Array.isArray(res.data) ? res.data : []);
      })
      .catch(() => {
        alert("Error al obtener los cuadernillos");
        setCuadernillos([]);
      });
  }, []);

  useEffect(() => {
    if (formData.nombreProyecto) {
      const proyecto = proyectos.find(p => p.nombre === formData.nombreProyecto);
      if (proyecto) {
        setCiudades(proyecto.ciudades);
      }
    } else {
      setCiudades([]);
    }
  }, [formData.nombreProyecto, proyectos]);

  const formatDateToSQL = (isoString) => {
    const date = new Date(isoString);
    return date.toISOString().slice(0, 19).replace('T', ' ');
  };

  const isFormComplete = () => {
    const requiredFields = [
      'nombreProyecto', 'ciudad', 'departamento', 'fechaAplicacion',
      'apli', 'prueba', 'nombreInstitucion', 'numeroCuadernillo',
      'nombreEstudiante', 'grado', 'genero'
    ];
    for (let field of requiredFields) {
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
        const nuevas = [...prev.respuestas];
        nuevas[index] = value;
        return { ...prev, respuestas: nuevas };
      });
    } else {
      setFormData(prev => {
        const nuevo = { ...prev, [name]: value };
        if (name === 'ciudad') {
          const ciudad = ciudades.find(c => c.nombre === value);
          nuevo.departamento = ciudad ? ciudad.departamento : '';
        }
        return nuevo;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formattedDate = formatDateToSQL(new Date());
    const correo = localStorage.getItem('correo');
    const documentoEstudiante = Math.floor(Math.random() * 10_000_000_001).toString();

    const respuestasObj = {};
    formData.respuestas.forEach((r, i) => {
      respuestasObj[`respuesta_${i + 1}`] = r;
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

    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/auth/proyecto/`, proyectoData);
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
      if (error.response) {
        alert(`Error: ${error.response.data.error}`);
      } else {
        alert('Error de conexión o del servidor');
      }
    }
  };

  return (
    <Layout3>
      <div className="p-8 max-w-4xl mx-auto bg-white rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-4">Cargar Información</h2>
        <form onSubmit={handleSubmit} className="space-y-4">

          {/* Proyecto */}
          <select name="nombreProyecto" value={formData.nombreProyecto} onChange={handleChange} required className="w-full p-2 border rounded">
            <option value="">Seleccione un proyecto</option>
            {proyectos.map((p, i) => (
              <option key={i} value={p.nombre}>{p.nombre}</option>
            ))}
          </select>

          {/* Ciudad */}
          <select name="ciudad" value={formData.ciudad} onChange={handleChange} required className="w-full p-2 border rounded">
            <option value="">Seleccione una ciudad</option>
            {ciudades.map((c, i) => (
              <option key={i} value={c.nombre}>{c.nombre}</option>
            ))}
          </select>

          {/* Departamento */}
          <input type="text" name="departamento" value={formData.departamento} readOnly className="w-full p-2 border rounded bg-gray-100" />

          {/* Fecha de aplicación */}
          <input type="date" name="fechaAplicacion" value={formData.fechaAplicacion} onChange={handleChange} required className="w-full p-2 border rounded" />

          {/* Aplicación y Prueba */}
          <input name="apli" value={formData.apli} onChange={handleChange} placeholder="Aplicación" required className="w-full p-2 border rounded" />
          <input name="prueba" value={formData.prueba} onChange={handleChange} placeholder="Prueba" required className="w-full p-2 border rounded" />

          {/* Institución */}
          <input name="nombreInstitucion" value={formData.nombreInstitucion} onChange={handleChange} placeholder="Nombre de la Institución" required className="w-full p-2 border rounded" />

          {/* Cuadernillo */}
          <select name="numeroCuadernillo" value={formData.numeroCuadernillo} onChange={handleChange} required className="w-full p-2 border rounded">
            <option value="">Seleccione un cuadernillo</option>
            {cuadernillos.map((c, i) => (
              <option key={i} value={c.numero}>{c.numero}</option>
            ))}
          </select>

          {/* Estudiante */}
          <input name="nombreEstudiante" value={formData.nombreEstudiante} onChange={handleChange} placeholder="Nombre del Estudiante" required className="w-full p-2 border rounded" />
          <input name="grado" value={formData.grado} onChange={handleChange} placeholder="Grado" required className="w-full p-2 border rounded" />
          <input name="genero" value={formData.genero} onChange={handleChange} placeholder="Género" required className="w-full p-2 border rounded" />
          <input name="edad" type="number" value={formData.edad} onChange={handleChange} placeholder="Edad" className="w-full p-2 border rounded" />

          {/* Tabla de Respuestas */}
          <div className="grid grid-cols-4 gap-2">
            {formData.respuestas.map((res, i) => (
              <input
                key={i}
                type="text"
                name={`respuesta${i}`}
                placeholder={`R${i + 1}`}
                value={res}
                onChange={handleChange}
                className="p-2 border rounded"
              />
            ))}
          </div>

          {/* Botón de envío */}
          <button type="submit" disabled={!isFormComplete()} className="bg-blue-600 text-white px-4 py-2 rounded">
            Enviar
          </button>

          {/* Mensaje de éxito */}
          {mensajeExito && (
            <div className="text-green-600 font-bold mt-2">{mensajeExito}</div>
          )}
        </form>
      </div>
    </Layout3>
  );
}

export default InfoLoad;
