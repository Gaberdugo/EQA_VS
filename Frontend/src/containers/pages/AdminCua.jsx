import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import Layout2 from "hocs/Layouts/Layout2";

function AdminCua() {
  const [formData, setFormData] = useState({
    materia: "",
    grado: "",
    preguntasSeleccionadas: [],
  });

  const [preguntasDisponibles, setPreguntasDisponibles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFormChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const fetchPreguntas = useCallback(async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/preguntas/`, {
        params: { materia: formData.materia, grado: formData.grado },
      });
      setPreguntasDisponibles(res.data);
    } catch (err) {
      alert("Error al cargar preguntas: " + err.response?.data?.error);
    } finally {
      setLoading(false);
    }
  }, [formData.materia, formData.grado]);

  useEffect(() => {
    if (formData.materia && formData.grado) {
      fetchPreguntas();
    }
  }, [formData.materia, formData.grado, fetchPreguntas]);

  const togglePregunta = (id) => {
    const isSelected = formData.preguntasSeleccionadas.includes(id);
    const updatedSeleccionadas = isSelected
      ? formData.preguntasSeleccionadas.filter((pid) => pid !== id)
      : [...formData.preguntasSeleccionadas, id];
    setFormData({ ...formData, preguntasSeleccionadas: updatedSeleccionadas });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.preguntasSeleccionadas.length !== 20) {
      alert("Debes seleccionar exactamente 20 preguntas para crear el cuadernillo.");
      return;
    }
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/cuadernillos/`, formData, {
        headers: { "Content-Type": "application/json" },
      });
      alert(res.data.message);
      setFormData({
        materia: "",
        grado: "",
        preguntasSeleccionadas: [],
      });
      setPreguntasDisponibles([]);
    } catch (err) {
      alert("Error al crear el cuadernillo: " + err.response?.data?.error);
    }
  };

  return (
    <Layout2>
      <div>
        <h1>Crear Cuadernillo</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <select name="materia" value={formData.materia} onChange={handleFormChange} required>
              <option value="">Selecciona Materia</option>
              <option value="mate">Matemáticas</option>
              <option value="lengua">Lenguaje</option>
            </select>
            <select name="grado" value={formData.grado} onChange={handleFormChange} required>
              <option value="">Selecciona Grado</option>
              <option value="Tercero">Tercero</option>
              <option value="Quinto">Quinto</option>
            </select>
          </div>
          <div>
            <h2>Preguntas Disponibles</h2>
            {loading ? (
              <p>Cargando preguntas...</p>
            ) : (
              preguntasDisponibles.map((pregunta) => (
                <div key={pregunta.id}>
                  <span>{pregunta.afirmacion}</span>
                  <input
                    type="checkbox"
                    checked={formData.preguntasSeleccionadas.includes(pregunta.id)}
                    onChange={() => togglePregunta(pregunta.id)}
                  />
                </div>
              ))
            )}
          </div>
          <button type="submit">Crear Cuadernillo</button>
        </form>
      </div>
    </Layout2>
  );
}

export default AdminCua;
