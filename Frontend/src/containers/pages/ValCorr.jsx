import React, { useState } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValCorr() {
  const [pk, setPk] = useState(""); // ID de la encuesta
  const [campo, setCampo] = useState(""); // Campo a modificar
  const [valor, setValor] = useState(""); // Nuevo valor
  const [mensaje, setMensaje] = useState(""); // Mensaje de estado
  const [loading, setLoading] = useState(false); // Estado de carga

  const handleModificar = async () => {
    if (!pk || !campo || !valor) {
      setMensaje("Por favor, completa todos los campos.");
      return;
    }

    setLoading(true);
    setMensaje("");

    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/res/modificar/`,
        {
          id: pk,
          campo,
          valor,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setMensaje(res.data.message || "Modificación realizada con éxito.");
    } catch (err) {
      if (err.response) {
        setMensaje(err.response.data.detail || "Error en el servidor.");
      } else {
        setMensaje("Error de conexión.");
      }
    } finally {
      setLoading(false);
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
        <div>
          <label htmlFor="pk">ID de la Encuesta:</label>
          <input
            type="text"
            id="pk"
            value={pk}
            onChange={(e) => setPk(e.target.value)}
            placeholder="Ingrese el ID"
            style={inputStyle}
          />
        </div>
        <div>
          <label htmlFor="campo">Campo a Modificar:</label>
          <input
            type="text"
            id="campo"
            value={campo}
            onChange={(e) => setCampo(e.target.value)}
            placeholder="Ingrese el campo"
            style={inputStyle}
          />
        </div>
        <div>
          <label htmlFor="valor">Nuevo Valor:</label>
          <input
            type="text"
            id="valor"
            value={valor}
            onChange={(e) => setValor(e.target.value)}
            placeholder="Ingrese el nuevo valor"
            style={inputStyle}
          />
        </div>
        <button onClick={handleModificar} style={buttonStyle} disabled={loading}>
          {loading ? "Modificando..." : "Modificar"}
        </button>
        {mensaje && <p style={mensajeStyle}>{mensaje}</p>}
      </div>
    </Layout4>
  );
}

export default ValCorr;
