import React, { useState } from "react";
import axios from "axios";
import Layout2 from "hocs/Layouts/Layout2";

function AdminPre() {
  const [formData, setFormData] = useState({
    tipo: "", // 'mate' o 'lengua'
    codigo_pregunta: "",
    grado: "",
    competencia: "",
    componente: "",
    afirmacion: "",
    evidencia: "",
    tarea: "",
    dificultad: "Baja", // 'Baja', 'Media', 'Alta'
    clave: "",
    // Para lenguaje
    tipo_texto: "",
    secuencia_textual: "",
    num_texto: "",
    texto: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/preguntas/`, formData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      alert(res.data.message);
      setFormData({
        tipo: "",
        codigo_pregunta: "",
        grado: "",
        competencia: "",
        componente: "",
        afirmacion: "",
        evidencia: "",
        tarea: "",
        dificultad: "Baja",
        clave: "",
        tipo_texto: "",
        secuencia_textual: "",
        num_texto: "",
        texto: "",
      });
    } catch (err) {
      alert("Error al agregar la pregunta: " + err.response?.data?.error);
    }
  };

  // Estilos personalizados
  const containerStyle = {
    maxWidth: "800px",
    height: "80vh", // Altura máxima del contenedor
    margin: "50px auto",
    padding: "20px",
    borderRadius: "10px",
    backgroundColor: "#f9f9f9",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    overflowY: "auto", // Habilitar scroll vertical
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

  const fullWidthStyle = {
    width: "100%",
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "5px",
    fontSize: "16px",
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

  return (
    <Layout2>
      <div style={containerStyle}>
        <h1 style={titleStyle}>Agregar Pregunta</h1>
        <form onSubmit={handleSubmit}>
          {/* Primera fila: Tipo, Código de Pregunta, Grado */}
          <div style={formRowStyle}>
            <select
              name="tipo"
              value={formData.tipo}
              onChange={handleChange}
              style={inputStyle}
              required
            >
              <option value="">Tipo de Pregunta</option>
              <option value="mate">Matemáticas</option>
              <option value="lengua">Lenguaje</option>
            </select>
            <input
              type="text"
              name="codigo_pregunta"
              value={formData.codigo_pregunta}
              onChange={handleChange}
              placeholder="Código de Pregunta"
              style={inputStyle}
              required
            />
            <select
              name="grado"
              value={formData.grado}
              onChange={handleChange}
              style={inputStyle}
              required
            >
              <option value="">Grado</option>
              <option value="Tercero">Tercero</option>
              <option value="Quinto">Quinto</option>
            </select>
          </div>

          {/* Segunda fila: Competencia, Componente */}
          <div style={formRowStyle}>
            <input
              type="text"
              name="competencia"
              value={formData.competencia}
              onChange={handleChange}
              placeholder="Competencia"
              style={inputStyle}
              required
            />
            <input
              type="text"
              name="componente"
              value={formData.componente}
              onChange={handleChange}
              placeholder="Componente"
              style={inputStyle}
              required
            />
          </div>

          {/* Campos de ancho completo */}
          <textarea
            name="afirmacion"
            value={formData.afirmacion}
            onChange={handleChange}
            placeholder="Afirmación"
            style={fullWidthStyle}
            required
          />
          <textarea
            name="evidencia"
            value={formData.evidencia}
            onChange={handleChange}
            placeholder="Evidencia"
            style={fullWidthStyle}
            disabled={formData.tipo === "lengua"}
            required
          />
          <textarea
            name="tarea"
            value={formData.tarea}
            onChange={handleChange}
            placeholder="Tarea"
            style={fullWidthStyle}
            required
          />

          {/* Última fila: Dificultad, Clave */}
          <div style={formRowStyle}>
            <select
              name="dificultad"
              value={formData.dificultad}
              onChange={handleChange}
              style={inputStyle}
              required
            >
              <option value="Baja">Baja</option>
              <option value="Media">Media</option>
              <option value="Alta">Alta</option>
            </select>
            <select
              name="clave"
              value={formData.clave}
              onChange={handleChange}
              style={inputStyle}
              required
            >
              <option value="">Clave</option>
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>

          {/* Campos adicionales para preguntas de lenguaje */}
          {formData.tipo === "lengua" && (
            <>
              <div style={formRowStyle}>
                <input
                  type="text"
                  name="tipo_texto"
                  value={formData.tipo_texto}
                  onChange={handleChange}
                  placeholder="Tipo de Texto"
                  style={inputStyle}
                  required
                />
                <input
                  type="text"
                  name="secuencia_textual"
                  value={formData.secuencia_textual}
                  onChange={handleChange}
                  placeholder="Secuencia Textual"
                  style={inputStyle}
                  required
                />
              </div>
              <div style={formRowStyle}>
                <input
                  type="number"
                  name="num_texto"
                  value={formData.num_texto}
                  onChange={handleChange}
                  placeholder="Número de Texto"
                  style={inputStyle}
                  required
                />
              </div>
              <textarea
                name="texto"
                value={formData.texto}
                onChange={handleChange}
                placeholder="Texto"
                style={fullWidthStyle}
                required
              />
            </>
          )}

          <button type="submit" style={buttonStyle}>
            Agregar Pregunta
          </button>
        </form>
      </div>
    </Layout2>
  );
}

export default AdminPre;
