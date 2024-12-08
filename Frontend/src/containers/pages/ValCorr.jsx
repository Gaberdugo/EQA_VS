import React, { useState } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValCorr() {
  const [pk, setPk] = useState(""); // ID de la encuesta
  const [datos, setDatos] = useState(null); // Datos de la encuesta
  const [mensaje, setMensaje] = useState(""); // Mensaje de estado
  const [loading, setLoading] = useState(false); // Estado de carga

  // Función para buscar los datos de la encuesta por ID
  const buscarEncuesta = async () => {
    if (!pk) {
      setMensaje("Por favor, ingresa un ID.");
      return;
    }

    setLoading(true);
    setMensaje("");

    try {
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/res/obtener/${pk}/`);
      setDatos(res.data);
      setMensaje("Encuesta cargada con éxito.");
    } catch (err) {
      if (err.response) {
        setMensaje(err.response.data.detail || "Error al cargar la encuesta.");
      } else {
        setMensaje("Error de conexión.");
      }
      setDatos(null);
    } finally {
      setLoading(false);
    }
  };

  // Función para manejar los cambios en los campos del formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setDatos((prev) => ({ ...prev, [name]: value }));
  };

  // Función para guardar los cambios
  const guardarCambios = async () => {
    if (!datos) return;

    setLoading(true);
    setMensaje("");

    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/res/modificar/`,
        {
          id: pk,
          datos, // Enviar todos los datos actualizados
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setMensaje(res.data.message || "Encuesta modificada con éxito.");
    } catch (err) {
      if (err.response) {
        setMensaje(err.response.data.detail || "Error al guardar los cambios.");
      } else {
        setMensaje("Error de conexión.");
      }
    } finally {
      setLoading(false);
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
    textAlign: "center",
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ddd",
    fontSize: "16px",
    marginBottom: "20px",
  };

  const buttonStyle = {
    padding: "10px 20px",
    backgroundColor: "#1B8830",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  };

  const mensajeStyle = {
    marginTop: "20px",
    color: mensaje.includes("éxito") ? "green" : "red",
  };

  return (
    <Layout4>
      <div style={containerStyle}>
        <h2>Modificar Encuesta</h2>

        {/* Buscar Encuesta */}
        {!datos && (
          <>
            <label htmlFor="pk">ID de la Encuesta:</label>
            <input
              type="text"
              id="pk"
              value={pk}
              onChange={(e) => setPk(e.target.value)}
              placeholder="Ingrese el ID"
              style={inputStyle}
            />
            <button onClick={buscarEncuesta} style={buttonStyle} disabled={loading}>
              {loading ? "Buscando..." : "Buscar Encuesta"}
            </button>
          </>
        )}

        {/* Mostrar y Editar Encuesta */}
        {datos && (
          <form>
            {Object.keys(datos).map((key) => (
              <div key={key} style={{ marginBottom: "10px" }}>
                <label htmlFor={key}>{key}:</label>
                <input
                  type="text"
                  id={key}
                  name={key}
                  value={datos[key] || ""}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
            ))}
            <button
              type="button"
              onClick={guardarCambios}
              style={buttonStyle}
              disabled={loading}
            >
              {loading ? "Guardando..." : "Guardar Cambios"}
            </button>
            <button
              type="button"
              onClick={() => setDatos(null)} // Resetear el estado
              style={{ ...buttonStyle, backgroundColor: "#f44336", marginLeft: "10px" }}
            >
              Cancelar
            </button>
          </form>
        )}

        {/* Mensaje de estado */}
        {mensaje && <p style={mensajeStyle}>{mensaje}</p>}
      </div>
    </Layout4>
  );
}

export default ValCorr;
