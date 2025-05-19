import React, { useState, useEffect } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValProyecto() {
  const [nombreProyecto, setNombreProyecto] = useState("");
  const [departamentos, setDepartamentos] = useState([]);
  const [ciudadesFiltradas, setCiudadesFiltradas] = useState([]);
  const [ciudadesSeleccionadas, setCiudadesSeleccionadas] = useState([]);
  const [departamentoSeleccionado, setDepartamentoSeleccionado] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchDepartamentos = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/api/departamentos/`);
        setDepartamentos(res.data);
      } catch (error) {
        console.error("Error al obtener departamentos:", error);
        setMensaje("❌ No se pudo obtener la lista de departamentos.");
      }
    };

    fetchDepartamentos();
  }, []);

  const handleDepartamentoChange = (e) => {
    const id = e.target.value;
    setDepartamentoSeleccionado(id);
    const departamento = departamentos.find((d) => d.id.toString() === id);
    setCiudadesFiltradas(departamento?.ciudades || []);
  };

  const toggleCiudadSeleccionada = (id) => {
    setCiudadesSeleccionadas((prev) =>
      prev.includes(id) ? prev.filter((cid) => cid !== id) : [...prev, id]
    );
  };

  const handleGuardarProyecto = async () => {
    if (!nombreProyecto.trim() || ciudadesSeleccionadas.length === 0) {
      setMensaje("⚠️ Completa todos los campos.");
      return;
    }

    setLoading(true);
    setMensaje("");

    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/auth/proyecto/`,
        {
          nombre: nombreProyecto,
          ciudades: ciudadesSeleccionadas,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (res.status === 201 || res.status === 200) {
        setMensaje("✅ Proyecto creado correctamente.");
        setNombreProyecto("");
        setDepartamentoSeleccionado("");
        setCiudadesSeleccionadas([]);
        setCiudadesFiltradas([]);
        setTimeout(() => {
          setMensaje("");
        }, 2000);
      }
    } catch (err) {
      console.error("Error al crear proyecto:", err);
      setMensaje("❌ Error al crear el proyecto.");
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
          Crear Nuevo Proyecto
        </h2>

        <input
          type="text"
          placeholder="Nombre del proyecto"
          value={nombreProyecto}
          onChange={(e) => setNombreProyecto(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />

        <select
          value={departamentoSeleccionado}
          onChange={handleDepartamentoChange}
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

        <div
          style={{
            textAlign: "left",
            marginBottom: "20px",
          }}
        >
          <strong>Ciudades:</strong>
          <ul style={{ listStyle: "none", paddingLeft: 0 }}>
            {ciudadesFiltradas.map((c) => (
              <li key={c.id}>
                <label>
                  <input
                    type="checkbox"
                    checked={ciudadesSeleccionadas.includes(c.id)}
                    onChange={() => toggleCiudadSeleccionada(c.id)}
                  />{" "}
                  {c.nombre}
                </label>
              </li>
            ))}
          </ul>
        </div>

        <button
          onClick={handleGuardarProyecto}
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
          {loading ? "Guardando..." : "Guardar Proyecto"}
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

export default ValProyecto;
