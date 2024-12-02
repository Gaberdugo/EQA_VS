import { useState } from "react";
import { connect } from "react-redux";
import axios from "axios";
import Layout2 from "hocs/Layouts/Layout2";

function AdminDigi() {
  const [formData, setFormData] = useState({
    email: "",
    first_name: "",
    second_name: "",
    last_name: "",
    second_last_name: "",
    role: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const { email, first_name, second_name, last_name, second_last_name, role, password } = formData;

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/create-user/`, formData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      setMessage("Usuario creado exitosamente.");
      
      console.log(res);

      setFormData({
        email: "",
        first_name: "",
        second_name: "",
        last_name: "",
        second_last_name: "",
        role: "",
        password: "",
      });
    } catch (err) {
      setError("Error al crear el usuario: " + (err.response?.data?.error || "Revise los datos ingresados."));
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
  };

  const titleStyle = {
    fontSize: "24px",
    marginBottom: "20px",
    color: "#333",
    textAlign: "center",
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    marginBottom: "15px",
    border: "1px solid #ddd",
    borderRadius: "5px",
    transition: "border-color 0.3s",
    fontSize: "16px",
  };

  const alertStyle = (type) => ({
    padding: "10px",
    borderRadius: "5px",
    marginBottom: "15px",
    backgroundColor: type === "success" ? "#d4edda" : "#f8d7da",
    color: type === "success" ? "#155724" : "#721c24",
    border: type === "success" ? "1px solid #c3e6cb" : "1px solid #f5c6cb",
  });

  return (
    <Layout2>
      <div style={containerStyle}>
        <h1 style={titleStyle}>Crear Usuario</h1>
        {message && <div style={alertStyle("success")}>{message}</div>}
        {error && <div style={alertStyle("error")}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            value={email}
            onChange={handleChange}
            placeholder="Correo Electrónico"
            style={inputStyle}
            onFocus={(e) => (e.target.style.borderColor = "#007bff")}
            onBlur={(e) => (e.target.style.borderColor = "#ddd")}
            required
          />
          <input
            type="text"
            name="first_name"
            value={first_name}
            onChange={handleChange}
            placeholder="Primer Nombre"
            style={inputStyle}
            required
          />
          <input
            type="text"
            name="second_name"
            value={second_name}
            onChange={handleChange}
            placeholder="Segundo Nombre"
            style={inputStyle}
          />
          <input
            type="text"
            name="last_name"
            value={last_name}
            onChange={handleChange}
            placeholder="Primer Apellido"
            style={inputStyle}
            required
          />
          <input
            type="text"
            name="second_last_name"
            value={second_last_name}
            onChange={handleChange}
            placeholder="Segundo Apellido"
            style={inputStyle}
            required
          />
          <select
            name="role"
            value={role}
            onChange={handleChange}
            style={inputStyle}
            required
          >
            <option value="">Selecciona un rol</option>
            <option value="digitador">Digitador</option>
            <option value="validador">Validador</option>
            <option value="terpel">Terpel</option>
          </select>
          <input
            type="password"
            name="password"
            value={password}
            onChange={handleChange}
            placeholder="Contraseña"
            style={inputStyle}
            required
          />
          
          <div
            className="container mt-5"
            style={{
              display: "flex", // Usamos flexbox
              justifyContent: "center", // Centra horizontalmente
            }}
          >
            <button
              type="submit"
              style={{
                backgroundColor: "#1B8830", // Color del botón
                color: "white", // Color del texto
                border: "none", // Sin borde
                padding: "10px 20px", // Espaciado interno
                fontSize: "16px", // Tamaño del texto
                borderRadius: "5px", // Bordes redondeados
                cursor: "pointer", // Cambia el cursor al pasar sobre el botón
              }}
            >
              Crear Usuario
            </button>
          </div>

        </form>
      </div>
    </Layout2>
  );
}

const mapStateToProps = (state) => ({});

export default connect(mapStateToProps, {})(AdminDigi);
