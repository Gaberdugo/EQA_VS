import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children, requiredRole }) => {
    const role = localStorage.getItem('role');

    if (role !== requiredRole) {
        return <Navigate to="/login" />; // O redirigir a una página de acceso denegado
    }

    return children; // Permitir acceso a la ruta
};

export default PrivateRoute;