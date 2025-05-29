import React, { useState, useEffect } from "react";
import Layout4 from "hocs/Layouts/Layout4";
import axios from "axios";

function ValProyecto() {
  const [nombreProyecto, setNombreProyecto] = useState("");
  const [ciudadesDisponibles, setCiudadesDisponibles] = useState([]);
  const [ciudadesSeleccionadas, setCiudadesSeleccionadas] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const [idAEliminar, setIdAEliminar] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchCiudades = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/api/ciudades/`);
        setCiudadesDisponibles(res.data);
      } catch (error) {
        console.error("Error al obtener ciudades:", error);
        setMensaje("❌ No se pudo obtener la lista de ciudades.");
      }
    };

    fetchCiudades();
  }, []);

  const handleCheckboxChange = (id) => {
    if (ciudadesSeleccionadas.includes(id)) {
      setCiudadesSeleccionadas(ciudadesSeleccionadas.filter((cid) => cid !== id));
    } else {
      setCiudadesSeleccionadas([...ciudadesSeleccionadas, id]);
    }
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
          ciudades_ids: ciudadesSeleccionadas,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (res.status === 200 || res.status === 201) {
        setMensaje("✅ Proyecto creado correctamente.");
        setNombreProyecto("");
        setCiudadesSeleccionadas([]);
        setTimeout(() => setMensaje(""), 2000);
      } else {
        setMensaje("❌ Algo salió mal al crear el proyecto.");
      }
    } catch (err) {
      console.error("Error al crear proyecto:", err);
      if (err.response) {
        setMensaje(err.response.data.error || "❌ Error del servidor.");
      } else {
        setMensaje("❌ Error de red.");
      }
    }

    setLoading(false);
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
          Crear Proyecto
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

        <div
          style={{
            textAlign: "left",
            maxHeight: "200px",
            overflowY: "auto",
            border: "1px solid #ccc",
            padding: "10px",
            borderRadius: "5px",
            marginBottom: "20px",
          }}
        >
          <p style={{ marginBottom: "10px", fontWeight: "bold" }}>
            Selecciona las ciudades:
          </p>
          {ciudadesDisponibles.map((ciudad) => (
            <label key={ciudad.id} style={{ display: "block", marginBottom: "5px" }}>
              <input
                type="checkbox"
                value={ciudad.id}
                checked={ciudadesSeleccionadas.includes(ciudad.id)}
                onChange={() => handleCheckboxChange(ciudad.id)}
              />
              {" " + ciudad.nombre}
            </label>
          ))}
        </div>

        <button
          onClick={handleGuardarProyecto}
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

        <h2 style={{ fontSize: "24px", marginBottom: "20px", marginTop: "40px",color: "#333" }}>
          Ver Proyectos
        </h2>

        <button
          onClick={() => window.open(`${process.env.REACT_APP_API_URL}/auth/excelPro/`, '_blank')}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            backgroundColor: "#33A652",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Descargar Excel de Proyectos
        </button>

        <h2 style={{ fontSize: "24px", marginBottom: "20px", marginTop: "40px", color: "#333" }}>
          Eliminar Proyecto
        </h2>

        <input
          type="text"
          placeholder="ID del proyecto"
          value={idAEliminar}
          onChange={(e) => setIdAEliminar(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />

        <button
          onClick={async () => {
            if (!idAEliminar.trim()) {
              setMensaje("⚠️ Ingresa un ID válido.");
              return;
            }

            const confirmacion = window.confirm(`¿Estás seguro de eliminar el proyecto con ID ${idAEliminar}?`);
            if (!confirmacion) return;

            try {
              await axios.delete(`${process.env.REACT_APP_API_URL}/auth/proyecto/${idAEliminar}/`);
              setMensaje("✅ Proyecto eliminado correctamente.");
              setIdAEliminar(""); // limpiar el input
            } catch (error) {
              console.error("Error al eliminar proyecto:", error);
              setMensaje("❌ No se pudo eliminar el proyecto.");
            }
          }}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            backgroundColor: "#FF1E0A",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Eliminar proyecto
        </button>


      </div>
    </Layout4>
  );
}

export default ValProyecto;
