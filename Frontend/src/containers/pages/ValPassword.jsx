import React, { useState, useEffect } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValPassword() {
  const [usuarios, setUsuarios] = useState([]);
  const [emailSeleccionado, setEmailSeleccionado] = useState("");
  const [nuevaContrasena, setNuevaContrasena] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        const token = localStorage.getItem("access");
        const res = await axios.get(
          `${process.env.REACT_APP_API_URL}/auth/digitadores/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        const filtrados = res.data.filter((user) => !user.is_admin);
        setUsuarios(filtrados);
      } catch (error) {
        console.error("Error al obtener usuarios:", error);
        setMensaje("No se pudo obtener la lista de usuarios.");
      }
    };

    fetchUsuarios();
  }, []);

  const handleCambio = async () => {
    if (!emailSeleccionado || !nuevaContrasena) {
      setMensaje("⚠️ Completa todos los campos.");
      return;
    }

    const confirmacion = window.confirm(
      `¿Estás seguro que deseas cambiar la contraseña de ${emailSeleccionado}?`
    );
    if (!confirmacion) return;

    setLoading(true);
    setMensaje("");

    try {
      const token = localStorage.getItem("access");

      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/auth/admin/change-user-password/`,
        {
          email: emailSeleccionado,
          new_password: nuevaContrasena,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMensaje(res.data.message || "✅ Contraseña cambiada correctamente.");
      setNuevaContrasena("");
      setEmailSeleccionado("");
    } catch (err) {
      setMensaje(
        err.response?.data?.error || "❌ Error al cambiar la contraseña."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout4>
      <div
        style={{
          maxWidth: "600px",
          margin: "50px auto",
          padding: "20px",
          borderRadius: "10px",
          backgroundColor: "#f9f9f9",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          textAlign: "center",
        }}
      >
        <h2 style={{ fontSize: "24px", marginBottom: "20px", color: "#333" }}>
          Cambiar Contraseña de Usuario
        </h2>

        <select
          value={emailSeleccionado}
          onChange={(e) => setEmailSeleccionado(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        >
          <option value="">Seleccione un usuario</option>
          {usuarios.map((u) => (
            <option key={u.id} value={u.email}>
              {u.email}
            </option>
          ))}
        </select>

        <input
          type="password"
          placeholder="Nueva contraseña"
          value={nuevaContrasena}
          onChange={(e) => setNuevaContrasena(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />

        <button
          onClick={handleCambio}
          disabled={loading}
          style={{
            padding: "10px 20px",
            backgroundColor: "#33A652",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            fontSize: "16px",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Cambiando..." : "Cambiar Contraseña"}
        </button>

        {mensaje && (
          <p
            style={{
              marginTop: "20px",
              color: mensaje.includes("✅") ? "green" : "red",
            }}
          >
            {mensaje}
          </p>
        )}
      </div>
    </Layout4>
  );
}

export default ValPassword;
