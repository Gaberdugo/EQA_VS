import React, { useState } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValPassword() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChangePassword = async () => {
    if (!currentPassword || !newPassword) {
      setMensaje("Por favor, completa ambos campos.");
      return;
    }

    setLoading(true);
    setMensaje("");

    try {
      const token = localStorage.getItem("access");

      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/auth/change-password/`,
        {
          current_password: currentPassword,
          new_password: newPassword,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setMensaje("Contraseña cambiada con éxito.");
    } catch (error) {
      const data = error.response?.data;
      setMensaje(
        data?.detail ||
        data?.current_password?.[0] ||
        data?.new_password?.[0] ||
        "Ocurrió un error al cambiar la contraseña."
      );
    } finally {
      setLoading(false);
      setCurrentPassword("");
      setNewPassword("");
    }
  };

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
    backgroundColor: "#33A652",
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
        <h2 style={titleStyle}>Cambiar Contraseña</h2>
        <input
          type="password"
          placeholder="Contraseña actual"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          style={inputStyle}
        />
        <input
          type="password"
          placeholder="Nueva contraseña"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          style={inputStyle}
        />
        <button
          onClick={handleChangePassword}
          style={buttonStyle}
          disabled={loading}
        >
          {loading ? "Cambiando..." : "Cambiar Contraseña"}
        </button>
        {mensaje && <p style={mensajeStyle}>{mensaje}</p>}
      </div>
    </Layout4>
  );
}

export default ValPassword;
