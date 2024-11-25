import React, { useState, useEffect } from "react";
import axios from "axios";
import Layout2 from "hocs/Layouts/Layout2";

function AdminCua() {
  const [formData, setFormData] = useState({
    materia: "",
    grado: "",
    preguntasSeleccionadas: [], // IDs de las preguntas seleccionadas
  });

  const [preguntasDisponibles, setPreguntasDisponibles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFormChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const fetchPreguntas = async () => {
    if (!formData.materia || !formData.grado) return;

    setLoading(true);
    try {
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/preguntas/`, {
        params: { materia: formData.materia, grado: formData.grado },
      });
      setPreguntasDisponibles(res.data); // Se asume que el backend retorna un arreglo de preguntas
    } catch (err) {
      alert("Error al cargar preguntas: " + err.response?.data?.error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPreguntas();
  }, [formData.materia, formData.grado]);

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

  // Estilos personalizados
  const containerStyle = {
    maxWidth: "800px",
    margin: "50px auto",
    padding: "20px",
    borderRadius: "10px",
    backgroundColor: "#f9f9f9",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  };

  const titleStyle = {
    fontSize: "24px",
    marginBottom: "20px",
    color: "#333",
    textAlign: "center",
  };

  const formRowStyle = {
    display: "flex",
    gap: "10px",
    marginBottom: "15px",
  };

  const inputStyle = {
    flex: 1,
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "5px",
    fontSize: "16px",
  };

  const buttonStyle = {
    width: "100%",
    padding: "10px",
    backgroundColor: "#1B8830",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  };

  const preguntaStyle = {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px",
    borderBottom: "1px solid #ddd",
    alignItems: "center",
  };

  const preguntaTextStyle = {
    flex: 1,
    marginRight: "10px",
  };

  const checkboxStyle = {
    width: "20px",
    height: "20px",
  };

  return (
    <Layout2>
      <div style={containerStyle}>
        <h1 style={titleStyle}>Crear Cuadernillo</h1>
        <form onSubmit={handleSubmit}>
          {/* Materia y Grado */}
          <div style={formRowStyle}>
            <select
              name="materia"
              value={formData.materia}
              onChange={handleFormChange}
              style={inputStyle}
              required
            >
              <option value="">Selecciona Materia</option>
              <option value="mate">Matemáticas</option>
              <option value="lengua">Lenguaje</option>
            </select>
            <select
              name="grado"
              value={formData.grado}
              onChange={handleFormChange}
              style={inputStyle}
              required
            >
              <option value="">Selecciona Grado</option>
              <option value="Tercero">Tercero</option>
              <option value="Quinto">Quinto</option>
            </select>
          </div>

          {/* Preguntas disponibles */}
          <div style={{ margin: "20px 0" }}>
            <h2 style={{ fontSize: "20px", marginBottom: "10px" }}>Preguntas Disponibles</h2>
            {loading ? (
              <p>Cargando preguntas...</p>
            ) : (
              preguntasDisponibles.map((pregunta) => (
                <div key={pregunta.id} style={preguntaStyle}>
                  <span style={preguntaTextStyle}>{pregunta.afirmacion}</span>
                  <input
                    type="checkbox"
                    checked={formData.preguntasSeleccionadas.includes(pregunta.id)}
                    onChange={() => togglePregunta(pregunta.id)}
                    style={checkboxStyle}
                  />
                </div>
              ))
            )}
          </div>

          {/* Botón de envío */}
          <button type="submit" style={buttonStyle}>
            Crear Cuadernillo
          </button>
        </form>
      </div>
    </Layout2>
  );
}

export default AdminCua;