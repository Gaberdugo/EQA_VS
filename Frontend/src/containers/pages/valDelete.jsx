import React, { useState } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValDelete() {
  const [mensaje, setMensaje] = useState("");
  const [pk, setPk] = useState(""); // Almacena el ID de la encuesta a eliminar
  const [loading, setLoading] = useState(false);

  // Función para manejar la eliminación
  const eliminarEncuesta = async () => {
    if (!pk) {
      setMensaje("Por favor, proporciona un ID válido.");
      return;
    }

    // Preguntar al usuario si desea confirmar
    const confirm = window.confirm(
      "¿Estás seguro de que deseas eliminar esta encuesta?"
    );
    if (!confirm) {
      setMensaje("Eliminación cancelada.");
      return;
    }

    setLoading(true); // Mostrar el estado de carga mientras se procesa la solicitud
    setMensaje(""); // Limpiar mensajes anteriores

    try {
      const res = await axios.delete(
        `${process.env.REACT_APP_API_URL}/eliminar/${pk}/`
      );
      // Mostrar el mensaje devuelto por Django
      if (res.status === 204) {
        setMensaje("Encuesta eliminada con éxito."); // Mensaje estático como fallback
      } else {
        const data = res.data;
        setMensaje(data.message || "Encuesta eliminada con éxito.");
      }
    } catch (err) {
      // Manejar errores
      if (err.response) {
        const data = err.response.data;
        setMensaje(data.detail || "Ocurrió un error al eliminar la encuesta.");
      } else {
        setMensaje("Error de conexión o servidor.");
      }
    } finally {
      setLoading(false); // Detener el estado de carga
      setPk(""); // Limpiar el ID después del proceso
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
    backgroundColor: "#f44336",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  };

  const mensajeStyle = {
    marginTop: "20px",
    color: mensaje.includes("con éxito") ? "green" : "red",
  };

  return (
    <Layout4>
      <div style={containerStyle}>
        <h2 style={titleStyle}>Eliminar Encuesta</h2>
        <div>
          <label htmlFor="pk">ID de la Encuesta:</label>
          <input
            type="text"
            id="pk"
            value={pk}
            onChange={(e) => setPk(e.target.value)}
            placeholder="Ingrese el ID de la encuesta"
            style={inputStyle}
          />
        </div>
        <button
          onClick={eliminarEncuesta}
          style={buttonStyle}
          disabled={loading} // Desactiva el botón mientras se está cargando
        >
          {loading ? "Eliminando..." : "Eliminar"}
        </button>
        {mensaje && <p style={mensajeStyle}>{mensaje}</p>}
      </div>
    </Layout4>
  );
}

export default ValDelete;
