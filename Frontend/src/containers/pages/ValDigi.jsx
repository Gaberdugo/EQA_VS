import React, { useState, useEffect } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import { connect } from "react-redux";
import axios from "axios";

function ValDigi() {
  const [digitadores, setDigitadores] = useState([]);
  const [selectedDigitador, setSelectedDigitador] = useState("");
  const [selectedEmail, setSelectedEmail] = useState("");
  const [encuestas, setEncuestas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingEncuestas, setLoadingEncuestas] = useState(false);

  const fetchDigitadores = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/digitadores/`);
      setDigitadores(res.data);
    } catch (err) {
      alert("Error al cargar digitadores: " + err.response?.data?.error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEncuestas = async (responsable) => {
    setLoadingEncuestas(true);
    try {
      const res = await axios.get(
        `${process.env.REACT_APP_API_URL}/res/responsable/?responsable=${responsable}`
      );
      setEncuestas(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      alert("Error al cargar encuestas: " + err.response?.data?.error);
      setEncuestas([]);
    } finally {
      setLoadingEncuestas(false);
    }
  };

  useEffect(() => {
    fetchDigitadores();
  }, []);

  const handleDigitadorChange = (e) => {
    const selectedEmail = e.target.value;
    setSelectedDigitador(selectedEmail);
    if (selectedEmail) {
      const selected = digitadores.find((d) => d.email === selectedEmail);
      const email = selected ? selected.email : "";
      setSelectedEmail(email);
    } else {
      setSelectedEmail("");
      setEncuestas([]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedDigitador) {
      alert("Por favor, selecciona un digitador.");
      return;
    }
    fetchEncuestas(selectedEmail);
  };

  const containerStyle = {
    maxWidth: "900px",
    margin: "50px auto",
    padding: "20px",
    borderRadius: "10px",
    backgroundColor: "#f9f9f9",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    textAlign: "center",
  };

  const scrollableContainerStyle = {
    maxHeight: "500px",
    overflowY: "auto",
    overflowX: "auto",
    border: "1px solid #ddd",
    borderRadius: "10px",
    marginTop: "20px",
  };

  const titleStyle = {
    fontSize: "24px",
    marginBottom: "20px",
    color: "#333",
  };

  const selectStyle = {
    width: "100%",
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ddd",
    fontSize: "16px",
    marginBottom: "20px",
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

  const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
  };

  const headerStyle = {
    backgroundColor: "#f4f4f4",
    border: "1px solid #ccc",
    padding: "10px",
    textAlign: "left",
    fontWeight: "bold",
    position: "sticky",
    top: "0",
    zIndex: "1",
  };

  const cellStyle = {
    border: "1px solid #ccc",
    padding: "10px",
    textAlign: "left",
  };

  return (
    <Layout4>
      <div style={containerStyle}>
        <h1 style={titleStyle}>Seleccionar Digitador</h1>
        <form onSubmit={handleSubmit}>
          {loading ? (
            <p>Cargando digitadores...</p>
          ) : (
            <select
              value={selectedDigitador}
              onChange={handleDigitadorChange}
              style={selectStyle}
              required
            >
              <option value="">Seleccione un digitador</option>
              {digitadores.map((digitador) => (
                <option key={digitador.email} value={digitador.email}>
                  {digitador.first_name} {digitador.second_name} ({digitador.email})
                </option>
              ))}
            </select>
          )}
          <button type="submit" style={buttonStyle}>
            Confirmar
          </button>
        </form>

        {/* Contenedor con scroll */}
        <div style={scrollableContainerStyle}>
          {loadingEncuestas ? (
            <p>Cargando encuestas...</p>
          ) : encuestas.length > 0 ? (
            <table style={tableStyle}>
              <thead>
                <tr>
                  <th style={headerStyle}>ID</th>
                  <th style={headerStyle}>Proyecto</th>
                  <th style={headerStyle}>Estudiante</th>
                  <th style={headerStyle}>Género</th>
                  <th style={headerStyle}>Curso</th>
                  <th style={headerStyle}>Fecha</th>
                  <th style={headerStyle}>Cuadernillo</th>
                  {[...Array(20).keys()].map((index) => (
                    <th key={`respuesta_${index + 1}`} style={headerStyle}>
                      Respuesta {index + 1}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {encuestas.map((encuesta) => (
                  <tr key={encuesta.id}>
                    <td style={cellStyle}>{encuesta.id}</td>
                    <td style={cellStyle}>{encuesta.nombre}</td>
                    <td style={cellStyle}>{encuesta.nombre_estudiante}</td>
                    <td style={cellStyle}>{encuesta.genero}</td>
                    <td style={cellStyle}>{encuesta.grado}</td>
                    <td style={cellStyle}>{encuesta.fecha}</td>
                    <td style={cellStyle}>{encuesta.numero_cuadernillo}</td>
                    {[...Array(20).keys()].map((index) => {
                      const respuestaKey = `respuesta_${index + 1}`;
                      return (
                        <td key={respuestaKey} style={cellStyle}>
                          {encuesta[respuestaKey]}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No se encontraron encuestas para este digitador.</p>
          )}
        </div>
      </div>
    </Layout4>
  );
}

const mapStateToProps = (state) => ({});

export default connect(mapStateToProps, {})(ValDigi);
