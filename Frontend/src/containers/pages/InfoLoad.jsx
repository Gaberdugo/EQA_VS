import React, { useState, useEffect } from 'react';
import Layout3 from "hocs/Layouts/Layout3";
import axios from "axios";

function InfoLoad() {
  const [formData, setFormData] = useState({
    nombreProyecto: '',
    ciudad: '',
    departamento: '',
    fechaAplicacion: '',
    apli: '',
    prueba: '',
    nombreInstitucion: '',
    numeroCuadernillo: '',
    nombreEstudiante: '',
    grado: '',
    genero: '',
    edad: '',
    respuestas: Array(20).fill(''),
  });

  const [proyectos, setProyectos] = useState([]);
  const [ciudades, setCiudades] = useState([]);
  const [cuadernillos, setCuadernillos] = useState([]);
  const [mensajeExito, setMensajeExito] = useState('');

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`)
      .then(res => setProyectos(res.data))
      .catch(() => alert('Error cargando proyectos'));

    axios.get(`${process.env.REACT_APP_API_URL}/res/cuader/`)
      .then(res => setCuadernillos(res.data))
      .catch(() => alert('Error cargando cuadernillos'));
  }, []);

  useEffect(() => {
    const proyecto = proyectos.find(p => p.nombre === formData.nombreProyecto);
    if (proyecto) setCiudades(proyecto.ciudades);
    else setCiudades([]);
  }, [formData.nombreProyecto, proyectos]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name.startsWith('respuesta')) {
      const index = parseInt(name.replace('respuesta', ''));
      const nuevas = [...formData.respuestas];
      nuevas[index] = value;
      setFormData({ ...formData, respuestas: nuevas });
    } else if (name === 'ciudad') {
      const ciudad = ciudades.find(c => c.nombre === value);
      setFormData({ ...formData, ciudad: value, departamento: ciudad ? ciudad.departamento : '' });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const correo = localStorage.getItem('correo') || 'usuario@example.com';
    const documentoEstudiante = Math.floor(Math.random() * 1e10).toString();
    const fechaCargue = new Date().toISOString().slice(0, 19).replace('T', ' ');

    const respuestasObj = {};
    formData.respuestas.forEach((r, i) => {
      respuestasObj[`respuesta_${i + 1}`] = r;
    });

    const payload = {
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
      fecha_cargue: fechaCargue,
      ...respuestasObj,
    };

    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/auth/proyecto/`, payload);
      setMensajeExito('¡Información cargada con éxito!');
      setFormData({
        ...formData,
        numeroCuadernillo: '',
        nombreEstudiante: '',
        grado: '',
        genero: '',
        edad: '',
        respuestas: Array(20).fill(''),
      });
      setTimeout(() => setMensajeExito(''), 3000);
    } catch (err) {
      console.error(err);
      alert('Error al guardar la información.');
    }
  };

  return (
    <Layout3>
      <div className="max-w-3xl mx-auto p-6 bg-white rounded shadow">
        <h2 className="text-xl font-bold mb-4">Cargar Información</h2>
        <form onSubmit={handleSubmit} className="space-y-4">

          <select name="nombreProyecto" value={formData.nombreProyecto} onChange={handleChange} className="w-full p-2 border rounded" required>
            <option value="">Seleccionar proyecto</option>
            {proyectos.map((p, i) => (
              <option key={i} value={p.nombre}>{p.nombre}</option>
            ))}
          </select>

          <select name="ciudad" value={formData.ciudad} onChange={handleChange} className="w-full p-2 border rounded" required>
            <option value="">Seleccionar ciudad</option>
            {ciudades.map((c, i) => (
              <option key={i} value={c.nombre}>{c.nombre}</option>
            ))}
          </select>

          <input type="text" name="departamento" value={formData.departamento} readOnly className="w-full p-2 border rounded bg-gray-100" />

          <input type="date" name="fechaAplicacion" value={formData.fechaAplicacion} onChange={handleChange} className="w-full p-2 border rounded" required />
          <input type="text" name="apli" value={formData.apli} onChange={handleChange} placeholder="Aplicación" className="w-full p-2 border rounded" required />
          <input type="text" name="prueba" value={formData.prueba} onChange={handleChange} placeholder="Prueba" className="w-full p-2 border rounded" required />
          <input type="text" name="nombreInstitucion" value={formData.nombreInstitucion} onChange={handleChange} placeholder="Institución" className="w-full p-2 border rounded" required />

          <select name="numeroCuadernillo" value={formData.numeroCuadernillo} onChange={handleChange} className="w-full p-2 border rounded" required>
            <option value="">Seleccionar cuadernillo</option>
            {cuadernillos.map((c, i) => (
              <option key={i} value={c.numero}>{c.numero}</option>
            ))}
          </select>

          <input type="text" name="nombreEstudiante" value={formData.nombreEstudiante} onChange={handleChange} placeholder="Nombre del estudiante" className="w-full p-2 border rounded" required />
          <input type="text" name="grado" value={formData.grado} onChange={handleChange} placeholder="Grado" className="w-full p-2 border rounded" required />
          <input type="text" name="genero" value={formData.genero} onChange={handleChange} placeholder="Género" className="w-full p-2 border rounded" required />
          <input type="number" name="edad" value={formData.edad} onChange={handleChange} placeholder="Edad" className="w-full p-2 border rounded" />

          <div className="grid grid-cols-4 gap-2">
            {formData.respuestas.map((r, i) => (
              <input
                key={i}
                type="text"
                name={`respuesta${i}`}
                value={r}
                onChange={handleChange}
                placeholder={`R${i + 1}`}
                className="p-2 border rounded"
              />
            ))}
          </div>

          <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
            Enviar
          </button>

          {mensajeExito && <p className="text-green-600">{mensajeExito}</p>}
        </form>
      </div>
    </Layout3>
  );
}

export default InfoLoad;
