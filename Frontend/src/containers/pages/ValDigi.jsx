import React, { useState, useEffect } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import { connect } from "react-redux";
import axios from "axios";

function ValDigi() {
  const [digitadores, setDigitadores] = useState([]);
  const [selectedDigitador, setSelectedDigitador] = useState("");
  const [selectedEmail, setSelectedEmail] = useState("");
  const [encuestas, setEncuestas] = useState([]); // Estado para las encuestas
  const [loading, setLoading] = useState(false);
  const [loadingEncuestas, setLoadingEncuestas] = useState(false);

  // Función para obtener digitadores
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

  // Función para obtener encuestas del digitador seleccionado (por email o responsable)
  const fetchEncuestas = async (responsable) => {
    setLoadingEncuestas(true);
    try {
      const res = await axios.get(
        `${process.env.REACT_APP_API_URL}/res/responsable/?responsable=${responsable}`
      );
      setEncuestas(Array.isArray(res.data) ? res.data : []); // Asegura que sea un arreglo
    } catch (err) {
      alert("Error al cargar encuestas: " + err.response?.data?.error);
      setEncuestas([]); // Reinicia a un arreglo vacío en caso de error
    } finally {
      setLoadingEncuestas(false);
    }
  };

  useEffect(() => {
    fetchDigitadores();
  }, []);

  const handleDigitadorChange = (e) => {
    const selectedEmail = e.target.value; // Obtén el email directamente desde el value del select
    setSelectedDigitador(selectedEmail);  // Establece el email seleccionado como el valor de selectedDigitador

    console.log(selectedEmail);  // Verifica si el email seleccionado es el esperado

    if (selectedEmail) {
      // Encuentra el digitador seleccionado por email
      const selected = digitadores.find((d) => d.email === selectedEmail);
      const email = selected ? selected.email : "";
      console.log(email);  // Verifica si el correo está siendo encontrado
      setSelectedEmail(email);
    } else {
      setSelectedEmail("");
      setEncuestas([]); // Limpia las encuestas si no hay un digitador seleccionado
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedDigitador) {
      alert("Por favor, selecciona un digitador.");
      return;
    }
    alert(`Digitador seleccionado: ${selectedEmail}`);
    if (selectedEmail) {
      fetchEncuestas(selectedEmail); // Obtiene las encuestas solo cuando se hace clic en el botón
    }
  };

  // Estilos personalizados
  const containerStyle = {
    maxWidth: "600px",
    margin: "50px auto",
    padding: "20px",
    borderRadius: "10px",
    backgroundColor: "#f9f9f9",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    textAlign: "center",
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

  const encuestasContainerStyle = {
    marginTop: "20px",
    textAlign: "left",
    maxHeight: "400px",   // Limita la altura del contenedor
    overflowY: "auto",    // Activa el scroll solo en la dirección vertical
  };

  const encuestaItemStyle = {
    borderBottom: "1px solid #ddd",
    padding: "10px 0",
  };

  const respuestaItemStyle = {
    marginLeft: "20px",
    fontStyle: "italic",
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

        {/* Mostrar las encuestas del digitador seleccionado */}
        <div style={encuestasContainerStyle}>
          <h2>Encuestas Asignadas</h2>
          {loadingEncuestas ? (
            <p>Cargando encuestas...</p>
          ) : encuestas.length > 0 ? (
            <ul>
              {encuestas.map((encuesta) => (
                <li key={encuesta.id} style={encuestaItemStyle}>
                  <strong>ID:</strong> {encuesta.id} -{" "}
                  <strong>Proyecto:</strong> {encuesta.nombre} -{" "}
                  <strong>Estudiante:</strong> {encuesta.nombre_estudiante} -{" "}
                  <strong>Fecha:</strong> {encuesta.fecha} -{" "}
                  <strong>Cuadernillo:</strong> {encuesta.numero_cuadernillo}

                  {/* Mostrar las respuestas */}
                  <div>
                    <strong>Respuestas:</strong>
                    <ul>
                      {[...Array(20).keys()].map((index) => {
                        const respuestaKey = `respuesta_${index + 1}`;
                        return (
                          <li key={respuestaKey} style={respuestaItemStyle}>
                            {respuestaKey.replace("_", " ").toUpperCase()}: {encuesta[respuestaKey]}
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                </li>
              ))}
            </ul>
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
