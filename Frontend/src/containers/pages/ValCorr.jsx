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
          datos,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setMensaje(res.data.message || "Encuesta modificada con éxito.");
      setDatos(null);
      setPk(""); // Resetear el ID de la encuesta
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

  // Estilos
  const styles = {
    container: {
      maxWidth: "800px",
      margin: "50px auto",
      padding: "20px",
      borderRadius: "10px",
      backgroundColor: "#f4f4f9",
      boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
      textAlign: "center",
    },
    input: {
      width: "100%",
      padding: "12px",
      borderRadius: "5px",
      border: "1px solid #ccc",
      fontSize: "16px",
      marginBottom: "20px",
    },
    button: {
      padding: "10px 20px",
      backgroundColor: "#1b8830",
      color: "#fff",
      border: "none",
      borderRadius: "5px",
      cursor: "pointer",
      fontSize: "16px",
      transition: "background-color 0.3s",
    },
    buttonCancel: {
      backgroundColor: "#f44336",
      marginLeft: "10px",
    },
    buttonHover: {
      backgroundColor: "#145d24",
    },
    mensaje: {
      marginTop: "20px",
      fontSize: "16px",
      color: mensaje.includes("éxito") ? "#2e7d32" : "#d32f2f",
    },
    formContainer: {
      maxHeight: "400px",
      overflowY: "auto",
      padding: "15px",
      border: "1px solid #ddd",
      borderRadius: "5px",
      backgroundColor: "#fff",
    },
    formField: {
      marginBottom: "15px",
      textAlign: "left",
    },
  };

  return (
    <Layout4>
      <div style={styles.container}>
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
              style={styles.input}
            />
            <button
              onClick={buscarEncuesta}
              style={{ ...styles.button }}
              disabled={loading}
            >
              {loading ? "Buscando..." : "Buscar Encuesta"}
            </button>
          </>
        )}

        {/* Mostrar y Editar Encuesta */}
        {datos && (
          <div style={styles.formContainer}>
            <form>
              {Object.keys(datos).map((key) => (
                <div key={key} style={styles.formField}>
                  <label htmlFor={key}>{key}:</label>
                  <input
                    type="text"
                    id={key}
                    name={key}
                    value={datos[key] || ""}
                    onChange={handleChange}
                    style={styles.input}
                  />
                </div>
              ))}
            </form>
          </div>
        )}

        {/* Botones de acción */}
        {datos && (
          <div style={{ marginTop: "20px" }}>
            <button
              onClick={guardarCambios}
              style={styles.button}
              disabled={loading}
            >
              {loading ? "Guardando..." : "Guardar Cambios"}
            </button>
            <button
              onClick={() => setDatos(null)}
              style={{ ...styles.button, ...styles.buttonCancel }}
            >
              Nueva Búsqueda
            </button>
          </div>
        )}

        {/* Mensaje de estado */}
        {mensaje && <p style={styles.mensaje}>{mensaje}</p>}
      </div>
    </Layout4>
  );
}

export default ValCorr;
