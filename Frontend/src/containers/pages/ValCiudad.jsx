import React, { useState, useEffect } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValCiudad() {
  const [departamentos, setDepartamentos] = useState([]);
  const [departamentoSeleccionado, setDepartamentoSeleccionado] = useState("");
  const [nombreCiudad, setNombreCiudad] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchDepartamentos = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}auth/departamentos/`);
        setDepartamentos(res.data);
      } catch (error) {
        console.error("Error al obtener departamentos:", error);
        setMensaje("❌ No se pudo obtener la lista de departamentos.");
      }
    };

    fetchDepartamentos();
  }, []);

  const handleGuardarCiudad = async () => {
    if (!departamentoSeleccionado || !nombreCiudad.trim()) {
      setMensaje("⚠️ Completa todos los campos.");
      return;
    }

    setLoading(true);
    setMensaje("");

    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}auth/ciudades/`,
        {
          nombre: nombreCiudad,
          departamento: departamentoSeleccionado,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (res.status === 201 || res.status === 200) {
        setMensaje("✅ Ciudad creada correctamente.");
        setNombreCiudad("");
        setDepartamentoSeleccionado("");
        setTimeout(() => {
          setMensaje("");
        }, 2000);
      }
    } catch (err) {
      console.error("Error al crear ciudad:", err);
      setMensaje("❌ Error al crear la ciudad.");
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
          Crear Nueva Ciudad
        </h2>

        <select
          value={departamentoSeleccionado}
          onChange={(e) => setDepartamentoSeleccionado(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        >
          <option value="">Seleccione un departamento</option>
          {departamentos.map((d) => (
            <option key={d.id} value={d.id}>
              {d.nombre}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Nombre de la ciudad"
          value={nombreCiudad}
          onChange={(e) => setNombreCiudad(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />

        <button
          onClick={handleGuardarCiudad}
          disabled={loading}
          style={{
            padding: "10px 20px",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            fontSize: "16px",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Guardando..." : "Guardar Ciudad"}
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

export default ValCiudad;
